from tkinter import messagebox


tasks_list = []


# ---------------- CLEAR FIELDS ----------------

def clear_task_field(screen):
    screen.enter_task_field.delete(
        0,
        "end"
    )


def clear_task_number_field(screen):
    screen.task_number_field.delete(
        0,
        "end"
    )


# ---------------- UPDATE CAT ----------------

def update_cat_status(screen):
    completed_tasks = 0

    for task in tasks_list:
        if task["completed"]:
            completed_tasks += 1


    if completed_tasks == 0:
        screen.show_pet("hungry")

    elif completed_tasks == 1:
        screen.show_pet("sad")

    elif completed_tasks == 2:
        screen.show_pet("normal")

    else:
        screen.show_pet("happy")


# ---------------- REORDER TASKS ----------------

def reorder_tasks(screen):
    unfinished_tasks = []
    finished_tasks = []


    for task in tasks_list:

        if task["completed"]:
            finished_tasks.append(task)

        else:
            unfinished_tasks.append(task)


    tasks_list.clear()

    tasks_list.extend(
        unfinished_tasks
    )

    tasks_list.extend(
        finished_tasks
    )


    screen.display_task_order(
        tasks_list
    )


# ---------------- COMPLETE TASK ----------------

def finish_task(screen, task):

    if task["completed"] is False:

        task["completed"] = True

        screen.show_task_completed(
            task
        )

    else:

        task["completed"] = False

        screen.show_task_uncompleted(
            task
        )


    reorder_tasks(
        screen
    )

    update_cat_status(
        screen
    )


# ---------------- ADD TASK ----------------

def add_task(screen):

    task_text = screen.enter_task_field.get()


    if task_text == "":

        messagebox.showerror(
            "Input Error",
            "Please enter a task"
        )

        return


    # create the task on screen
    task_widgets = screen.create_task_row(
        len(tasks_list) + 1,
        task_text
    )


    # create task dictionary
    new_task = {
        "frame": task_widgets["frame"],
        "number": task_widgets["number"],
        "label": task_widgets["label"],
        "button": task_widgets["button"],
        "completed": False
    }


    # button for completing task
    new_task["button"].config(
        command=lambda: finish_task(
            screen,
            new_task
        )
    )


    # save task
    tasks_list.append(
        new_task
    )


    # clear input field
    clear_task_field(
        screen
    )


    # update scrolling
    screen.refresh_task_scroll()


# ---------------- DELETE TASK ----------------

def delete_task(screen):

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


    # find the task
    task_to_delete = tasks_list[
        task_number - 1
    ]


    # delete it from screen
    task_to_delete["frame"].destroy()


    # delete it from list
    tasks_list.pop(
        task_number - 1
    )


    # clear number field
    clear_task_number_field(
        screen
    )


    # update numbers and order
    reorder_tasks(
        screen
    )


    # update cat
    update_cat_status(
        screen
    )