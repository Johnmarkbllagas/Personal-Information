import tkinter as tk
from tkinter import messagebox
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('personal_info.db')
cursor = conn.cursor()

# Create the PersonalInformation table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS PersonalInformation (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    age INTEGER,
                    gender TEXT
                )''')
conn.commit()

def submit():
    name = name_entry.get()
    age = age_entry.get()
    gender = gender_var.get()

    if not name:
        messagebox.showwarning("ERROR", "ENTER YOUR NAME")
        return

    if not age:
        messagebox.showwarning("ERROR", "ENTER YOUR AGE")
        return

    gender_str = "Male" if gender == 1 else "Female"

    # Insert the data into the database
    cursor.execute("INSERT INTO PersonalInformation (name, age, gender) VALUES (?, ?, ?)", (name, age, gender_str))
    conn.commit()

    messagebox.showinfo("Result", "Record added successfully")
    refresh_listbox()

def delete_selected():
    # Get the index of the selected item in the listbox
    selected_index = listbox.curselection()

    if selected_index:
        # Get the text of the selected item
        selected_item = listbox.get(selected_index)
        # Extract the name from the text
        name = selected_item.split(':')[1].strip()

        # Delete the selected item from the database
        cursor.execute("DELETE FROM PersonalInformation WHERE name=?", (name,))
        conn.commit()

        # Refresh the listbox to reflect the changes
        refresh_listbox()

def refresh_listbox():
    # Clear the existing items in the listbox
    listbox.delete(0, tk.END)

    # Retrieve data from the database and populate the listbox
    cursor.execute("SELECT name, age, gender FROM PersonalInformation")
    rows = cursor.fetchall()
    for row in rows:
        listbox.insert(tk.END, f"Name: {row[0]}, Age: {row[1]}, Gender: {row[2]}")

# Create the main application window
app = tk.Tk()
app.title("Personal Information Manager")

# Name entry
name_label = tk.Label(app, text="Enter Your Name:")
name_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

name_entry = tk.Entry(app)
name_entry.grid(row=0, column=1, padx=10, pady=5)

# Age entry
age_label = tk.Label(app, text="Enter Your Age:")
age_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)

age_entry = tk.Entry(app)
age_entry.grid(row=1, column=1, padx=10, pady=5)

# Gender selection
gender_label = tk.Label(app, text="Select Your Gender:")
gender_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)

gender_var = tk.IntVar(value=0)
male_radio = tk.Radiobutton(app, text="Male", variable=gender_var, value=1)
male_radio.grid(row=2, column=1, padx=10, pady=5)

female_radio = tk.Radiobutton(app, text="Female", variable=gender_var, value=2)
female_radio.grid(row=2, column=2, padx=10, pady=5)

# Submit button
submit_button = tk.Button(app, text="Add Record", command=submit)
submit_button.grid(row=3, column=1, columnspan=5, padx=10, pady=5)

# Delete selected button
delete_button = tk.Button(app, text="Delete Selected", command=delete_selected)
delete_button.grid(row=4, column=1, columnspan=5, padx=10, pady=5)

# Listbox to display existing data
listbox = tk.Listbox(app)
listbox.grid(row=5, column=0, columnspan=3, padx=10, pady=5)
refresh_listbox()

app.mainloop()

# Close the database connection when the application exits
conn.close()
