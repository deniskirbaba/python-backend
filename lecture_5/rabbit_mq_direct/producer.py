import pika
from concurrent.futures import ThreadPoolExecutor, wait


def produce_many(producer_name: str):
    params = pika.ConnectionParameters(
        host= "localhost",
        credentials=pika.PlainCredentials(
            username="admin",
            password="adminpass"
        )
    )

    connection = pika.BlockingConnection(parameters=params)
    channel = connection.channel()

    for i in range(1_000_000):
        channel.basic_publish(
            exchange="",
            routing_key="hello",
            body=f"{producer_name}: {i}"
        )

    connection.close()


with ThreadPoolExecutor() as e:
    futures = [e.submit(produce_many, f"PRODUCER: {i}") for i in range(10)]
    wait(futures)

    print("completed")
    