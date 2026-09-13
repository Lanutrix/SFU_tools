import requests

import auth_data
from config import TOKEN

import person_data


def search_people(name: str, last_name: str = '', year: str = '', speciality: str = '', size: int = 3000) -> list[person_data.Person]:
    full_name = ''
    if last_name == '':
        full_name = f'{name}*'
    else:
        full_name = f'{last_name}* {name}'

    json_data = {
        'fullName': full_name,
        'sort': '+fullName',
        'size': size
    }

    response = requests.post(
        'https://sfedu.modeus.org/schedule-calendar-v2/api/people/persons/search',
        headers=auth_data.get_headers_modeus(TOKEN),
        json=json_data,
    )
    if response.status_code != 200:
        raise Exception(f"Failed to search people: {response.status_code}")
    persons = person_data.parse_persons(response.json())

    if speciality != '':
        persons = [person for person in persons if person.специальность is not None and (speciality in person.специальность)]
    if year != '':
        year_int = int(year)
        persons = [person for person in persons if person.год_поступления == year_int]
    
    return persons

people = search_people(
    name='Валерия',
    last_name='',
    year=2024,
    speciality='без'
)
person_data.nice_print_persons(people)