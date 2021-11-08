'''
模型名：开门输入信号异常诊断模型
逻辑：
1. 零速信号无效；
2. 车门处于关闭状态；
3. 开门输入信号发生跳变；
4. 24小时内发生信号跳变10次及以上或者用一次通断电代替,每次上电从0次重新开始累计10次及以上

开门信号
0 -> 1（1至5个周期） -> 0
'''


import time
from datetime import datetime
from typing import Dict, List, Any

import numpy as np
import pandas as pd

from globalbase.model_abc import FrameModel
from globalbase.myfunc import stack_dataframe
from globalbase.func_zb import add_block_no
from pandasql import sqldf


# ZeroSpeedSignal           {"0":"无效","1":"有效"}
# DoorClose                 {"0":"不关闭","1":"关闭"}
# DoorOpenSignalFeedback    {"0":"无效","1":"开门"}

SYS_CODE = ['07']
DATA_MAPPING = {'ZeroSpeedSignal-01': '1107_3_4_1_1',
                'ZeroSpeedSignal-02': '1107_31_4_1_1',
                'ZeroSpeedSignal-03': '1107_59_4_1_1',
                'ZeroSpeedSignal-04': '1107_87_4_1_1',
                'ZeroSpeedSignal-05': '1107_115_4_1_1',
                'ZeroSpeedSignal-06': '1107_143_4_1_1',
                'ZeroSpeedSignal-07': '1107_171_4_1_1',
                'ZeroSpeedSignal-08': '1107_199_4_1_1',
                'ZeroSpeedSignal-09': '1107_227_4_1_1',
                'ZeroSpeedSignal-10': '1107_255_4_1_1',
                'DoorClose-01': '1107_1_4_1_1',
                'DoorClose-02': '1107_29_4_1_1',
                'DoorClose-03': '1107_57_4_1_1',
                'DoorClose-04': '1107_85_4_1_1',
                'DoorClose-05': '1107_113_4_1_1',
                'DoorClose-06': '1107_141_4_1_1',
                'DoorClose-07': '1107_169_4_1_1',
                'DoorClose-08': '1107_197_4_1_1',
                'DoorClose-09': '1107_225_4_1_1',
                'DoorClose-10': '1107_253_4_1_1',
                'DoorOpenSignalFeedback-01': '1107_2_6_1_1',
                'DoorOpenSignalFeedback-02': '1107_30_6_1_1',
                'DoorOpenSignalFeedback-03': '1107_58_6_1_1',
                'DoorOpenSignalFeedback-04': '1107_86_6_1_1',
                'DoorOpenSignalFeedback-05': '1107_114_6_1_1',
                'DoorOpenSignalFeedback-06': '1107_142_6_1_1',
                'DoorOpenSignalFeedback-07': '1107_170_6_1_1',
                'DoorOpenSignalFeedback-08': '1107_198_6_1_1',
                'DoorOpenSignalFeedback-09': '1107_226_6_1_1',
                'DoorOpenSignalFeedback-10': '1107_254_6_1_1'}


class Model(FrameModel):

    model_name: str = '开门输入信号异常诊断模型'
    model_code: str = 'ZB_M0027'
    threshold: Dict = {'max_count': 10}
    error_message_template = {
        1: "{line},{train_no},{coach_no},车门系统,{model_name},{model_code},ZB_M002701,{door_no}车门开门输入信号异常,,2,{ccu_time}"
    }

    # fetch data : time intervel
    start_time: int = None
    time_window: int = 1800

    # cache data define
    df_summary_last: pd.DataFrame = pd.DataFrame()
    prev_data_batch_time: float = None

    def initilize(self) -> None:
        self.hbase_conn.data_mapping = DATA_MAPPING

    def core_logic(self, df: pd.DataFrame) -> List[Dict]:

        # Step 1: Stop loop if no valid data fetched
        info_list = []
        if df.empty:
            return info_list

        # Step 2: set dtypes
        df_dtype = self.set_dtypes(df)

        # Step 3: reset historical count data
        self.try_reset_hist_data(df_dtype)

        # Step 4: stack data for door_no columns
        model_col_no = len(DATA_MAPPING)
        stack_columns = list(df.columns[-model_col_no:])

        df_stack = stack_dataframe(
            df, stack_columns=stack_columns, suffix_name='door_no')

        # Step 5: filetering data with model condition
        _filter = (df_stack['ZeroSpeedSignal'] == 0) & (
            df_stack['DoorClose'] == 1)
        df_filter = df_stack[_filter]

        # Step 5: calculate current dataframe's hop times for each door
        df_hop_count = self.count_hop_times(df_filter)

        # Step 6: merge summary data
        df_summary_cur = self.merge_summary_df(
            self.df_summary_last, df_hop_count)

        # Step 7: get alarm info via comparing two summary records
        msg_box = self.get_alarm_info(self.df_summary_last, df_summary_cur)

        # Step 8: update cache data
        self.df_summary_last = df_summary_cur

        return msg_box

    def set_dtypes(self, df: pd.DataFrame) -> pd.DataFrame:
        """Set dtypes to int from str"""
        df = df.fillna(0)
        col_type_mapping = {k: int for k in DATA_MAPPING.keys()}
        df = df.astype(col_type_mapping)
        return df

    def try_reset_hist_data(self, df: pd.DataFrame) -> None:
        """Each daty reset the flash counter"""
        cur_data_batch_time = df['ccu_time'].max()
        if self.prev_data_batch_time is None:
            self.prev_data_batch_time = cur_data_batch_time
            return
        cur_date = datetime.fromtimestamp(cur_data_batch_time).date()
        prec_date = datetime.fromtimestamp(self.prev_data_batch_time).date()

        # reset in certain condition
        if cur_date != prec_date:
            self.df_summary_last = pd.DataFrame()

        # update status
        self.prev_data_batch_time = cur_data_batch_time

    @staticmethod
    def count_hop_times(df: pd.DataFrame) -> pd.DataFrame:
        '''Caculating how many flash's happended
        Needs 'bn' columns
        Adds 'cnt' column indicate flash_cnt
        '''
        # add bn
        df = add_block_no(df, stat_col='DoorOpenSignalFeedback')
        sql = """
        with tmp as (
        select line,train_no,coach_no,door_no,bn,max(ccu_time) as ccu_time
        from df
        where DoorOpenSignalFeedback = 1
        group by line,train_no,coach_no,door_no,bn
        having count(1)<=5)

        select line,train_no,coach_no,door_no,max(ccu_time) as ccu_time,
        count(distinct bn) as cnt
        from tmp
        group by line,train_no,coach_no,door_no
        """
        df_res = sqldf(sql, locals())
        return df_res

    def merge_summary_df(self, df_hist: pd.DataFrame, df_batch: pd.DataFrame) -> pd.DataFrame:
        '''Update data_summary with current data batch'''
        if df_hist.empty:
            return df_batch

        sql = """
        with tmp as
        (select line,train_no,coach_no,door_no,cnt,ccu_time
        from df_hist
        union all
        select line,train_no,coach_no,door_no,cnt,ccu_time
        from df_batch)
        select line,train_no,coach_no,door_no,sum(cnt) as cnt,
        max(ccu_time) as ccu_time
        from tmp
        group by line,train_no,coach_no,door_no
        """
        df_res = sqldf(sql, locals())
        return df_res

    def get_alarm_info(self, df_prev: pd.DataFrame, df_cur: pd.DataFrame) -> List[Dict]:
        """Gen alarm info """
        threshold = self.threshold['max_count']

        # case 1: if history is empty
        sql_empty = f"""
        select 1 as error_key,
        line, train_no,coach_no,door_no, ccu_time
        from df_cur 
        where cnt>={threshold}
        """
        if df_prev.empty:
            df_res = sqldf(sql_empty, locals())
            return df_res.to_dict('records')

        # case 2: if history is not empty
        sql = f"""
        select
        1 as error_key,
        df_cur.line, df_cur.train_no, df_cur.coach_no, df_cur.door_no, df_cur.cnt,
        df_cur.ccu_time
        from df_cur
        left join df_prev on df_cur.line = df_prev.line
        and df_cur.train_no = df_prev.train_no
        and df_cur.coach_no = df_prev.coach_no
        and df_cur.door_no = df_prev.door_no
        where df_cur.cnt>={threshold} and df_prev.cnt <{threshold}
        """
        df_res = sqldf(sql, locals())
        return df_res.to_dict('records')


def main_test():
    local_df_paths = ['./ZB_M0027_DoorOpenSignalAbnormal/sample_df_modify00.xlsx',
                      './ZB_M0027_DoorOpenSignalAbnormal/sample_df_modify01.xlsx',
                      './ZB_M0027_DoorOpenSignalAbnormal/sample_df_modify02.xlsx'
                      ]
    local_save_res_path = './ZB_M0027_DoorOpenSignalAbnormal/sample_result.xlsx'

    my_model = Model()
    my_model.threshold = {'max_count': 5}
    return my_model._test_core_logic(local_df_paths, local_save_res_path)


if __name__ == "__main__":
    # local_df_paths=[r'./ZB_M0008_ParkingCylinderPressure/sample_df.xlsx']
    mymodel = Model()
    mymodel.run()
