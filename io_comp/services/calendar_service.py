from typing import List, Dict
from datetime import time, timedelta, datetime, date

# Import our models
from io_comp.models.person import Person
from io_comp.models.time_slot import TimeSlot

# Custom exceptions for domain-specific errors
class CalendarError(Exception):
    """Base exception for calendar domain errors."""
    pass

class InvalidDurationError(CalendarError):
    """Raised when the requested meeting duration is invalid (e.g., zero or negative)."""
    pass

class CalendarService:
    """Service handling the core business logic of the calendar."""
    
    # Workday hours are now configurable via parameters instead of being hardcoded
    def __init__(self, people: List[Person], workday_start: time = time(7, 0), workday_end: time = time(19, 0)):
        # Convert the list of people to a dictionary for easy lookup by name
        self.people_dict: Dict[str, Person] = {person.name: person for person in people}
        
        # Set configurable working hours
        self.workday_start = workday_start
        self.workday_end = workday_end
        
        # A dummy date to help us perform mathematical operations on times
        self._dummy_date = date.today()

    def _to_datetime(self, t: time) -> datetime:
        """Helper method to convert 'time' to 'datetime' for time math."""
        return datetime.combine(self._dummy_date, t)

    def find_available_slots(self, person_list: List[str], event_duration: timedelta) -> List[time]:
        """
        Finds all available starting times where ALL requested persons 
        are available for the given duration.
        """
        # Validate the requested duration using our custom exception
        if event_duration.total_seconds() <= 0:
            raise InvalidDurationError("Meeting duration must be greater than zero.")

        # 1. Collect all events of the requested persons
        all_slots: List[TimeSlot] = []
        for name in person_list:
            person = self.people_dict.get(name)
            if person:
                for event in person.events:
                    all_slots.append(event.time_slot)
        
        # 2. Sort all events by start time
        all_slots.sort(key=lambda slot: slot.start_time)
        
        # 3. Merge overlapping events (to create continuous blocks of busy time)
        merged_slots: List[TimeSlot] = []
        if all_slots:
            current_start = all_slots[0].start_time
            current_end = all_slots[0].end_time
            
            for slot in all_slots[1:]:
                # If there is an overlap or the event starts exactly when the previous one ends
                if slot.start_time <= current_end:
                    if slot.end_time > current_end:
                        current_end = slot.end_time
                else:
                    # No overlap - save the busy block and start a new one
                    merged_slots.append(TimeSlot(current_start, current_end))
                    current_start = slot.start_time
                    current_end = slot.end_time
            
            merged_slots.append(TimeSlot(current_start, current_end))
            
        # 4. Find the gaps (available time) between the busy blocks
        available_start_times: List[time] = []
        current_time_dt = self._to_datetime(self.workday_start)
        end_of_day_dt = self._to_datetime(self.workday_end)
        
        for slot in merged_slots:
            slot_start_dt = self._to_datetime(slot.start_time)
            slot_end_dt = self._to_datetime(slot.end_time)
            
            # Check if there is enough time from the current moment until the start of the next busy block
            if slot_start_dt - current_time_dt >= event_duration:
                available_start_times.append(current_time_dt.time())
            
            # Advance the current time to the end of the busy block (if it's later)
            if slot_end_dt > current_time_dt:
                current_time_dt = slot_end_dt
                
        # 5. Check the remaining gap from the last event until the end of the workday
        if end_of_day_dt - current_time_dt >= event_duration:
            available_start_times.append(current_time_dt.time())
            
        return available_start_times