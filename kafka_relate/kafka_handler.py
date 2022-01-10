import json
from typing import Dict, Iterable
from kafka import KafkaConsumer,KafkaProducer

# kafka_filename = "kafka_config.json"
kafka_filename = "kafka_config_test.json"
with open(kafka_filename,'r',encoding='utf-8') as f:
    KAFKA = json.load(f)


def send_msg_to_kafka(alarm_msg:str,KakfaInfo:Dict = KAFKA)  -> None:
    '''
    @description : 发送报警信息到kafka

    @param : {*->(注释，类型，样例)}

    @return : {}

    '''        

    producer = KafkaProducer(bootstrap_servers=KakfaInfo['producer_ip'],
                                #sasl_plain_password =KakfaInfo['password'],
                                # api_version = tuple(KakfaInfo['api_version']),
                                )
    feature = producer.send(KakfaInfo['producer_topic'],alarm_msg.encode())
    result = feature.get(timeout=1)
    producer.close()

def get_msg_from_kafka() -> Iterable:
    kafka_conn = KafkaConsumer(KAFKA['comsumer_topic'],
                                group_id =KAFKA['comsumer_group'],
                                bootstrap_servers = KAFKA['comsumer_ip'],
                                auto_offset_reset = KAFKA['consumer_pos'],
                                # api_version = tuple(KAFKA['api_version']),
                                )    

    for msg_value in kafka_conn:
        msg_value = msg_value.value.decode()
        yield msg_value

if __name__ == "__main__":
    print("Done")