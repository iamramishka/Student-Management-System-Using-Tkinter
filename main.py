import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import sqlite3

#Copyright © 2024 Ramishka Madhushan
#Project Link :- https://github.com/ramishka98/Student-Management-System-Using-Tkinter

def create_connection():
    """ Create a database connection to the SQLite database """
    return sqlite3.connect('student_management_system.db')

def create_table():
    """ Create the students table if it doesn't exist """
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            roll_number TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            grade TEXT,
            section TEXT,
            gender TEXT,
            birth_date TEXT,
            attendance INTEGER
        );
    ''')
    conn.commit()
    conn.close()

def add_student(student):
    """ Add a new student to the students table """
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO students(roll_number, name, grade, section, gender, birth_date, attendance)
            VALUES(?,?,?,?,?,?,?)
        ''', (student[0], student[1], student[2], student[3], student[4], student[5], student[6]))
        conn.commit()
        student_table.insert("", "end", values=student)
        messagebox.showinfo("Add Record", "Record added successfully!")
        clear_entries()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Roll No already exists.")
    finally:
        conn.close()

def update_student(student):
    """ Update a student in the students table """
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            UPDATE students SET name=?, grade=?, section=?, gender=?, birth_date=?, attendance=?
            WHERE roll_number=?
        ''', (student[1], student[2], student[3], student[4], student[5], student[6], student[0]))
        conn.commit()
        messagebox.showinfo("Update Record", "Record updated successfully!")
    finally:
        conn.close()

def delete_student(roll_number):
    """ Delete a student by Roll No """
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM students WHERE roll_number=?', (roll_number,))
    conn.commit()
    conn.close()

def search_student():
    """ Search and display students by Roll No """
    roll_number = search_entry.get()
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students WHERE roll_number=?', (roll_number,))
    rows = cursor.fetchall()
    student_table.delete(*student_table.get_children())  # Clear existing entries in the Treeview
    if rows:
        for row in rows:
            student_table.insert('', 'end', values=row)
        messagebox.showinfo("Search Result", "Student(s) found.")
    else:
        messagebox.showinfo("Search Result", "No student found with Roll No: " + roll_number)
    conn.close()

def add_record():
    student = [entry.get() for entry in entries]
    add_student(student)

def update_selected():
    selected = student_table.selection()
    if selected:
        new_values = [entry.get() for entry in entries]
        student_table.item(selected[0], values=new_values)
        update_student(new_values)
        clear_entries()

def delete_selected():
    selected = student_table.selection()
    if selected:
        roll_number = student_table.item(selected[0], 'values')[0]
        delete_student(roll_number)
        student_table.delete(selected[0])
        messagebox.showinfo("Delete Record", "Record deleted successfully!")

def clear_entries():
    for entry in entries:
        entry.delete(0, tk.END)
    messagebox.showinfo("Clear Entries", "All entries cleared!")

# Setup the database table
create_table()

win = tk.Tk()
win.geometry("1350x700+0+0")
win.title("Student Management System")
win.config(bg="lightgray")

style = ttk.Style()
style.theme_use("default")
style.configure("Treeview", background="white", foreground="black", rowheight=25, fieldbackground='white')
style.map("Treeview", background=[("selected", "darkred")])

title_label = tk.Label(win, text="Student Management System", font=("Arial", 20, "bold"), bg="teal", foreground="white")
title_label.pack(side=tk.TOP, fill=tk.X)

detail_frame = tk.LabelFrame(win, text="Student Records", font=("Arial", 14), bg="lightgray", foreground="black")
detail_frame.place(x=40, y=90, width=420, height=570)

search_label = tk.Label(detail_frame, text="Search by Roll No:", font=("Arial", 16), bg="lightgray", foreground="black")
search_label.place(x=20, y=10)
search_entry = tk.Entry(detail_frame, bd=1, font=("Arial", 16), bg="white", foreground="black")
search_entry.place(x=20, y=50, width=250, height=30)
search_button = tk.Button(detail_frame, text="Search", bg="teal", foreground="white", font=("Arial", 13), command=search_student)
search_button.place(x=280, y=50, width=100, height=30)

data_frame = tk.Frame(win, bg="teal", relief=tk.GROOVE)
data_frame.place(x=490, y=98, width=830, height=565)

labels = ["Roll No", "Name", "Grade", "Section", "Gender", "BOD", "Attendance"]
entries = []
y_pos = 90
for i, label in enumerate(labels):
    lab = tk.Label(detail_frame, text=label + ":", font=("Arial", 16), bg="lightgray", foreground="black")
    lab.place(x=20, y=y_pos + 50 * i)
    if label == "Gender":
        ent = ttk.Combobox(detail_frame, font=("Arial", 16), values=("Male", "Female", "Other"))
    elif label == "BOD":
        ent = DateEntry(detail_frame, width=24, background='darkblue', foreground='white', borderwidth=2)
    else:
        ent = tk.Entry(detail_frame, bd=1, font=("Arial", 16), bg="white", foreground="black")
    ent.place(x=110, y=y_pos + 50 * i, width=250, height=30)
    entries.append(ent)

main_frame = tk.Frame(data_frame, bg="teal", bd=2, relief=tk.GROOVE)
main_frame.pack(fill=tk.BOTH, expand=True)
Y_Scroll = tk.Scrollbar(main_frame, orient=tk.VERTICAL)
X_Scroll = tk.Scrollbar(main_frame, orient=tk.HORIZONTAL)
student_table = ttk.Treeview(main_frame, columns=tuple(labels), yscrollcommand=Y_Scroll.set, xscrollcommand=X_Scroll.set)
Y_Scroll.config(command=student_table.yview)
X_Scroll.config(command=student_table.xview)
Y_Scroll.pack(side=tk.RIGHT, fill=tk.Y)
X_Scroll.pack(side=tk.BOTTOM, fill=tk.X)
for col in student_table["columns"]:
    student_table.heading(col, text=col)
    student_table.column(col, width=100)
student_table["show"] = "headings"
student_table.pack(fill=tk.BOTH, expand=True)

btn_frame = tk.Frame(detail_frame, bg="lightgray", bd=0, relief=tk.GROOVE)
btn_frame.place(x=20, y=430, width=380, height=100)
button_specs = [
    ("Add", add_record), ("Update", update_selected),
    ("Delete", delete_selected), ("Clear", clear_entries)
]
for index, (text, command) in enumerate(button_specs):
    button = tk.Button(btn_frame, text=text, bg="teal", foreground="white", font=("Arial", 13), command=command)
    button.grid(row=index // 2, column=index % 2, padx=10, pady=10, sticky="ew")
    btn_frame.grid_columnconfigure(index % 2, weight=1)

win.mainloop()
