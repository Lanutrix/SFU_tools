from lms_sfu.models.event import Event
from lms_sfu.utils import href_id

SKIP_COURSE_NAMES = {"Военная подготовка"}


def parse_events(data: dict) -> list[Event]:
    embedded = data.get("_embedded", {})

    courses = {
        item["id"]: item
        for item in embedded.get("course-unit-realizations", [])
    }
    rooms = {
        item["id"]: item
        for item in embedded.get("rooms", [])
    }
    persons = {
        item["id"]: item
        for item in embedded.get("persons", [])
    }

    room_by_event: dict[str, str] = {}
    for item in embedded.get("event-rooms", []):
        event_id = href_id(item["_links"]["event"]["href"])
        room_id = href_id(item["_links"]["room"]["href"])
        room_by_event[event_id] = room_id

    teacher_by_event: dict[str, str] = {}
    for item in embedded.get("event-attendees", []):
        if item.get("roleId") != "TEACH":
            continue
        event_id = href_id(item["_links"]["event"]["href"])
        person_id = href_id(item["_links"]["person"]["href"])
        teacher_by_event[event_id] = person_id

    result: list[Event] = []

    for item in embedded.get("events", []):
        event_id = item["id"]
        course_id = href_id(item["_links"]["course-unit-realization"]["href"])
        course = courses.get(course_id)

        name = course["name"] if course else item["name"]
        if name in SKIP_COURSE_NAMES:
            continue

        room_id = room_by_event.get(event_id)
        room = rooms.get(room_id) if room_id else None
        location = room["name"] if room else ""

        person_id = teacher_by_event.get(event_id)
        person = persons.get(person_id) if person_id else None
        teacher = person["fullName"] if person else ""

        result.append(
            Event(
                name=name,
                start=item["start"],
                end=item["end"],
                location=location,
                teacher=teacher,
                type=item["typeId"],
            )
        )

    return result


def format_events(events: list[Event]) -> str:
    lines: list[str] = []
    for event in events:
        lines.extend(
            [
                f"Name: {event.name}",
                f"Start: {event.start}",
                f"End: {event.end}",
                f"Location: {event.location}",
                f"Teacher: {event.teacher}",
                f"Type: {event.type}",
                "-" * 40,
            ]
        )
    return "\n".join(lines)
