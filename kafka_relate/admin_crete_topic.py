from kafka import KafkaAdminClient
from kafka.admin import NewTopic

topic_list = [NewTopic(name='NLCJ-data4',num_partitions=1,replication_factor=1)]
AdminClient =  KafkaAdminClient(bootstrap_servers = ['192.168.1.151:6667'])

AdminClient.create_topics(new_topics=topic_list)
AdminClient.close()
print("Done create")