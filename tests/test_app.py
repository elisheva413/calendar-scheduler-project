# """
# Unit tests for Comp calendar scheduler
# """
# import pytest


# def test_find_available_slots():
#     """Test finding available time slots"""
#     assert True

import unittest
from datetime import time, timedelta

# Import the models and service from our app
from io_comp.models.person import Person
from io_comp.models.event import Event
from io_comp.models.time_slot import TimeSlot
from io_comp.services.calendar_service import CalendarService

class TestCalendarService(unittest.TestCase):
    """Unit tests for the CalendarService business logic."""

    def setUp(self):
        """Set up dummy data before each test runs."""
        # Create Alice and her events
        self.alice = Person("Alice")
        self.alice.add_event(Event("Morning meeting", TimeSlot(time(8, 0), time(9, 30))))
        self.alice.add_event(Event("Lunch with Jack", TimeSlot(time(13, 0), time(14, 0))))
        self.alice.add_event(Event("Yoga", TimeSlot(time(16, 0), time(17, 0))))

        # Create Jack and his events
        self.jack = Person("Jack")
        self.jack.add_event(Event("Morning meeting", TimeSlot(time(8, 0), time(8, 50))))
        self.jack.add_event(Event("Sales call", TimeSlot(time(9, 0), time(9, 40))))
        self.jack.add_event(Event("Lunch with Alice", TimeSlot(time(13, 0), time(14, 0))))
        self.jack.add_event(Event("Yoga", TimeSlot(time(16, 0), time(17, 0))))

        # Create Bob who has no events for the day
        self.bob = Person("Bob")

        # Initialize the service with our mock data (no need to read from CSV for unit tests)
        people_list = [self.alice, self.jack, self.bob]
        self.service = CalendarService(people_list)

    def test_find_available_slots_success(self):
        """Test finding a 60-minute slot for Alice and Jack (matches the README example)."""
        duration = timedelta(minutes=60)
        result = self.service.find_available_slots(["Alice", "Jack"], duration)
        
        expected_slots = [time(7, 0), time(9, 40), time(14, 0), time(17, 0)]
        self.assertEqual(result, expected_slots)

    def test_no_available_slots_due_to_duration(self):
        """Test when the requested duration is too long and no slots are available."""
        # Request a 10-hour meeting!
        duration = timedelta(hours=10) 
        result = self.service.find_available_slots(["Alice"], duration)
        
        # We expect an empty list because Alice doesn't have a 10-hour gap
        self.assertEqual(result, [])

    def test_person_with_no_events(self):
        """Test availability for a person with a completely free calendar."""
        # Request a full 12-hour day meeting (07:00 to 19:00)
        duration = timedelta(hours=12)
        result = self.service.find_available_slots(["Bob"], duration)
        
        # Bob should be available right from the start of the day
        self.assertEqual(result, [time(7, 0)])

if __name__ == '__main__':
    unittest.main()
