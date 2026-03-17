from dataclasses import dataclass
from datetime import time

@dataclass(frozen=True)
class TimeSlot:
    """Represents a specific time range with a start and end time."""
    start_time: time
    end_time: time