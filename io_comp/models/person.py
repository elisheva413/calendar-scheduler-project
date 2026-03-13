from dataclasses import dataclass, field
from typing import List
from io_comp.models.event import Event

@dataclass
class Person:
    """Represents a person and their scheduled events."""
    name: str
    events: List[Event] = field(default_factory=list)

    def add_event(self, event: Event) -> None:
        """Adds a new event to the person's calendar."""
        self.events.append(event)