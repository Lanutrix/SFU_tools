from dataclasses import dataclass


@dataclass
class Event:
    name: str
    start: str
    end: str
    location: str
    teacher: str
    type: str
