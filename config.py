import os

from dotenv import load_dotenv

load_dotenv()

ATTENDEE_PERSON_ID = os.getenv("ATTENDEE_PERSON_ID")
TOKEN = os.getenv("TOKEN")
MOODLE_SESSION = os.getenv("MOODLE_SESSION")
