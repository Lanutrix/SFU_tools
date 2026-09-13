from lms_sfu.modeus.client import ModeusClient
from lms_sfu.modeus.people import search_people
from lms_sfu.modeus.schedule import get_schedule, get_schedule_raw

__all__ = [
    "ModeusClient",
    "get_schedule",
    "get_schedule_raw",
    "search_people",
]
