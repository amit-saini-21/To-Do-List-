import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import json, os

# Initialize task lists to track entries, labels, status, and buttons
task_entries = []
task_labels = []
task_status = []
task_buttons = []
completed_labels = []
task_images = []
task_vars = []  # List to hold StringVar for each task

# Save tasks to JSON file
def save_tasks():
    # Force update all StringVars with the latest Entry text
    for i in range(len(task_entries)):
        task_vars[i].set(task_entries[i].get())
    tasks = []
    for i, var in enumerate(task_vars):
        task_text = var.get()
        completed = task_status[i]
        tasks.append({"text": task_text, "completed": completed})
    with open("tasks.json", "w") as f:
        json.dump(tasks, f)

# Load tasks from JSON file
def load_tasks():
    if os.path.exists("tasks.json"):
        with open("tasks.json", "r") as f:
            try:
                tasks = json.load(f)
            except json.JSONDecodeError:
                tasks = []
        for task in tasks:
            add_task(task_text=task.get("text", ""), completed=task.get("completed", False))

def delete_task(task_index):
    confirm = messagebox.askyesno("Delete Task", "Are you sure you want to delete this task?")
    if confirm:
        # Destroy the task elements
        task_entries[task_index].destroy()
        task_labels[task_index].destroy()
        task_buttons[task_index][0].destroy()  # Delete button
        task_buttons[task_index][1].destroy()  # Complete button

        # Destroy "Completed" label if it exists
        if completed_labels[task_index]:
            completed_labels[task_index].destroy()

        # Remove the task from lists
        del task_entries[task_index]
        del task_labels[task_index]
        del task_buttons[task_index]
        del task_status[task_index]
        del completed_labels[task_index]
        del task_vars[task_index]

        # Save current scroll position
        pos = canvas.yview()[0]
        
        # Rearrange remaining tasks
        for i in range(len(task_entries)):
            task_labels[i].config(text=f"{i + 1}.")
            canvas.create_window(20, 24 + i * 40, window=task_labels[i])
            canvas.create_window(280, 24 + i * 40, window=task_entries[i])
            canvas.create_window(720, 24 + i * 40, window=task_buttons[i][0])
            canvas.create_window(820, 24 + i * 40, window=task_buttons[i][1])
            
            # Update button commands for delete and complete buttons
            task_buttons[i][0].config(command=lambda idx=i: delete_task(idx))
            task_buttons[i][1].config(command=lambda idx=i: mark_task_complete(idx))
            
            # Reposition the "Completed" label for completed tasks
            if task_status[i] and completed_labels[i] is not None:
                canvas.create_window(600, 24 + i * 40, window=completed_labels[i])

        configure_canvas()
        # Restore previous scroll position
        canvas.yview_moveto(pos)
        save_tasks()  # Save changes

def configure_canvas():
    bbox = canvas.bbox("all")
    if bbox:
        x1, y1, x2, y2 = bbox
        content_height = y2 - y1
        canvas_height = 470  # as defined for canvas height
        if content_height < canvas_height:
            canvas.config(scrollregion=(x1, y1, x2, canvas_height))
        else:
            canvas.config(scrollregion=bbox)
    else:
        canvas.config(scrollregion=(0, 0, 900, 470))


def mark_task_complete(task_index):
    if 0 <= task_index < len(task_labels) and not task_status[task_index]:
        task_labels[task_index].config(fg="#7dec39")
        
        # Create "Completed" label for completed tasks
        completed_label = tk.Label(canvas, text="✅ Completed", font=("Arial", 12, "bold"), fg="#7dec39", bg="#0B0C10")
        completed_labels[task_index] = completed_label
        task_status[task_index] = True

        # Save current scroll position
        pos = canvas.yview()[0]
        
        canvas.create_window(600, 24 + task_index * 40, window=completed_label)
        configure_canvas()
        # Restore previous scroll position
        canvas.yview_moveto(pos)
        save_tasks()  # Save changes

def on_double_click(event):
    """Allow editing the task on double-click."""
    # Set the entry widget to normal (editable)
    event.widget.config(state="normal")

def add_task(task_text=None, completed=False):
    task_number = len(task_entries) + 1

    # Task number label
    task_label = tk.Label(canvas, text=f"{task_number}.", font=("Arial", 14, "bold"), bg="#0B0C10", fg="white")
    task_labels.append(task_label)
    task_status.append(False)

    # Create a StringVar for the task entry
    var = tk.StringVar()
    if task_text is not None:
        var.set(task_text)
    task_vars.append(var)

    # Task entry with textvariable
    new_task_entry = tk.Entry(canvas, font=("Algerian", 14, "bold"), fg="red", justify="center",
                              width=40, bg="#0B0C10", textvariable=var)
    task_entries.append(new_task_entry)

    # Agar task_text already maujood hai (loaded task), to usko readonly state mein set kar do
    if task_text is not None and task_text != "":
        new_task_entry.config(state="readonly", readonlybackground="#0B0C10")

    # Bind events: Enter & FocusOut will make the entry read-only; double-click will enable editing.
    new_task_entry.bind("<Return>", lambda event: make_entry_readonly(new_task_entry))
    new_task_entry.bind("<FocusOut>", lambda event: make_entry_readonly(new_task_entry))
    new_task_entry.bind("<Double-Button-1>", on_double_click)

    # Delete button
    delete_img_path = "trash1.png"
    delete_image = Image.open(delete_img_path)
    delete_photo = ImageTk.PhotoImage(delete_image)
    task_images.append(delete_photo)
    delete_button = tk.Button(canvas, image=delete_photo, bg="white", activebackground="#47c4de",
                              width=70, height=24, command=lambda idx=len(task_entries) - 1: delete_task(idx))
    
    # Complete button
    complete_img_path = "complete1.png"
    complete_image = Image.open(complete_img_path)
    complete_photo = ImageTk.PhotoImage(complete_image)
    task_images.append(complete_photo)
    complete_button = tk.Button(canvas, image=complete_photo, bg="white", activebackground="#47c4de",
                                width=70, height=24, command=lambda idx=len(task_entries) - 1: mark_task_complete(idx))
    
    # Add the task widgets to canvas using create_window for scrolling behavior
    canvas.create_window(20, 24 + (task_number - 1) * 40, window=task_label)
    canvas.create_window(280, 24 + (task_number - 1) * 40, window=new_task_entry)
    canvas.create_window(720, 24 + (task_number - 1) * 40, window=delete_button)
    canvas.create_window(820, 24 + (task_number - 1) * 40, window=complete_button)

    task_buttons.append([delete_button, complete_button])
    completed_labels.append(None)
    configure_canvas()

    # If loaded task was already completed, mark it complete
    if completed:
        mark_task_complete(len(task_entries) - 1)

    save_tasks()  # Save after adding a new task


def make_entry_readonly(entry):
    entry.config(state="readonly", readonlybackground="#0B0C10")
    save_tasks()  # Ensure latest text is saved when entry becomes read-only

def delete_all_tasks():
    confirm = messagebox.askyesno("Delete All Tasks", "Are you sure you want to delete all tasks?")
    if confirm:
        for entry in task_entries:
            entry.destroy()
        for label in task_labels:
            label.destroy()
        for buttons in task_buttons:
            buttons[0].destroy()
            buttons[1].destroy()
        for label in completed_labels:
            if label:
                label.destroy()
        task_entries.clear()
        task_labels.clear()
        task_buttons.clear()
        task_status.clear()
        completed_labels.clear()
        task_vars.clear()
        configure_canvas()
        save_tasks()

def show_tasks():
    show_window = tk.Toplevel(root)
    show_window.title("Show Tasks")
    show_window.geometry("400x300")
    
    label = tk.Label(show_window, text="Choose a task type to show:")
    label.pack(pady=10)

    choice = tk.StringVar()
    choice.set("all")

    tk.Radiobutton(show_window, text="All Tasks", variable=choice, value="all").pack()
    tk.Radiobutton(show_window, text="Completed Tasks", variable=choice, value="completed").pack()
    tk.Radiobutton(show_window, text="Incomplete Tasks", variable=choice, value="incomplete").pack()

    confirm_button = tk.Button(show_window, text="Show", command=lambda: display_selected_tasks(choice.get(), show_window))
    confirm_button.pack(pady=10)

def display_selected_tasks(option, show_window):
    result_window = tk.Toplevel(show_window)
    result_window.title("Tasks")
    result_window.geometry("400x400")

    if option == "all":
        tk.Label(result_window, text="All Tasks").pack(pady=10)
        for index, var in enumerate(task_vars):
            task_text = var.get()
            status = "Completed" if task_status[index] else "Incomplete"
            tk.Label(result_window, text=f"{index + 1}. {task_text} ({status})").pack(anchor="w")
    
    elif option == "completed":
        tk.Label(result_window, text="Completed Tasks").pack(pady=10)
        for index, var in enumerate(task_vars):
            if task_status[index]:
                tk.Label(result_window, text=f"{index + 1}. {var.get()}").pack(anchor="w")
    
    elif option == "incomplete":
        tk.Label(result_window, text="Incomplete Tasks").pack(pady=10)
        for index, var in enumerate(task_vars):
            if not task_status[index]:
                tk.Label(result_window, text=f"{index + 1}. {var.get()}").pack(anchor="w")

# GUI setup
root = tk.Tk()
root.title("To-Do List")
root.geometry("926x670")
root.maxsize(926,670)
root.minsize(926,670)
root.config(bg="#0B0C10")

title_label = tk.Label(root, text="📜 To-Do-List 📜", font=("Algerian", 38, "bold"),
                        bg="#0B0C10", fg="#47c4de", justify="center")
title_label.place(x=275, y=20)

# Canvas and scroll settings
def on_mouse_wheel(event):
    canvas.yview_scroll(-1 * (event.delta // 120), "units")
canvas = tk.Canvas(root, width=900, height=470, bg="#0B0C10")
canvas.place(x=10, y=180)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollbar.place(x=900, y=180, height=474)
canvas.config(yscrollcommand=scrollbar.set)
canvas.bind("<MouseWheel>", on_mouse_wheel)
# Buttons: Add Task, Show Tasks, Delete All Tasks
tk.Button(root, text="➕ Add Task", command=add_task, bg="#1F2833", fg="white",
          activebackground="#47c4de", font=("Arial", 12, "bold"), height=2, width=15).place(x=10, y=120)
tk.Button(root, text="📋 Show Tasks", command=show_tasks, bg="#1F2833", fg="white",
          activebackground="#47c4de", font=("Arial", 12, "bold"), height=2, width=15).place(x=200, y=120)
tk.Button(root, text="❌ Delete All Tasks", command=delete_all_tasks, bg="#1F2833", fg="white",
          activebackground="#47c4de", font=("Arial", 12, "bold"), height=2, width=15).place(x=750, y=120)

# Load tasks from JSON file on startup
load_tasks()

root.mainloop()

