import os
import sys
import pandas as pd
import docx
from doc_helper import gen_modified_doc, replace_str
from folder_maker import mkfolder

VALUE_CUR_LIST = ['ZB_M0027', 'DoorOpenSignalAbnormal', '开门输入信号异常诊断模型']

FRAME_DOC_PATHS = ['docs\\ZB_M0027_开门输入信号异常诊断模型\\1-文档\\ZB_M0027_开门输入信号异常诊断模型测试报告.docx',
                   'docs\\ZB_M0027_开门输入信号异常诊断模型\\1-文档\\ZB_M0027_开门输入信号异常诊断模型设计说明书.docx',
                   'docs\\ZB_M0027_开门输入信号异常诊断模型\\1-文档\\ZB_M0027_开门输入信号异常诊断模型部署说明.docx',
                   'docs\\ZB_M0027_开门输入信号异常诊断模型\\1-文档\\ZB_M0027_开门输入信号异常诊断模型需求规格说明书.docx']

df = pd.read_excel('./model_summary1103.xlsx')
cols = ['模型编号f', '模型名称英文f', '模型名称']

df_select = df[cols][:6]


# loop through read file
for i, row in df_select.iterrows():
    print('[STATR WORK ON THIS]')
    print(row.values)
    model_code, model_enname, model_cnname = row.values
    pairs = list(zip(VALUE_CUR_LIST, row.values))
    folder_name = model_code + '_' + model_cnname

    # crete folder
    create_folder_name = os.path.join('docs', folder_name)
    write_file_folder = os.path.join('docs', folder_name, '1-文档')
    mkfolder(create_folder_name)

    for path in FRAME_DOC_PATHS:
        # read frame file
        doc = docx.Document(path)
        filename_raw = os.path.basename(path)
        filename_gen = replace_str(filename_raw, pairs)
        write_file_path = os.path.join(write_file_folder, filename_gen)
        gen_modified_doc(path, write_file_path, pairs)
