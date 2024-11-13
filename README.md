# calendar_project_2
**What is it?** </br>
A simple calendar application built with Python and Tkinter that allows users to manage their calendar events, including birthdays, meetings, and events. This program connects to a PostgreSQL database to store, retrieve, update, and delete entries.


Requirements

    Python 3
    Tkinter for the GUI
    PostgreSQL for database management
    psycopg2 library for connecting to PostgreSQL
    python-dotenv to load environment variables

Once the program is running, the Tkinter interface provides the following options:

    Show Current Month: Display the calendar of the current month.
    Show Current Year: Display the full year’s calendar.
    Add Entry: Add a new entry (Birthday, Event, or Meeting) to the calendar.
    Show Entry: Search for a specific entry by name or description.
    Delete Entry: Delete an entry from the calendar.
    Change Entry: Update the date of an existing entry.
    Show All Entries: View all entries of a specific type (Birthday, Event, or Meeting).
    Exit: Exit the application.

Example Workflow:

    To add a birthday, select 'b' for Birthday, enter a name (e.g., "John's Birthday"), and provide a date (e.g., "2024-05-15").
    To view a birthday, select 'b' and enter the name you want to search for.
    To delete a meeting, select 'm' for Meeting, provide the name of the meeting, and click the "Delete Entry" button.
    To view all events, select 'e' for Event and click the "Show All Entries" button.



