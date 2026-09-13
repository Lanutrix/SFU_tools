from dataclasses import dataclass
from typing import Optional


@dataclass
class Person:
    attendee_person_id: str
    last_name: str
    first_name: str
    middle_name: str
    admission_year: Optional[int] = None
    specialty_code: Optional[str] = None
    specialty: Optional[str] = None
    role: str = ""
