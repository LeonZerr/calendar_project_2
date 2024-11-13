# calendar_project_2
**What is it?** </br>
A simple calendar application built with Python and Tkinter that allows users to manage their calendar events, including birthdays, meetings, and events. This program connects to a PostgreSQL database to store, retrieve, update, and delete entries.

Features

    Display Current Month: Shows the calendar for the current month.
    Display Current Year: Displays all months of the current year.
    Add Entries: Users can add birthdays, meetings, and events to the calendar.
    View Entries: Search and display specific entries by name/description.
    Delete Entries: Users can delete existing entries from the calendar.
    Update Entries: Change the date of an existing event, meeting, or birthday.
    View All Entries: Show all entries of a specific type (birthday, event, or meeting).

Requirements

    Python 3.x
    Tkinter for the GUI
    PostgreSQL for database management
    psycopg2 library for connecting to PostgreSQL
    python-dotenv to load environment variables

How to Use

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



