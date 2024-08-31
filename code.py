import tkinter as tk
from tkinter import messagebox, simpledialog
from calendar import monthrange, month_name
from datetime import datetime

def create_curved_rectangle(canvas, x1, y1, x2, y2, radius=20, **kwargs):
    points = [x1 + radius, y1,
              x1 + radius, y1,
              x2 - radius, y1,
              x2 - radius, y1,
              x2, y1,
              x2, y1 + radius,
              x2, y1 + radius,
              x2, y2 - radius,
              x2, y2 - radius,
              x2, y2,
              x2 - radius, y2,
              x2 - radius, y2,
              x1 + radius, y2,
              x1 + radius, y2,
              x1, y2,
              x1, y2 - radius,
              x1, y2 - radius,
              x1, y1 + radius,
              x1, y1 + radius,
              x1, y1]
    return canvas.create_polygon(points, **kwargs, smooth=True)

def update_calendar():
    for widget in calendar_frame.winfo_children():
        widget.destroy()

    month_days = monthrange(current_year, current_month)[1]
    start_day = datetime(current_year, current_month, 1).weekday()

    month_label.config(text=f"{month_name[current_month]} {current_year}")

    day_names = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    for day_name in day_names:
        tk.Label(calendar_frame, text=day_name, bg='lightgray', font=('Arial', 10, 'bold'), padx=20, pady=10).grid(row=0, column=day_names.index(day_name), sticky='nsew')

    for day in range(1, month_days + 1):
        day_canvas = tk.Canvas(calendar_frame, width=60, height=60, bg='lightblue', highlightthickness=0)
        day_canvas.grid(row=(start_day + day) // 7 + 1, column=(start_day + day) % 7, sticky='nsew')
        create_curved_rectangle(day_canvas, 5, 5, 55, 55, radius=20, fill='white', outline='black')
        day_canvas.create_text(30, 30, text=str(day), font=('Arial', 10))

        if current_year == datetime.now().year and current_month == datetime.now().month and day == datetime.now().day:
            create_curved_rectangle(day_canvas, 5, 5, 55, 55, radius=20, fill='lightblue', outline='blue')

        day_canvas.bind("<Button-1>", lambda e, d=day: select_day(d))

    for i in range(7):
        calendar_frame.grid_columnconfigure(i, weight=1)
    calendar_frame.grid_rowconfigure(0, weight=1)

def select_day(day):
    global selected_day
    selected_day = day
    reminder_date.set(f"{selected_day:02d}/{current_month:02d}/{current_year}")

def add_reminder():
    if selected_day is None:
        messagebox.showwarning("No Day Selected", "Please select a day first.")
        return
    
    reminder_text = reminder_title.get()
    reminder_time_text = reminder_time.get()
    reminder_date_text = reminder_date.get()

    if reminder_text and reminder_time_text:
        reminders[f"{current_year}-{current_month:02d}-{selected_day:02d}"] = f"{reminder_text} at {reminder_time_text}"
        reminder_listbox.insert(tk.END, f"{reminder_date_text} - {reminder_text} at {reminder_time_text}")
        messagebox.showinfo("Reminder Added", "Reminder has been added.")
        clear_reminder_fields()
    else:
        messagebox.showwarning("Incomplete Information", "Please enter both a title and a time for the reminder.")

def clear_reminder_fields():
    reminder_title.delete(0, tk.END)
    reminder_time.delete(0, tk.END)
    reminder_date.set("")

def prev_month():
    global current_year, current_month
    if current_month == 1:
        current_month = 12
        current_year -= 1
    else:
        current_month -= 1
    update_calendar()

def next_month():
    global current_year, current_month
    if current_month == 12:
        current_month = 1
        current_year += 1
    else:
        current_month += 1
    update_calendar()

root = tk.Tk()
root.title("Calendar and Reminder App")

selected_day = None
current_year = datetime.now().year
current_month = datetime.now().month
reminders = {}

canvas = tk.Canvas(root, borderwidth=0, background="#ffffff")
scroll_frame = tk.Frame(canvas, bg='lightblue')
vsb = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=vsb.set)

vsb.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)
canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

scroll_frame.bind("<Configure>", lambda event, canvas=canvas: canvas.configure(scrollregion=canvas.bbox("all")))

def _on_mouse_wheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

canvas.bind_all("<MouseWheel>", _on_mouse_wheel)

calendar_frame = tk.Frame(scroll_frame, bg='lightblue')
calendar_frame.pack(padx=10, pady=10, fill='both', expand=True)

nav_frame = tk.Frame(scroll_frame, bg='lightblue')
nav_frame.pack(padx=10, pady=10, fill='x')

prev_button = tk.Button(nav_frame, text="<", command=prev_month, font=('Arial', 12, 'bold'), bg='lightgray', relief='raised')
prev_button.grid(row=0, column=0)

month_label = tk.Label(nav_frame, text="", font=("Arial", 16, 'bold'), bg='lightblue')
month_label.grid(row=0, column=1)

next_button = tk.Button(nav_frame, text=">", command=next_month, font=('Arial', 12, 'bold'), bg='lightgray', relief='raised')
next_button.grid(row=0, column=2)

reminder_frame = tk.Frame(scroll_frame, bg='lightblue')
reminder_frame.pack(padx=10, pady=5, fill='x')

tk.Label(reminder_frame, text="Title:", bg='lightblue', font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky='e', pady=2)
reminder_title = tk.Entry(reminder_frame, font=('Arial', 10))
reminder_title.grid(row=0, column=1, pady=2, padx=5)

tk.Label(reminder_frame, text="Date:", bg='lightblue', font=('Arial', 10, 'bold')).grid(row=1, column=0, sticky='e', pady=2)
reminder_date = tk.StringVar()
reminder_date_entry = tk.Entry(reminder_frame, textvariable=reminder_date, font=('Arial', 10), state='readonly')
reminder_date_entry.grid(row=1, column=1, pady=2, padx=5)

tk.Label(reminder_frame, text="Time:", bg='lightblue', font=('Arial', 10, 'bold')).grid(row=2, column=0, sticky='e', pady=2)
reminder_time = tk.Entry(reminder_frame, font=('Arial', 10))
reminder_time.grid(row=2, column=1, pady=2, padx=5)

add_reminder_button = tk.Button(reminder_frame, text="Add Reminder", command=add_reminder, font=('Arial', 10, 'bold'), bg='lightgreen', relief='raised')
add_reminder_button.grid(row=3, column=0, columnspan=2, pady=5)

reminder_listbox = tk.Listbox(scroll_frame, font=('Arial', 10), bg='white')
reminder_listbox.pack(padx=10, pady=5, fill='both', expand=True)

update_calendar()
root.mainloop()
