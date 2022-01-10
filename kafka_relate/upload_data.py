from kafka import KafkaConsumer, KafkaProducer
import json

KAFKA_CONSUMER_CONN_CONF = {
    'topics': ['NLCJ-data'],
    'configs': {'group_id': 'TK0109-test6666',
                'auto_offset_reset': 'earliest',
                'bootstrap_servers': ['192.168.1.151:6667']}
}

KAFKA_PRODUCER_CONN_CONF = {
    'configs': {'bootstrap_servers': ['192.168.1.151:6667']
                },
    'topic': 'NLCJ-alarminfo'
}

producer = KafkaProducer(**KAFKA_PRODUCER_CONN_CONF['configs'])

file_name = 'kafka_test_env_set\datatest1.json'

with open(file_name,'r',encoding='utf-8') as f :
    data = json.load(f)

# print(data)
for row in data:
    # msg = f"batch10 data no of {i}"
    producer.send('NLCJ-data',row.encode())
    print(f"sent msg {row}")
producer.flush()
producer.close()
print('done')


# for i in range(10):
#     msg = f"new_data no of {i}"
#     producer.send(KAFKA_PRODUCER_CONN_CONF['topic'],msg.encode())

# print('done')