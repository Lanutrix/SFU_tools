from dataclasses import dataclass
from typing import Optional


@dataclass
class Person:
    attendee_person_id: str
    фамилия: str
    имя: str
    отчество: str
    год_поступления: Optional[int] = None
    специальность_код: Optional[str] = None
    специальность: Optional[str] = None
    роль: str = ""


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
        key=lambda student: student.get("learningStartDate") or ""
    )


def parse_persons(data: dict) -> list[Person]:
    """
    Парсит ответ API в список Person.

    Поддерживает оба варианта структуры:

    {
        "persons": [...],
        "students": [...],
        "employees": [...]
    }

    и

    {
        "_embedded": {
            "persons": [...],
            "students": [...],
            "employees": [...]
        }
    }
    """

    # Если API вернул данные внутри _embedded,
    # работаем с ним. Иначе используем data напрямую.
    embedded = data.get("_embedded", data)

    persons_data = embedded.get("persons", [])
    students_data = embedded.get("students", [])
    employees_data = embedded.get("employees", [])

    # personId всех преподавателей
    employees_by_person = {
        employee["personId"]
        for employee in employees_data
        if employee.get("personId")
    }

    # Группируем ВСЕ записи студентов по personId
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

        # Выбираем актуальную запись студента
        student = get_actual_student(person_students)

        # Определяем роль
        if person_id in employees_by_person:
            role = "преподаватель"
        elif person_students:
            role = "студент"
        else:
            role = ""

        # Данные студента
        if student:
            # Год поступления — префикс flowCode, напр. "2025_Бакалавр_Специалист_ОФО"
            flow_code = student.get("flowCode") or ""
            try:
                year = int(flow_code[:4]) if flow_code[:4].isdigit() else None
            except (ValueError, TypeError):
                year = None

            specialty_code = student.get("specialtyCode")
            specialty_name = student.get("specialtyName")

        else:
            year = None
            specialty_code = None
            specialty_name = None

        result.append(
            Person(
                attendee_person_id=person_id,
                фамилия=person_data.get("lastName", ""),
                имя=person_data.get("firstName", ""),
                отчество=person_data.get("middleName", ""),
                год_поступления=year,
                специальность_код=specialty_code,
                специальность=specialty_name,
                роль=role,
            )
        )

    return result


def nice_print_persons(persons: list[Person]) -> None:
    print("=" * 40)
    print(f"Всего: {len(persons)}")
    print("=" * 40)
    for person in persons:
        print(f"attendee_person_id: {person.attendee_person_id}")
        print(f"Фамилия: {person.фамилия}")
        print(f"Имя: {person.имя}")
        print(f"Отчество: {person.отчество}")
        print(f"Год поступления: {person.год_поступления}")
        print(f"Специальность код: {person.специальность_код}")
        print(f"Специальность: {person.специальность}")
        print(f"Роль: {person.роль}")
        print("-" * 40)