import faust


class Event(faust.Record):

    deviceid: str
    timestamp: str
    event_type: int
    event_status: str


app = faust.App("event_processing_app", broker="kafka://localhost:9092")
raw_events = app.topic("raw_events", value_type=Event)
processed_events = app.topic("processed_events", value_type=Event)

flagged_status_types = ["warning", "error"]


@app.agent(raw_events, sink=[processed_events])
async def event(events):
    async for event in events:
        print(f"Processing type: {event.event_type}, status: {event.event_status}")
        if event.event_status in flagged_status_types:
            print("Sinking event to processed_events.")
            yield event


if __name__ == "__main__":
    app.main()
