# """
# This is the App entry point
# """
# import sys

# def main():
#     """Main entry point for the application"""
#     print("\n\n")
#     print("Your goal is to design and create a simple Calendar in Python. You can replace this main function with your own code.")
#     print("Please see README.md")
#     sys.exit(1)


# if __name__ == "__main__":
#     main()

import os
from datetime import timedelta

# Import the layers we built
from io_comp.repositories.csv_repository import CsvRepository
from io_comp.services.calendar_service import CalendarService

def main():
    print("Starting Calendar App...\n")

    # 1. Define the path to the data file (relative to the project folder)
    csv_path = os.path.join("resources", "calendar.csv")

    # 2. Initialize the Repository and load data
    repository = CsvRepository(csv_path)
    try:
        people_list = repository.load_data()
    except FileNotFoundError:
        print(f"Error: Could not find the file at {csv_path}")
        print("Please make sure you are running the script from the 'python-project' folder.")
        return

    # 3. Initialize the Service (Dependency Injection)
    calendar_service = CalendarService(people_list)

    # 4. Define the requirements according to the README example
    persons_to_meet = ["Alice", "Jack"]
    meeting_duration = timedelta(minutes=60)

    print(f"Looking for a 60-minute slot for: {', '.join(persons_to_meet)}")
    print("-" * 40)

    # 5. Execute the core algorithm
    available_slots = calendar_service.find_available_slots(persons_to_meet, meeting_duration)

    # 6. Print the results in the requested format
    if not available_slots:
        print("No available slots found.")
    else:
        for start_time in available_slots:
            print(f"Starting Time of available slots: {start_time.strftime('%H:%M')}")
            
    print("\nFinished successfully!")

if __name__ == "__main__":
    main()