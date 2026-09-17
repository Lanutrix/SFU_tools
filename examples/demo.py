"""CLI-примеры для локальной проверки API."""

from datetime import datetime, timedelta

from lms_sfu import config
from lms_sfu.modeus import get_schedule, search_people
from lms_sfu.moodle import mark_lesson, parse_attendance_url
from lms_sfu.parsers import format_events, format_persons


def demo_schedule() -> None:
    start = datetime.now().strftime("%Y-%m-%d")
    end = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    events = get_schedule(start, end)
    print(format_events(events))


def demo_people() -> None:
    people = search_people(name="Дмитрий", year=2024, specialty="системы")
    print(format_persons(people))


def _print_mark_result(result) -> None:
    print(f"status: {result.status_code}")
    print(f"final_url: {result.final_url}")
    if result.redirects:
        print("redirects:")
        for step in result.redirects:
            print(f"  {step}")
    print(f"body[:100]: {result.body_preview!r}")
    if result.error:
        print(f"error: {result.error}")
    print("ok" if result.ok else "failed")


def demo_attendance(source: str | None = None) -> None:
    if not config.MOODLE_SESSION:
        raise ValueError("MOODLE_SESSION is not set")

    if source is None:
        source = input("Вставь ссылку attendance: ").strip()

    try:
        qrpass, sessid = parse_attendance_url(source)
    except ValueError as exc:
        print(f"Ошибка: {exc}")
        raise SystemExit(1) from exc

    print(f"qrpass={qrpass!r} sessid={sessid!r}")
    result = mark_lesson(config.MOODLE_SESSION, qrpass, sessid)
    _print_mark_result(result)


if __name__ == "__main__":
    import sys

    command = sys.argv[1] if len(sys.argv) > 1 else "schedule"
    if command == "schedule":
        demo_schedule()
    elif command == "people":
        demo_people()
    elif command == "attendance":
        link = sys.argv[2] if len(sys.argv) > 2 else None
        demo_attendance(link)
    else:
        print(
            "Usage: python -m examples.demo "
            "[schedule|people|attendance [url]]"
        )
        raise SystemExit(1)
