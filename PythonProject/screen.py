import tkinter


# ---------------- WINDOW ----------------

gui = tkinter.Tk()

gui.title("ToDo App")

gui.geometry("1200x750")

gui.minsize(900, 600)

gui.configure(bg="#F5F5F5")


# ---------------- SCREEN AREAS ----------------

# left half
leftFrame = tkinter.Frame(
    gui,
    bg="#F5F5F5"
)

leftFrame.place(
    relx=0,
    rely=0,
    relwidth=0.5,
    relheight=1
)


# top right quarter
topRightFrame = tkinter.Frame(
    gui,
    bg="#F5F5F5"
)

topRightFrame.place(
    relx=0.5,
    rely=0,
    relwidth=0.5,
    relheight=0.5
)


# bottom right quarter
taskFrame = tkinter.Frame(
    gui,
    bg="white"
)

taskFrame.place(
    relx=0.5,
    rely=0.5,
    relwidth=0.5,
    relheight=0.5
)


# ---------------- DIVIDING LINES ----------------

# vertical line
verticalLine = tkinter.Frame(
    gui,
    bg="#CFCFCF",
    width=2
)

verticalLine.place(
    relx=0.5,
    rely=0,
    relheight=1,
    anchor="n"
)


# horizontal line - only on the right half
horizontalLine = tkinter.Frame(
    gui,
    bg="#CFCFCF",
    height=2
)

horizontalLine.place(
    relx=0.5,
    rely=0.5,
    relwidth=0.5,
    anchor="w"
)


# ---------------- TASK TITLE ----------------

titleLabel = tkinter.Label(
    taskFrame,
    text="MY TASKS",
    bg="white",
    fg="#222222",
    font=("Arial", 22, "bold")
)

titleLabel.pack(
    pady=(20, 10)
)


# ---------------- ADD TASK AREA ----------------

addFrame = tkinter.Frame(
    taskFrame,
    bg="white"
)

addFrame.pack(
    fill="x",
    padx=30,
    pady=10
)


enterTaskField = tkinter.Entry(
    addFrame,
    font=("Arial", 14),
    bd=1,
    relief="solid"
)

enterTaskField.pack(
    side="left",
    fill="x",
    expand=True,
    ipady=7
)


# ---------------- TASK LIST ----------------

tasksFrame = tkinter.Frame(
    taskFrame,
    bg="white"
)

tasksFrame.pack(
    fill="both",
    expand=True,
    padx=30,
    pady=10
)


tasks = []


# ---------------- ADD TASK FUNCTION ----------------

def addTask():

    taskText = enterTaskField.get()

    if taskText == "":
        return

    # frame for one task
    oneTaskFrame = tkinter.Frame(
        tasksFrame,
        bg="#F7F7F7"
    )

    oneTaskFrame.pack(
        fill="x",
        pady=4
    )


    # task number
    taskNumber = len(tasks) + 1

    numberLabel = tkinter.Label(
        oneTaskFrame,
        text=str(taskNumber) + ".",
        bg="#F7F7F7",
        fg="#555555",
        font=("Arial", 13)
    )

    numberLabel.pack(
        side="left",
        padx=(10, 5),
        pady=8
    )


    # task text
    taskLabel = tkinter.Label(
        oneTaskFrame,
        text=taskText,
        bg="#F7F7F7",
        fg="#222222",
        font=("Arial", 13)
    )

    taskLabel.pack(
        side="left",
        padx=5,
        pady=8
    )


    # done button
    doneButton = tkinter.Button(
        oneTaskFrame,
        text="☐",
        font=("Arial", 14),
        bg="white",
        bd=0,
        width=3
    )

    doneButton.pack(
        side="right",
        padx=10
    )


    # function for marking task as finished
    def finishTask():

        if doneButton["text"] == "☐":

            doneButton.config(
                text="✓"
            )

            taskLabel.config(
                fg="#888888",
                font=("Arial", 13, "overstrike")
            )

        else:

            doneButton.config(
                text="☐"
            )

            taskLabel.config(
                fg="#222222",
                font=("Arial", 13)
            )


    doneButton.config(
        command=finishTask
    )


    # save task
    tasks.append(
        {
            "frame": oneTaskFrame,
            "number": numberLabel
        }
    )


    # clear text field
    enterTaskField.delete(
        0,
        tkinter.END
    )


# ---------------- ADD BUTTON ----------------

Submit = tkinter.Button(
    addFrame,
    text="Add Task",
    bg="#4F6BED",
    fg="white",
    activebackground="#4058C9",
    activeforeground="white",
    font=("Arial", 12, "bold"),
    bd=0,
    padx=18,
    pady=8,
    command=addTask
)

Submit.pack(
    side="left",
    padx=(10, 0)
)


# ---------------- DELETE AREA ----------------

deleteFrame = tkinter.Frame(
    taskFrame,
    bg="white"
)

deleteFrame.pack(
    fill="x",
    padx=30,
    pady=(0, 20)
)


deleteLabel = tkinter.Label(
    deleteFrame,
    text="Delete task number:",
    bg="white",
    fg="#444444",
    font=("Arial", 11)
)

deleteLabel.pack(
    side="left"
)


taskNumberField = tkinter.Entry(
    deleteFrame,
    width=5,
    font=("Arial", 12),
    justify="center"
)

taskNumberField.pack(
    side="left",
    padx=8
)


# ---------------- DELETE FUNCTION ----------------

def deleteTask():

    number = taskNumberField.get()

    if number == "":
        return

    if not number.isdigit():
        return

    number = int(number)

    if number < 1 or number > len(tasks):
        return


    # find task
    taskToDelete = tasks[number - 1]

    # remove from screen
    taskToDelete["frame"].destroy()

    # remove from list
    tasks.pop(number - 1)


    # fix numbers
    for i in range(len(tasks)):

        tasks[i]["number"].config(
            text=str(i + 1) + "."
        )


    taskNumberField.delete(
        0,
        tkinter.END
    )


# ---------------- DELETE BUTTON ----------------

deleteButton = tkinter.Button(
    deleteFrame,
    text="Delete",
    bg="#E85B5B",
    fg="white",
    activebackground="#C94A4A",
    activeforeground="white",
    font=("Arial", 11, "bold"),
    bd=0,
    padx=15,
    pady=6,
    command=deleteTask
)

deleteButton.pack(
    side="left"
)


# ---------------- ENTER KEY ----------------

enterTaskField.bind(
    "<Return>",
    lambda event: addTask()
)


# ---------------- START PROGRAM ----------------

gui.mainloop()