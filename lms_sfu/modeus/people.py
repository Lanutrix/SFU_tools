from lms_sfu.modeus.client import ModeusClient
from lms_sfu.models.person import Person
from lms_sfu.parsers.persons import parse_persons


def search_people(
    name: str,
    last_name: str = "",
    year: int | str | None = None,
    specialty: str = "",
    size: int = 3000,
    client: ModeusClient | None = None,
) -> list[Person]:
    client = client or ModeusClient()

    if last_name:
        full_name = f"{last_name}* {name}"
    else:
        full_name = f"{name}*"

    data = client.post(
        "/schedule-calendar-v2/api/people/persons/search",
        json={
            "fullName": full_name,
            "sort": "+fullName",
            "size": size,
        },
    )
    persons = parse_persons(data)

    if specialty:
        persons = [
            person
            for person in persons
            if person.specialty is not None and specialty in person.specialty
        ]

    if year is not None and year != "":
        year_int = int(year)
        persons = [
            person for person in persons if person.admission_year == year_int
        ]

    return persons
