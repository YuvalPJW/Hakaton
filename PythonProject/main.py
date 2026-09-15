import tkinter
from tkinter import messagebox

import screen
import client


# ---------------- CHAT ----------------

# client.py is not changed. We only give it the left side of the screen.
client.setup_chat_client(screen.left_frame)


# ---------------- TASK DATA ----------------

# This is the only task list in the program.
tasks_list = []

# How many completed tasks make the pet happy.
daily_goal = 4


# ---------------- INPUT FUNCTIONS ----------------

def input_error():
    if screen.enter_task_field.get() == "":
        messagebox.showerror(
            "Input Error",
            "Please enter a task"
        )
        return 0

    return 1


def clear_task_number_field():
    screen.task_number_field.delete(
        0,
        tkinter.END
    )


def clear_task_field():
    screen.enter_task_field.delete(
        0,
        tkinter.END
    )


# ---------------- PET ----------------

def update_pet():
    completed_tasks = 0

    for task in tasks_list:
        if task["completed"]:
            completed_tasks += 1

    if completed_tasks == 0:
        pet_state = "sad"

    elif completed_tasks < daily_goal:
        pet_state = "hungry"

    else:
        pet_state = "happy"

    screen.show_pet(pet_state)


# ---------------- REORDER TASKS ----------------

def reorder_tasks():
    unfinished_tasks = []
    finished_tasks = []

    for task in tasks_list:
        if task["completed"]:
            finished_tasks.append(task)
        else:
            unfinished_tasks.append(task)

    tasks_list.clear()
    tasks_list.extend(unfinished_tasks)
    tasks_list.extend(finished_tasks)

    # screen.py only handles how the new order is displayed.
    screen.display_task_order(tasks_list)


# ---------------- FINISH TASK ----------------

def finish_task(task):
    if task["completed"] is False:
        task["completed"] = True
        screen.show_task_completed(task)

    else:
        task["completed"] = False
        screen.show_task_uncompleted(task)

    reorder_tasks()
    update_pet()


# ---------------- ADD TASK ----------------

def insert_task():
    value = input_error()

    if value == 0:
        return

    task_text = screen.enter_task_field.get()
    task_number = len(tasks_list) + 1

    # screen.py creates the widgets.
    # main.py keeps the task data and behavior.
    new_task = screen.create_task_row(
        task_number,
        task_text
    )

    new_task["completed"] = False

    new_task["button"].config(
        command=lambda: finish_task(new_task)
    )

    tasks_list.append(new_task)

    clear_task_field()
    screen.refresh_task_scroll()


# ---------------- DELETE TASK ----------------

def delete_task():
    if len(tasks_list) == 0:
        messagebox.showerror(
            "No Task",
            "There are no tasks to delete"
        )
        return

    number = screen.task_number_field.get()

    if number == "":
        messagebox.showerror(
            "Input Error",
            "Please enter a task number"
        )
        return

    if not number.isdigit():
        messagebox.showerror(
            "Input Error",
            "Please enter a valid number"
        )
        return

    task_number = int(number)

    if task_number < 1 or task_number > len(tasks_list):
        messagebox.showerror(
            "Input Error",
            "Task number does not exist"
        )
        return

    task_to_delete = tasks_list[task_number - 1]

    task_to_delete["frame"].destroy()
    tasks_list.pop(task_number - 1)

    clear_task_number_field()
    reorder_tasks()
    update_pet()


# ---------------- CONNECT BUTTONS TO FUNCTIONS ----------------

screen.submit_button.config(
    command=insert_task
)

screen.delete_button.config(
    command=delete_task
)

screen.enter_task_field.bind(
    "<Return>",
    lambda event: insert_task()
)


# ---------------- START PROGRAM ----------------

# The pet starts sad because no tasks have been completed yet.
update_pet()

screen.gui.mainloop()
