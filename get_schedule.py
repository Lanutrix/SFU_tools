from config import ATTENDEE_PERSON_ID, TOKEN

import requests
from datetime import datetime

import auth_data
import Events

def get_schedule(start_date: str, end_date: str, attendee_person_id: str = ATTENDEE_PERSON_ID):
    json_data = {
        'size': 5000,
        'timeMin': f'{start_date}T21:00:00Z',
        'timeMax': f'{end_date}T21:00:00Z',
        'attendeePersonId': [
            attendee_person_id,
        ],
    }
    response = requests.post(
        'https://sfedu.modeus.org/schedule-calendar-v2/api/calendar/events/search?tz=Europe/Moscow',
        #cookies=cookies,
        headers=auth_data.get_headers_modeus(TOKEN),
        json=json_data,
    )
    if response.status_code != 200:
        raise Exception(f"Failed to get schedule: {response.status_code}")
    return response.json()

schedule = get_schedule('2026-09-13', '2026-09-20')
Events.nice_print_events(Events.parse_events(schedule))