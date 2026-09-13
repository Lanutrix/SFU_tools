"""CLI-примеры для локальной проверки API."""

from datetime import datetime, timedelta

from lms_sfu.modeus import get_schedule, search_people
from lms_sfu.moodle import mark_lesson
from lms_sfu.parsers import format_events, format_persons
from lms_sfu import config


def demo_schedule() -> None:
    start = datetime.now().strftime("%Y-%m-%d")
    end = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    events = get_schedule(start, end)
    print(format_events(events))


def demo_people() -> None:
    people = search_people(name="Дмитрий", year=2024, specialty="системы")
    print(format_persons(people))


def demo_attendance(qrpass: str, sessid: str) -> None:
    if not config.MOODLE_SESSION:
        raise ValueError("MOODLE_SESSION is not set")
    ok = mark_lesson(config.MOODLE_SESSION, qrpass, sessid)
    print("ok" if ok else "failed")


if __name__ == "__main__":
    import sys

    command = sys.argv[1] if len(sys.argv) > 1 else "schedule"
    if command == "schedule":
        demo_schedule()
    elif command == "people":
        demo_people()
    elif command == "attendance":
        demo_attendance(sys.argv[2], sys.argv[3])
    else:
        print("Usage: python -m examples.demo [schedule|people|attendance qr sessid]")
        raise SystemExit(1)
