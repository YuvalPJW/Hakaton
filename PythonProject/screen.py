import tkinter


# ---------------- WINDOW ----------------

gui = tkinter.Tk()

gui.title("ToDo App")
gui.geometry("1200x750")
gui.minsize(900, 600)

gui.configure(bg="#f5f5f5")


# ---------------- MAIN SPLIT ----------------

main_split = tkinter.PanedWindow(
    gui,
    orient=tkinter.HORIZONTAL,
    sashwidth=6,
    bg="#cfcfcf",
    bd=0
)

main_split.pack(
    fill="both",
    expand=True
)


# ---------------- LEFT SIDE ----------------

left_frame = tkinter.Frame(
    main_split,
    bg="#f5f5f5"
)

main_split.add(
    left_frame,
    minsize=200
)


# ---------------- RIGHT SIDE ----------------

right_split = tkinter.PanedWindow(
    main_split,
    orient=tkinter.VERTICAL,
    sashwidth=6,
    bg="#cfcfcf",
    bd=0
)

main_split.add(
    right_split,
    minsize=300
)


# ---------------- TOP RIGHT ----------------

top_right_frame = tkinter.Frame(
    right_split,
    bg="#f5f5f5"
)

right_split.add(
    top_right_frame,
    minsize=150
)


# ---------------- BOTTOM RIGHT ----------------

task_frame = tkinter.Frame(
    right_split,
    bg="white"
)

right_split.add(
    task_frame,
    minsize=200
)


# ---------------- TASK TITLE ----------------

title_label = tkinter.Label(
    task_frame,
    text="MY TASKS",
    bg="white",
    fg="#222222",
    font=("Arial", 22, "bold")
)

title_label.pack(
    pady=(15, 8)
)


# ---------------- ADD TASK AREA ----------------

add_frame = tkinter.Frame(
    task_frame,
    bg="white"
)

add_frame.pack(
    fill="x",
    padx=30,
    pady=5
)


enter_task_field = tkinter.Entry(
    add_frame,
    font=("Arial", 14),
    bd=1,
    relief="solid"
)

enter_task_field.pack(
    side="left",
    fill="x",
    expand=True,
    ipady=7
)


# ---------------- TASK LIST AREA ----------------

list_container = tkinter.Frame(
    task_frame,
    bg="white"
)

list_container.pack(
    fill="both",
    expand=True,
    padx=30,
    pady=8
)


task_canvas = tkinter.Canvas(
    list_container,
    bg="white",
    highlightthickness=0
)

task_canvas.pack(
    side="left",
    fill="both",
    expand=True
)


scroll_bar = tkinter.Scrollbar(
    list_container,
    orient="vertical",
    command=task_canvas.yview
)

scroll_bar.pack(
    side="right",
    fill="y"
)


task_canvas.configure(
    yscrollcommand=scroll_bar.set
)


tasks_frame = tkinter.Frame(
    task_canvas,
    bg="white"
)


canvas_window = task_canvas.create_window(
    (0, 0),
    window=tasks_frame,
    anchor="nw"
)


# ---------------- SCROLL FUNCTIONS ----------------

def update_scroll(event):
    task_canvas.configure(
        scrollregion=task_canvas.bbox("all")
    )


tasks_frame.bind(
    "<Configure>",
    update_scroll
)


def resize_tasks_frame(event):
    task_canvas.itemconfig(
        canvas_window,
        width=event.width
    )


task_canvas.bind(
    "<Configure>",
    resize_tasks_frame
)


def mouse_scroll(event):
    task_canvas.yview_scroll(
        int(-1 * (event.delta / 120)),
        "units"
    )


task_canvas.bind_all(
    "<MouseWheel>",
    mouse_scroll
)


# ---------------- TASKS ----------------

tasks = []


# ---------------- REORDER TASKS ----------------

def reorder_tasks():
    unfinished_tasks = []
    finished_tasks = []

    for task in tasks:
        if task["completed"]:
            finished_tasks.append(task)
        else:
            unfinished_tasks.append(task)

    tasks.clear()

    tasks.extend(unfinished_tasks)
    tasks.extend(finished_tasks)

    for task in tasks:
        task["frame"].pack_forget()

    for index in range(len(tasks)):
        tasks[index]["frame"].pack(
            fill="x",
            pady=4
        )

        tasks[index]["number"].config(
            text=str(index + 1) + "."
        )


# ---------------- ADD TASK FUNCTION ----------------

def add_task():
    task_text = enter_task_field.get()

    if task_text == "":
        return

    one_task_frame = tkinter.Frame(
        tasks_frame,
        bg="#f7f7f7"
    )

    one_task_frame.pack(
        fill="x",
        pady=4
    )


    task_number = len(tasks) + 1


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


    new_task = {
        "frame": one_task_frame,
        "number": number_label,
        "label": task_label,
        "button": done_button,
        "completed": False
    }


    def finish_task():
        if new_task["completed"] is False:
            new_task["completed"] = True

            done_button.config(
                text="✓",
                fg="#4f6bed"
            )

            task_label.config(
                fg="#888888",
                font=("Arial", 13, "overstrike")
            )

        else:
            new_task["completed"] = False

            done_button.config(
                text="☐",
                fg="black"
            )

            task_label.config(
                fg="#222222",
                font=("Arial", 13)
            )

        reorder_tasks()


    done_button.config(
        command=finish_task
    )


    tasks.append(new_task)


    enter_task_field.delete(
        0,
        tkinter.END
    )


    gui.update_idletasks()

    task_canvas.configure(
        scrollregion=task_canvas.bbox("all")
    )


# ---------------- ADD BUTTON ----------------

submit_button = tkinter.Button(
    add_frame,
    text="Add Task",
    bg="#4f6bed",
    fg="white",
    activebackground="#4058c9",
    activeforeground="white",
    font=("Arial", 12, "bold"),
    bd=0,
    padx=18,
    pady=8,
    command=add_task
)

submit_button.pack(
    side="left",
    padx=(10, 0)
)


# ---------------- DELETE AREA ----------------

delete_frame = tkinter.Frame(
    task_frame,
    bg="white"
)

delete_frame.pack(
    fill="x",
    padx=30,
    pady=(0, 15)
)


delete_label = tkinter.Label(
    delete_frame,
    text="Delete task number:",
    bg="white",
    fg="#444444",
    font=("Arial", 11)
)

delete_label.pack(
    side="left"
)


task_number_field = tkinter.Entry(
    delete_frame,
    width=5,
    font=("Arial", 12),
    justify="center"
)

task_number_field.pack(
    side="left",
    padx=8
)


# ---------------- DELETE FUNCTION ----------------

def delete_task():
    number = task_number_field.get()

    if number == "":
        return

    if not number.isdigit():
        return

    number = int(number)

    if number < 1 or number > len(tasks):
        return


    task_to_delete = tasks[number - 1]

    task_to_delete["frame"].destroy()

    tasks.pop(number - 1)

    reorder_tasks()


    task_number_field.delete(
        0,
        tkinter.END
    )


    gui.update_idletasks()

    task_canvas.configure(
        scrollregion=task_canvas.bbox("all")
    )


# ---------------- DELETE BUTTON ----------------

delete_button = tkinter.Button(
    delete_frame,
    text="Delete",
    bg="#e85b5b",
    fg="white",
    activebackground="#c94a4a",
    activeforeground="white",
    font=("Arial", 11, "bold"),
    bd=0,
    padx=15,
    pady=6,
    command=delete_task
)

delete_button.pack(
    side="left"
)




enter_task_field.bind(
    "<Return>",
    lambda event: add_task()
)


