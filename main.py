import calendar
import datetime
from tkinter import Tk, Label, Button, Entry, StringVar, Text, messagebox
from calendar_database import *  


#Global variables
year = datetime.datetime.now().year
month = datetime.datetime.now().month


create_tables() #Creates tables if necessary
data = load_entries() #loads data (entry's) from the DB


#Functions to call the different options inside the GUI.:
def show_current_month():
    '''Displays the current month in the output box.'''
    output_text.delete("1.0", "end")  #Clear output area before updating
    month_text = calendar.month(year, month) #Create current month as text
    output_text.insert("end", month_text)  #Insert and show current month


def show_current_year():
    '''Displays the current year month by month in the output box without month headers.'''
    output_text.delete("1.0", "end")  
    for month_num in range(1, 13):  #Loops through all months
        
        month_text = calendar.month(year, month_num) #Generate calendars
        
        output_text.insert("end", month_text + "\n\n") #Output / space between months

    output_text.yview("end") #Allows user to scroll through months


def add_entry_gui():
    '''Adds a new entry to the database from the GUI.'''
    entry_type = type_var.get() #Gets selected entry type
    name_or_description = name_or_description_entry.get() #Gets value from GUI and stores it as 'name_or_description'
    date = date_entry.get()

    if not entry_type or not name_or_description or not date:
        messagebox.showwarning("Warning", "Please fill in all fields.")
        return

    try:
        datetime.datetime.strptime(date, "%Y-%m-%d") #Validates date format  
        add_entry(data, entry_type, name_or_description, date) #Saves entry to DB
        messagebox.showinfo("Success", "Entry added!")
        output_text.delete("1.0", "end")
        output_text.insert("end", f"Entry '{name_or_description}' added successfully!\n")
    except ValueError:
        messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")


def display_entry_gui():
    '''Displays a specific entry from the database.'''
    entry_type = type_var.get()
    name_or_description = name_or_description_entry.get()
    name, date = get_entry(data, entry_type, name_or_description)

    output_text.delete("1.0", "end")
    if name and date:
        output_text.insert("end", f"{name} : {date}\n") #Displays entry
    else:
        output_text.insert("end", "Entry not found.\n")


def delete_entry_gui():
    '''Deletes a selected entry from the database.'''
    
    entry_type = type_var.get() 
    name_or_description = name_or_description_entry.get().strip()  

    #Check if required fields are filled
    if not entry_type or not name_or_description:
        messagebox.showwarning("Warning", "Please fill in the first two fields to delete an entry.")
        return
    
    delete_entry(data, entry_type, name_or_description) #Deletes entry

    messagebox.showinfo("Success", "Entry deleted!")
    output_text.delete("1.0", "end")
    output_text.insert("end", f"Entry '{name_or_description}' deleted successfully.\n")


def change_entry_gui():
    '''Changes the date for a specific entry in the database.'''
    entry_type = type_var.get()
    name_or_description = name_or_description_entry.get()
    new_date = date_entry.get()

    try:
        datetime.datetime.strptime(new_date, "%Y-%m-%d") 
        change_entry(data, entry_type, name_or_description, new_date)
        messagebox.showinfo("Success", "Entry updated!")
        output_text.delete("1.0", "end")
        output_text.insert("end", f"Entry '{name_or_description}' updated successfully!\n")
    except ValueError:
        messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")


def show_all_gui():
    '''Displays all entries of the selected type.'''
    entry_type = type_var.get()
    entries = show_all(data, entry_type)

    output_text.delete("1.0", "end")
    if entries:
        for entry in entries:
            output_text.insert("end", f"{entry[0]} : {entry[1]}\n") #Shows each entry
    else:
        output_text.insert("end", "No entries found.\n")


#Main GUI Window (TKinter)
root = Tk()
root.title("Calendar")
root.configure(bg='#2C2C2C')

#Labels (UI Elements)
#Entry Type
Label(root, text="Type (b=Birthday, e=Event, m=Meeting):",bg="#2C2C2C",fg="#B0BEC5").grid(row=0, column=0, padx=5, pady=5)
type_var = StringVar()
type_entry = Entry(root, textvariable=type_var)
type_entry.grid(row=0, column=1, padx=5, pady=5)

#Name or Description
Label(root, text="Name/Description:",bg="#2C2C2C",fg="#B0BEC5").grid(row=1, column=0, padx=5, pady=5)
name_or_description_entry = Entry(root)
name_or_description_entry.grid(row=1, column=1, padx=5, pady=5)

#Date
Label(root, text="Date (YYYY-MM-DD):",bg="#2C2C2C",fg="#B0BEC5").grid(row=2, column=0, padx=5, pady=5)
date_entry = Entry(root)
date_entry.grid(row=2, column=1, padx=5, pady=5)

#Buttons 
Button(root, text="Show Current Month", command=show_current_month,width=16,bg='#9C27B0',fg='#FFFFFF',font=("Helvetica", 12)).grid(row=3, column=0, columnspan=2, padx=5, pady=5)
Button(root, text="Show Current Year", command=show_current_year,width=16,bg='#64B5F6',fg='#FFFFFF',font=("Helvetica", 12)).grid(row=4, column=0, columnspan=2, padx=5, pady=5)
Button(root, text="Add Entry", command=add_entry_gui,width=16,bg='#00BFAE',fg='#FFFFFF',font=("Helvetica", 12)).grid(row=5, column=0, columnspan=2, padx=5, pady=5)
Button(root, text="Show Entry", command=display_entry_gui,width=16,bg='#2196F3',fg='#FFFFFF',font=("Helvetica", 12)).grid(row=6, column=0, columnspan=2, padx=5, pady=5)
Button(root, text="Delete Entry", command=delete_entry_gui,width=16,bg='#FF5252',fg='#FFFFFF',font=("Helvetica", 12)).grid(row=7, column=0, columnspan=2, padx=5, pady=5)
Button(root, text="Change Entry", command=change_entry_gui,width=16,bg='#FFB300',fg='#FFFFFF',font=("Helvetica", 12)).grid(row=8, column=0, columnspan=2, padx=5, pady=5)
Button(root, text="Show All Entries", command=show_all_gui,width=16,bg='#B0BEC5',fg='#FFFFFF',font=("Helvetica", 12)).grid(row=9, column=0, columnspan=2, padx=5, pady=5)
Button(root, text="Exit", command=root.quit,bg='#9E9E9E',fg='#FFFFFF',font=("Helvetica", 12)).grid(row=10, column=0, columnspan=2, padx=5, pady=5)

#Textbox
output_text = Text(root, height=10, width=40,bg='#F5F5F5',fg='#333333')
output_text.grid(row=11, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()
