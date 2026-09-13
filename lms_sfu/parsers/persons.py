from typing import Optional

from lms_sfu.models.person import Person


def get_actual_student(students: list[dict]) -> Optional[dict]:
    """
    Выбирает актуальную запись студента.

    Приоритет:
    1. Запись, где learningEndDate == None
    2. Если таких несколько — самая новая по learningStartDate
    3. Если активных нет — самая новая запись вообще
    """
    if not students:
        return None

    active_students = [
        student
        for student in students
        if student.get("learningEndDate") is None
    ]
    candidates = active_students if active_students else students

    return max(
        candidates,
        key=lambda student: student.get("learningStartDate") or "",
    )


def parse_persons(data: dict) -> list[Person]:
    """
    Парсит ответ API в список Person.

    Поддерживает оба варианта структуры: с `_embedded` и без.
    """
    embedded = data.get("_embedded", data)

    persons_data = embedded.get("persons", [])
    students_data = embedded.get("students", [])
    employees_data = embedded.get("employees", [])

    employees_by_person = {
        employee["personId"]
        for employee in employees_data
        if employee.get("personId")
    }

    students_by_person: dict[str, list[dict]] = {}
    for student in students_data:
        person_id = student.get("personId")
        if not person_id:
            continue
        students_by_person.setdefault(person_id, []).append(student)

    result: list[Person] = []

    for person_data in persons_data:
        person_id = person_data.get("id", "")
        person_students = students_by_person.get(person_id, [])
        student = get_actual_student(person_students)

        if person_id in employees_by_person:
            role = "преподаватель"
        elif person_students:
            role = "студент"
        else:
            role = ""

        if student:
            flow_code = student.get("flowCode") or ""
            year = int(flow_code[:4]) if flow_code[:4].isdigit() else None
            specialty_code = student.get("specialtyCode")
            specialty_name = student.get("specialtyName")
        else:
            year = None
            specialty_code = None
            specialty_name = None

        result.append(
            Person(
                attendee_person_id=person_id,
                last_name=person_data.get("lastName", ""),
                first_name=person_data.get("firstName", ""),
                middle_name=person_data.get("middleName", ""),
                admission_year=year,
                specialty_code=specialty_code,
                specialty=specialty_name,
                role=role,
            )
        )

    return result


def format_persons(persons: list[Person]) -> str:
    lines = [
        "=" * 40,
        f"Всего: {len(persons)}",
        "=" * 40,
    ]
    for person in persons:
        lines.extend(
            [
                f"attendee_person_id: {person.attendee_person_id}",
                f"Фамилия: {person.last_name}",
                f"Имя: {person.first_name}",
                f"Отчество: {person.middle_name}",
                f"Год поступления: {person.admission_year}",
                f"Специальность код: {person.specialty_code}",
                f"Специальность: {person.specialty}",
                f"Роль: {person.role}",
                "-" * 40,
            ]
        )
    return "\n".join(lines)
