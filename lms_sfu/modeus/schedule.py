from lms_sfu import config
from lms_sfu.modeus.client import ModeusClient
from lms_sfu.models.event import Event
from lms_sfu.parsers.events import parse_events


def get_schedule_raw(
    start_date: str,
    end_date: str,
    attendee_person_id: str | None = None,
    client: ModeusClient | None = None,
) -> dict:
    client = client or ModeusClient()
    person_id = attendee_person_id or config.ATTENDEE_PERSON_ID
    if not person_id:
        raise ValueError("ATTENDEE_PERSON_ID is not set")

    return client.post(
        "/schedule-calendar-v2/api/calendar/events/search?tz=Europe/Moscow",
        json={
            "size": 5000,
            "timeMin": f"{start_date}T21:00:00Z",
            "timeMax": f"{end_date}T21:00:00Z",
            "attendeePersonId": [person_id],
        },
    )


def get_schedule(
    start_date: str,
    end_date: str,
    attendee_person_id: str | None = None,
    client: ModeusClient | None = None,
) -> list[Event]:
    data = get_schedule_raw(start_date, end_date, attendee_person_id, client)
    return parse_events(data)
