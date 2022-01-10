from kafka import KafkaConsumer, KafkaProducer
import json

import logging 
# logging.basicConfig(level=logging.DEBUG)

KAFKA_CONSUMER_CONN_CONF = {
    'topics': ['NLCJ-data'],
    'configs': {'group_id': 'TK0109-test6692',
                'auto_offset_reset': 'earliest',
                'bootstrap_servers': ['192.168.1.151:6667']}
}

KAFKA_PRODUCER_CONN_CONF = {
    'configs': {'bootstrap_servers': ['192.168.1.151:6667']
                },
    'topic': 'NLCJ-alarminfo'
}

producer = KafkaProducer(**KAFKA_PRODUCER_CONN_CONF['configs'])

consumer = KafkaConsumer('NLCJ-data',**KAFKA_CONSUMER_CONN_CONF['configs'])

# print(data)
for msg in consumer:
    # msg = f"batch10 data no of {i}"
    msg_decoded = msg.value.decode()
    print(msg_decoded)


# for i in range(10):
#     msg = f"new_data no of {i}"
#     producer.send(KAFKA_PRODUCER_CONN_CONF['topic'],msg.encode())

# print('done')