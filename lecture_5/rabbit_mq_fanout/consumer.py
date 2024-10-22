import sys

import pika

queue = sys.argv[1]

parameters = pika.ConnectionParameters(
    host="localhost",
    credentials=pika.PlainCredentials(
        username="admin",
        password="adminpass",
    ),
)
connection = pika.BlockingConnection(parameters=parameters)
channel = connection.channel()

channel.queue_declare(queue=queue)
channel.queue_bind(
    queue=queue,
    exchange="test.fanout",
)


def callback(ch, method, properties, body):
    print(f"CONSUMER[{queue}]: Received\n{ch}\n{method}\n{properties}\n{body}")


channel.basic_consume(
    queue=queue,
    on_message_callback=callback,
    auto_ack=True,
)

print("CONSUMER: Waiting for messages")
channel.start_consuming()