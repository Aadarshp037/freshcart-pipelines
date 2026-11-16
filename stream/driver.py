
import pika
import json
import sys

EXCHANGE = "rapido-dispatch"


def main():
    if len(sys.argv) != 3:
        print('Usage: python driver.py NAME "PATTERN"')
        return

    name = sys.argv[1]
    pattern = sys.argv[2]

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost")
    )

    channel = connection.channel()

    channel.exchange_declare(
        exchange=EXCHANGE,
        exchange_type="topic",
        durable=True
    )

    result = channel.queue_declare(
        queue="",
        exclusive=True
    )

    queue_name = result.method.queue

    channel.queue_bind(
        exchange=EXCHANGE,
        queue=queue_name,
        routing_key=pattern
    )

    channel.basic_qos(prefetch_count=1)

    print(f"{name} listening on pattern: {pattern}")

    def callback(ch, method, properties, body):
        try:
            message = json.loads(body)

            if not message.get("zone"):
                print(
                    f"{name} | NACK | Missing zone | "
                    f"{method.routing_key}"
                )
                ch.basic_nack(
                    delivery_tag=method.delivery_tag,
                    requeue=False
                )
                return

            print(
                f"{name} | ACK | {method.routing_key} | {message}"
            )

            ch.basic_ack(
                delivery_tag=method.delivery_tag
            )

        except (json.JSONDecodeError, TypeError):
            print(f"{name} | NACK | Invalid JSON")

            ch.basic_nack(
                delivery_tag=method.delivery_tag,
                requeue=False
            )

    channel.basic_consume(
        queue=queue_name,
        on_message_callback=callback,
        auto_ack=False
    )

    try:
        channel.start_consuming()

    except KeyboardInterrupt:
        print(f"\nStopping {name}")
        channel.stop_consuming()

    finally:
        connection.close()


if __name__ == "__main__":
    main()
