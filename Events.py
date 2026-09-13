from dataclasses import dataclass


@dataclass
class Event:
    name: str
    start: str
    end: str
    location: str
    teacher: str
    type: str


def get_id(href: str) -> str:
    """'/123-456' -> '123-456'"""
    return href.rsplit("/", 1)[-1]


def parse_events(data: dict) -> list[Event]:
    # -------------------------
    # Индексы для быстрого поиска
    # -------------------------

    data = data.get('_embedded', {})
    
    courses = {
        item["id"]: item
        for item in data.get("course-unit-realizations", [])
    }

    rooms = {
        item["id"]: item
        for item in data.get("rooms", [])
    }

    persons = {
        item["id"]: item
        for item in data.get("persons", [])
    }

    # event_id -> room_id
    room_by_event = {}

    for item in data.get("event-rooms", []):
        event_id = get_id(item["_links"]["event"]["href"])
        room_id = get_id(item["_links"]["room"]["href"])

        room_by_event[event_id] = room_id

    # event_id -> person_id
    teacher_by_event = {}

    for item in data.get("event-attendees", []):
        if item.get("roleId") != "TEACH":
            continue

        event_id = get_id(item["_links"]["event"]["href"])
        person_id = get_id(item["_links"]["person"]["href"])

        teacher_by_event[event_id] = person_id

    # -------------------------
    # Собираем Event
    # -------------------------

    result = []

    for item in data.get("events", []):
        event_id = item["id"]

        # Предмет
        course_id = get_id(
            item["_links"]["course-unit-realization"]["href"]
        )

        course = courses.get(course_id)

        name = course["name"] if course else item["name"]
        if name == "Военная подготовка":
            continue

        # Аудитория
        room_id = room_by_event.get(event_id)
        room = rooms.get(room_id)

        location = room["name"] if room else ""

        # Преподаватель
        person_id = teacher_by_event.get(event_id)
        person = persons.get(person_id)

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

def nice_print_events(events: list[Event]):
    for event in events:
        print(f"Name: {event.name}")
        print(f"Start: {event.start}")
        print(f"End: {event.end}")
        print(f"Location: {event.location}")
        print(f"Teacher: {event.teacher}")
        print(f"Type: {event.type}")
        print("-" * 40)