import calendar
import datetime
from tkinter import Tk, Label, Button, Entry, StringVar, Text, messagebox
import psycopg2
from dotenv import load_dotenv
import os


#DB connection properties
load_dotenv() 
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")


#Global variables
year = datetime.datetime.now().year
month = datetime.datetime.now().month


#Functions to connect to the DB and to access/modify the data
def connect_db():
    '''Establish a connection to the PostgreSQL database.'''
    conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_password, host=db_host, port=db_port)
    return conn


def create_tables():
    '''Creates the tables if they do not exist.'''
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS birthdays (
        name VARCHAR(255) PRIMARY KEY,
        date DATE
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS events (
        name VARCHAR(255) PRIMARY KEY,
        date DATE
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS meetings (
        name VARCHAR(255) PRIMARY KEY,
        date DATE
    );
    """)

    conn.commit()
    cursor.close()
    conn.close()


def load_entries():
    '''Loads entries from the database.'''
    conn = connect_db()
    cursor = conn.cursor()
    entries = {
        "birthdays": {},
        "events": {},
        "meetings": {}
    }

    cursor.execute("SELECT name, date FROM birthdays;")#birthdays
    for row in cursor.fetchall():
        entries["birthdays"][row[0]] = row[1]

    cursor.execute("SELECT name, date FROM events;")#events
    for row in cursor.fetchall():
        entries["events"][row[0]] = row[1]

    cursor.execute("SELECT name, date FROM meetings;")#meetings
    for row in cursor.fetchall():
        entries["meetings"][row[0]] = row[1]

    cursor.close()
    conn.close()
    return entries


def save_entry(data):
    '''Saves entries to the database.'''
    conn = connect_db()
    cursor = conn.cursor()
    
    #birthdays
    for name, date in data["birthdays"].items():
        cursor.execute("INSERT INTO birthdays (name, date) VALUES (%s, %s) ON CONFLICT (name) DO UPDATE SET date = excluded.date;", (name, date))

    #events
    for name, date in data["events"].items():
        cursor.execute("INSERT INTO events (name, date) VALUES (%s, %s) ON CONFLICT (name) DO UPDATE SET date = excluded.date;", (name, date))

    #meetings
    for name, date in data["meetings"].items():
        cursor.execute("INSERT INTO meetings (name, date) VALUES (%s, %s) ON CONFLICT (name) DO UPDATE SET date = excluded.date;", (name, date))

    conn.commit()
    cursor.close()
    conn.close()


def add_entry(data, entry_type, name_or_description, date):
    '''Adds a new entry to the database.'''
    if entry_type == 'b':
        data["birthdays"][name_or_description] = date
    elif entry_type == 'm':
        data["meetings"][name_or_description] = date
    elif entry_type == 'e':
        data["events"][name_or_description] = date
    save_entry(data)


def get_entry(data, entry_type, name_or_description):
    '''Searches for a specific entry in the database.'''
    conn = connect_db()
    cursor = conn.cursor()
    result = None
    
    if entry_type == 'b':
        cursor.execute("SELECT * FROM birthdays WHERE name = %s;", (name_or_description,))
        result = cursor.fetchone()
    elif entry_type == 'm':
        cursor.execute("SELECT * FROM meetings WHERE name = %s;", (name_or_description,))
        result = cursor.fetchone()
    elif entry_type == 'e':
        cursor.execute("SELECT * FROM events WHERE name = %s;", (name_or_description,))
        result = cursor.fetchone()

    cursor.close()
    conn.close()
    
    if result:
        return result[0], result[1]  #(name_or_description, date)
    else:
        return None, None  #if entry not found


def delete_entry(data, entry_type, name_or_description):
    '''Deletes an entry from the database.'''
    conn = connect_db()
    cursor = conn.cursor()
    
    if entry_type == 'b':
        cursor.execute("DELETE FROM birthdays WHERE name = %s;", (name_or_description,))
    elif entry_type == 'm':
        cursor.execute("DELETE FROM meetings WHERE name = %s;", (name_or_description,))
    elif entry_type == 'e':
        cursor.execute("DELETE FROM events WHERE name = %s;", (name_or_description,))
    
    conn.commit()
    cursor.close()
    conn.close()

    #Update the local data in the dictionary
    if entry_type == 'b':
        if name_or_description in data["birthdays"]:
            del data["birthdays"][name_or_description]
    elif entry_type == 'm':
        if name_or_description in data["meetings"]:
            del data["meetings"][name_or_description]
    elif entry_type == 'e':
        if name_or_description in data["events"]:
            del data["events"][name_or_description]
    
    save_entry(data)  #Save changes in the database


def change_entry(data, entry_type, name_or_description, new_date):
    '''Changes the date of an entry in the database.'''
    try:
        datetime.datetime.strptime(new_date, "%Y-%m-%d")  #Check if date format is correct
    except ValueError:
        raise ValueError("Invalid date format. Please use YYYY-MM-DD.")
    
    conn = connect_db()
    cursor = conn.cursor()
    
    if entry_type == 'b':
        cursor.execute("UPDATE birthdays SET date = %s WHERE name = %s;", (new_date, name_or_description))
    elif entry_type == 'm':
        cursor.execute("UPDATE meetings SET date = %s WHERE name = %s;", (new_date, name_or_description))
    elif entry_type == 'e':
        cursor.execute("UPDATE events SET date = %s WHERE name = %s;", (new_date, name_or_description))
    
    conn.commit()
    cursor.close()
    conn.close()

    if entry_type == 'b':
        if name_or_description in data["birthdays"]:
            data["birthdays"][name_or_description] = new_date
    elif entry_type == 'm':
        if name_or_description in data["meetings"]:
            data["meetings"][name_or_description] = new_date
    elif entry_type == 'e':
        if name_or_description in data["events"]:
            data["events"][name_or_description] = new_date
    
    save_entry(data)  


def show_all(data, entry_type):
    '''Lists all entries (as tuples) of a specific type from the database.'''
    conn = connect_db()
    cursor = conn.cursor()

    if entry_type == 'b':
        cursor.execute("SELECT * FROM birthdays;")
    elif entry_type == 'm':
        cursor.execute("SELECT * FROM meetings;")
    elif entry_type == 'e':
        cursor.execute("SELECT * FROM events;")

    entries = cursor.fetchall()
    cursor.close()
    conn.close()

    return entries  

