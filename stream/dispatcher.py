
import pika
import json
import random
import time
import uuid
import argparse
from datetime import datetime, timezone

EXCHANGE = "rapido-dispatch"

ZONES = {
    "bangalore": ["koramangala", "indiranagar", "whitefield"],
    "chennai": ["tnagar", "adyar", "velachery"]
}

def connect():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost")
    )
    channel = connection.channel()
    channel.exchange_declare(
        exchange=EXCHANGE,
        exchange_type="topic",
        durable=True
    )
    return connection, channel

def publish(channel, city, zone, request_type, bad=False):
    routing_key = f"{city}.{zone}.{request_type}"

    message = {
        "id": str(uuid.uuid4())[:8],
        "city": city,
        "type": request_type,
        "ts": datetime.now(timezone.utc).isoformat()
    }

    if not bad:
        message["zone"] = zone

    channel.basic_publish(
        exchange=EXCHANGE,
        routing_key=routing_key,
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2,
            content_type="application/json"
        )
    )

    print(
        f"PUBLISHED | {routing_key} | "
        f"{message['id']} | {'BAD' if bad else 'GOOD'}"
    )

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--once-key")
    parser.add_argument("--duration", type=int, default=120)
    args = parser.parse_args()

    connection, channel = connect()

    try:
        if args.once_key:
            parts = args.once_key.split(".")
            if len(parts) != 3:
                raise ValueError("Routing key must have 3 words")
            publish(channel, parts[0], parts[1], parts[2])
            return

        count = 0
        start = time.time()

        while time.time() - start < args.duration:
            count += 1
            city = random.choice(list(ZONES.keys()))
            zone = random.choice(ZONES[city])
            request_type = random.choice(["ride", "food"])

            bad = count % 10 == 0
            publish(channel, city, zone, request_type, bad=bad)

            time.sleep(2)

    finally:
        connection.close()

if __name__ == "__main__":
    main()
