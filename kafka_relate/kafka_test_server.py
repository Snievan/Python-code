from kafka import KafkaConsumer, KafkaProducer


KAFKA_CONSUMER_CONN_CONF = {
    'topics': ['NLCJ-data2'],
    'configs': {'group_id': 'TK0109-test6666',
                'auto_offset_reset': 'earliest',
                'bootstrap_servers': ['192.168.1.151:6667']}
}

KAFKA_PRODUCER_CONN_CONF = {
    'configs': {'bootstrap_servers': ['192.168.1.151:6667']
                },
    'topic': 'NLCJ-alarminfo'
}

_topics = KAFKA_PRODUCER_CONN_CONF['topic']
_configs_consumer = KAFKA_CONSUMER_CONN_CONF['configs']
consumer = KafkaConsumer(_topics, **_configs_consumer)

print(consumer.topics())


for msg in consumer:
    msg_encoded = msg.value.decode()
    print(msg_encoded)