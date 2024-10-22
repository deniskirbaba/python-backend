import pika

params = pika.ConnectionParameters(
    host= "localhost",
    credentials=pika.PlainCredentials(
        username="admin",
        password="adminpass"
    )
)

connection = pika.BlockingConnection(parameters=params)
channel = connection.channel()

channel.queue_declare(queue="hello")


def callback(ch, method, properties, body):
    print(f"CONSUMER: Received {body}")


channel.basic_consume(
    queue="hello",
    on_message_callback=callback,
    auto_ack=True
)

print("CONSUMER: waiting for messages")
channel.start_consuming()
