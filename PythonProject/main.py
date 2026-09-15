import tkinter
from tkinter import messagebox
import screen
import client

client.setup_chat_client(screen.left_frame)
import screen


# list that stores all tasks
tasks_list = []
counter = 1

def input_error():

    if screen.enter_task_field.get() == "":
        messagebox.showerror(
            "Input Error",
            "Please enter a task"
        )

        return 0
    return 1


# ---------------- CLEAR FIELDS ----------------

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


    # remove all task rows from their old positions
    for task in tasks_list:

        task["frame"].pack_forget()


    # put them back in the correct order
    for index in range(len(tasks_list)):

        tasks_list[index]["frame"].pack(
            fill="x",
            pady=4
        )

        tasks_list[index]["number"].config(
            text=str(index + 1) + "."
        )


    # update scroll area
    screen.gui.update_idletasks()

    screen.task_canvas.configure(
        scrollregion=screen.task_canvas.bbox("all")
    )


# ---------------- FINISH TASK ----------------

def finish_task(task):

    if task["completed"] is False:

        task["completed"] = True

        task["button"].config(
            text="✓",
            fg="#4f6bed"
        )

        task["label"].config(
            fg="#888888",
            font=("Arial", 13, "overstrike")
        )


    else:

        task["completed"] = False

        task["button"].config(
            text="☐",
            fg="black"
        )

        task["label"].config(
            fg="#222222",
            font=("Arial", 13)
        )


    reorder_tasks()


# ---------------- INSERT TASK ----------------

def insert_task():

    value = input_error()


    if value == 0:
        return


    task_text = screen.enter_task_field.get()


    # frame for one task
    one_task_frame = tkinter.Frame(
        screen.tasks_frame,
        bg="#f7f7f7"
    )

    one_task_frame.pack(
        fill="x",
        pady=4
    )


    # task number
    task_number = len(tasks_list) + 1


    number_label = tkinter.Label(
        one_task_frame,
        text=str(task_number) + ".",
        bg="#f7f7f7",
        fg="#555555",
        font=("Arial", 13)
    )

    number_label.pack(
        side="left",
        padx=(10, 5),
        pady=8
    )


    # task text
    task_label = tkinter.Label(
        one_task_frame,
        text=task_text,
        bg="#f7f7f7",
        fg="#222222",
        font=("Arial", 13),
        anchor="w"
    )

    task_label.pack(
        side="left",
        padx=5,
        pady=8,
        fill="x",
        expand=True
    )


    # done button
    done_button = tkinter.Button(
        one_task_frame,
        text="☐",
        font=("Arial", 14),
        bg="white",
        bd=0,
        width=3
    )

    done_button.pack(
        side="right",
        padx=10
    )


    # dictionary containing the task
    new_task = {
        "frame": one_task_frame,
        "number": number_label,
        "label": task_label,
        "button": done_button,
        "completed": False
    }


    # button command
    done_button.config(
        command=lambda: finish_task(new_task)
    )


    # add task to the list
    tasks_list.append(new_task)


    # clear entry field
    clear_task_field()


    # update scroll area
    screen.gui.update_idletasks()

    screen.task_canvas.configure(
        scrollregion=screen.task_canvas.bbox("all")
    )


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


    # get task
    task_to_delete = tasks_list[task_number - 1]


    # delete task from screen
    task_to_delete["frame"].destroy()


    # delete task from list
    tasks_list.pop(task_number - 1)


    # clear delete field
    clear_task_number_field()


    # update order and numbers
    reorder_tasks()


# ---------------- BUTTON COMMANDS ----------------

screen.submit_button.config(
    command=insert_task
)


screen.delete_button.config(
    command=delete_task
)


# pressing Enter also adds a task
screen.enter_task_field.bind(
    "<Return>",
    lambda event: insert_task()
)


# ---------------- START PROGRAM ----------------

screen.gui.mainloop()