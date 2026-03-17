from dataclasses import dataclass
from io_comp.models.time_slot import TimeSlot

@dataclass(frozen=True)
class Event:
    """Represents a calendar event with a subject and a specific time slot."""
    subject: str
    time_slot: TimeSlot