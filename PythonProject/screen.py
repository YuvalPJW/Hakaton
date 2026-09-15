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


# horizontal line - only on the right
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
    pady=(15, 8)
)


# ---------------- ADD TASK AREA ----------------

addFrame = tkinter.Frame(
    taskFrame,
    bg="white"
)

addFrame.pack(
    fill="x",
    padx=30,
    pady=5
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


# ---------------- TASKS LIST AREA ----------------

listContainer = tkinter.Frame(
    taskFrame,
    bg="white"
)

listContainer.pack(
    fill="both",
    expand=True,
    padx=30,
    pady=8
)


# Canvas allows scrolling
taskCanvas = tkinter.Canvas(
    listContainer,
    bg="white",
    highlightthickness=0
)

taskCanvas.pack(
    side="left",
    fill="both",
    expand=True
)


# Scrollbar
scrollbar = tkinter.Scrollbar(
    listContainer,
    orient="vertical",
    command=taskCanvas.yview
)

scrollbar.pack(
    side="right",
    fill="y"
)


taskCanvas.configure(
    yscrollcommand=scrollbar.set
)


# Frame inside the canvas
tasksFrame = tkinter.Frame(
    taskCanvas,
    bg="white"
)


canvasWindow = taskCanvas.create_window(
    (0, 0),
    window=tasksFrame,
    anchor="nw"
)


# ---------------- SCROLL FUNCTIONS ----------------

def updateScroll(event):

    taskCanvas.configure(
        scrollregion=taskCanvas.bbox("all")
    )


tasksFrame.bind(
    "<Configure>",
    updateScroll
)


# Make tasksFrame use the whole canvas width
def resizeTasksFrame(event):

    taskCanvas.itemconfig(
        canvasWindow,
        width=event.width
    )


taskCanvas.bind(
    "<Configure>",
    resizeTasksFrame
)


# Mouse wheel
def mouseScroll(event):

    taskCanvas.yview_scroll(
        int(-1 * (event.delta / 120)),
        "units"
    )


taskCanvas.bind_all(
    "<MouseWheel>",
    mouseScroll
)


# ---------------- TASKS ----------------

tasks = []


# ---------------- REORDER TASKS ----------------

def reorderTasks():

    # unfinished tasks first
    unfinished = []

    # finished tasks last
    finished = []

    for task in tasks:

        if task["completed"] == True:
            finished.append(task)

        else:
            unfinished.append(task)


    # rebuild list in new order
    tasks.clear()

    tasks.extend(unfinished)

    tasks.extend(finished)


    # remove task frames from their current positions
    for task in tasks:

        task["frame"].pack_forget()


    # place them again in correct order
    for i in range(len(tasks)):

        tasks[i]["frame"].pack(
            fill="x",
            pady=4
        )

        # update task number
        tasks[i]["number"].config(
            text=str(i + 1) + "."
        )


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
        font=("Arial", 13),
        anchor="w"
    )

    taskLabel.pack(
        side="left",
        padx=5,
        pady=8,
        fill="x",
        expand=True
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


    # Dictionary that represents this task
    newTask = {
        "frame": oneTaskFrame,
        "number": numberLabel,
        "label": taskLabel,
        "button": doneButton,
        "completed": False
    }


    # ---------------- COMPLETE TASK ----------------

    def finishTask():

        # if task is unfinished
        if newTask["completed"] == False:

            newTask["completed"] = True

            doneButton.config(
                text="✓",
                fg="#4F6BED"
            )

            taskLabel.config(
                fg="#888888",
                font=("Arial", 13, "overstrike")
            )


        # if task was already finished
        else:

            newTask["completed"] = False

            doneButton.config(
                text="☐",
                fg="black"
            )

            taskLabel.config(
                fg="#222222",
                font=("Arial", 13)
            )


        # move finished tasks to bottom
        reorderTasks()


    doneButton.config(
        command=finishTask
    )


    # add task to list
    tasks.append(newTask)


    # clear entry
    enterTaskField.delete(
        0,
        tkinter.END
    )


    # update scrolling area
    gui.update_idletasks()

    taskCanvas.configure(
        scrollregion=taskCanvas.bbox("all")
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
    pady=(0, 15)
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


    # delete from screen
    taskToDelete["frame"].destroy()


    # delete from list
    tasks.pop(number - 1)


    # update numbers
    reorderTasks()


    # clear delete field
    taskNumberField.delete(
        0,
        tkinter.END
    )


    # update scrolling
    gui.update_idletasks()

    taskCanvas.configure(
        scrollregion=taskCanvas.bbox("all")
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