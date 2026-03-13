# Calendar Meeting Scheduler

This is a simple Python project that finds available meeting times for a group of people based on their schedules.

## 🧠 How it works (The Algorithm)
To solve the problem efficiently, I used an "Interval Merging" approach:
1. **Collect:** Get all the events for the requested people.
2. **Sort:** Sort the events by their start time.
3. **Merge:** If any events overlap, merge them into one big block of "busy time".
4. **Find Gaps:** Go through the workday (07:00 to 19:00) and find the free time gaps between the busy blocks that fit the requested meeting duration.

### Time Complexity
Let **n** be the number of events.

- Sorting the events: `O(n log n)`
- Merging overlapping intervals: `O(n)`
- Finding available gaps: `O(n)`

Overall complexity: **O(n log n)**.

## 🏗️ Project Structure
I organized the code using basic Object-Oriented Programming (OOP) to keep it clean and easy to read:
* `models/` - Simple classes representing our data (`Person`, `Event`, `TimeSlot`).
* `repositories/` - Responsible only for reading the CSV file (`CsvRepository`).
* `services/` - Contains the core logic and algorithm (`CalendarService`).
* `app.py` - The main file that connects everything and runs the program.

## 🚀 How to Run
I used only Python's built-in libraries, so there is no need to install anything extra (like Pandas).
Just open your terminal, make sure you are in the `python-project` folder, and run:

```bash
python -m io_comp.app
```

## 🧪 Tests
The project includes unit tests written using Python's built-in unittest module.
Instead of reading from the CSV file during tests, I used mock data in memory to make sure we are only testing the algorithm's logic.

To run the tests:

```bash
python -m unittest tests.test_app
```
