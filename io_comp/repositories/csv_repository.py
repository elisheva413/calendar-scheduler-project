import csv
from datetime import datetime
from typing import List, Dict

# Import our models
from io_comp.models.person import Person
from io_comp.models.event import Event
from io_comp.models.time_slot import TimeSlot

class CsvRepository:
    """Repository responsible for loading calendar data from a CSV file."""
    
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load_data(self) -> List[Person]:
        """Reads the CSV and returns a list of Person objects with their events."""
        people_dict: Dict[str, Person] = {}

        # Open the file for reading
        with open(self.file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            
            for row in reader:
                # Ensure we have a valid row with 4 columns (name, subject, start, end)
                if not row or len(row) < 4:
                    continue
                
                name = row[0].strip()
                subject = row[1].strip()
                start_str = row[2].strip()
                end_str = row[3].strip()

                # Convert strings (e.g., "08:00") to time objects
                start_time = datetime.strptime(start_str, "%H:%M").time()
                end_time = datetime.strptime(end_str, "%H:%M").time()

                # Create our models
                time_slot = TimeSlot(start_time, end_time)
                event = Event(subject, time_slot)

                # If the person doesn't exist in our dictionary yet, create them
                if name not in people_dict:
                    people_dict[name] = Person(name)
                
                # Add the event to the respective person
                people_dict[name].add_event(event)

        # Return only the list of people (without the dictionary keys)
        return list(people_dict.values())