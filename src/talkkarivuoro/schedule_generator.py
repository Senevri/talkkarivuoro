from datetime import datetime, timedelta
from ics import Calendar, Event
from pprint import pprint


def generate_schedule(
    time_step=timedelta(weeks=12),
    start_date=datetime(2023, 10, 9),
    num_turns=4,
    event_name="Talkkarivuoro",
):
    pprint((time_step, start_date, num_turns))

    # Create an iCalendar object
    cal = Calendar()

    # Calculate and add events to the calendar
    for turn in range(num_turns):
        end_date = start_date + timedelta(days=6)  # Assuming a one-week period for each turn

        print(
            f"Turn {turn + 1}: {start_date.strftime('%d-%m-%Y')} to {end_date.strftime('%d-%m-%Y')}"
        )

        event = Event()
        event.name = event_name
        event.begin = start_date
        event.end = end_date

        cal.events.add(event)

        # Add 12 weeks to the start date for the next turn
        start_date += time_step

    return cal


if __name__ == "__main__":
    cal = generate_schedule()
    # Save the calendar to an .ics file
    filename = "yard_maintenance_schedule"
    with open(f"{filename}.ics", "w") as f:
        f.writelines(cal.serialize_iter())

    print(f"Schedule saved to {filename}.ics")
