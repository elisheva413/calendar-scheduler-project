import os
import logging
from datetime import timedelta

# Import the layers we built
from io_comp.repositories.csv_repository import CsvRepository
from io_comp.services.calendar_service import CalendarService

# Configure the logging system
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting Calendar App...")

    # 1. Define the path to the data file (relative to the project folder)
    csv_path = os.path.join("resources", "calendar.csv")

    # 2. Initialize the Repository and load data
    repository = CsvRepository(csv_path)
    try:
        people_list = repository.load_data()
        logger.info(f"Successfully loaded data from {csv_path}")
    except FileNotFoundError:
        logger.error(f"Could not find the file at {csv_path}")
        logger.error("Please make sure you are running the script from the 'python-project' folder.")
        return

    # 3. Initialize the Service (Dependency Injection)
    calendar_service = CalendarService(people_list)

    # 4. Define the requirements according to the README example
    persons_to_meet = ["Alice", "Jack"]
    meeting_duration = timedelta(minutes=60)

    logger.info(f"Looking for a 60-minute slot for: {', '.join(persons_to_meet)}")
    logger.info("-" * 40)

    # 5. Execute the core algorithm
    available_slots = calendar_service.find_available_slots(persons_to_meet, meeting_duration)

    # 6. Log the results in the requested format
    if not available_slots:
        logger.info("No available slots found.")
    else:
        for start_time in available_slots:
            logger.info(f"Starting Time of available slots: {start_time.strftime('%H:%M')}")
            
    logger.info("Finished successfully!")

if __name__ == "__main__":
    main()