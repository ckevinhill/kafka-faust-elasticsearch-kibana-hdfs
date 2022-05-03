import argparse
import json
import multiprocessing
import random
import time
from datetime import datetime

from kafka import KafkaProducer

prog = "Kafka Event Generator"
desc = "run specified number of threads to create events"
parser = argparse.ArgumentParser(prog=prog, description=desc)
parser.add_argument("--thread-count", "-tc", default=1, type=int)
parser.add_argument("--event-count", "-ec", default=4, type=int)

valid_deviceids = [f"dev_{x}" for x in range(1, 20)]
valid_types = [f"type_{x}" for x in range(1, 10)]
valid_status = ["info", "warning", "error"]


class Event:
    """Event class for application events."""

    def __init__(self, deviceid, timestamp, event_type, event_status) -> None:
        self.deviceid = deviceid
        self.timestamp = timestamp
        self.event_type = event_type
        self.event_status = event_status

    def to_dict(self):
        """Returns dictionary representation of Event"""
        return {
            "deviceid": self.deviceid,
            "timestamp": self.timestamp,
            "event_type": self.event_type,
            "event_status": self.event_status,
        }

    def to_json(self) -> str:
        """Returns JSON string representation of Event"""
        return json.dumps(self.to_dict())


def send_event(producer: KafkaProducer):
    """Send one event."""
    time.sleep(random.choice(range(1, 20)))

    deviceid = random.choice(valid_deviceids)
    event_status = random.choice(valid_status)
    event_type = random.choice(valid_types)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    event = Event(
        deviceid=deviceid,
        timestamp=ts,
        event_type=event_type,
        event_status=event_status,
    )

    print("Sending: " + event.to_json())
    producer.send("raw_events", value=event.to_json())


def send_events(thread_id, event_cnt):
    """Send events function used by worker."""

    producer = KafkaProducer(
        bootstrap_servers=["localhost:9092"],
        value_serializer=lambda x: x.encode("utf-8"),
    )

    for i in range(event_cnt):
        send_event(producer)

    pass


if __name__ == "__main__":

    parsed_args = parser.parse_args()
    thread_count = parsed_args.thread_count
    event_count = parsed_args.event_count
    events_per_thread = int(event_count / thread_count)

    with multiprocessing.Manager() as manager:
        jobs = []

        for thread_id in range(thread_count):
            t = multiprocessing.Process(
                target=send_events,
                args=(thread_id, events_per_thread),
            )
            jobs.append(t)
            t.start()

        for curr_job in jobs:
            curr_job.join()

        print("Process Completed")
