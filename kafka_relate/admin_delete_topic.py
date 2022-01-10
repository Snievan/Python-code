from kafka import KafkaAdminClient
from kafka.admin import NewTopic

topic_list = ['NLCJ-data2','NLCJ-data3','NLCJ-data4']
AdminClient =  KafkaAdminClient(bootstrap_servers = ['192.168.1.151:6667'])

AdminClient.delete_topics(topics=topic_list)
AdminClient.close()
print("Done Delete")