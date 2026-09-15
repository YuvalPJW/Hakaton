from tkinter import *
import screen
# import messagebox class from tkinter
from tkinter import messagebox

# global list is declare for storing all the task
tasks_list = []

# global variable is declare for counting the task
counter = 1


# Function for checking input error when
# empty input is given in task field
def inputError():
    # check for enter task field is empty or not
    if screen.enterTaskField.get() == "":
        # show the error message
        messagebox.showerror("Input Error")

        return 0

    return 1


# Function for clearing the contents
# of task number text field
def clear_taskNumberField():
    # clear the content of task number text field
    screen.taskNumberField.delete(0.0, END)


# Function for clearing the contents
# of task entry field
def clear_taskField():
    # clear the content of task field entry box
    screen.enterTaskField.delete(0, END)


# Function for inserting the contents
# from the task entry field to the text area
def insertTask():
    global counter

    # check for error
    value = inputError()

    # if error occur then return
    if value == 0:
        return

    # get the task string concatenating
    # with new line character
    content = screen.enterTaskField.get() + "\n"

    # store task in the list
    tasks_list.append(content)

    # insert content of task entry field to the text area
    # add task one by one in below one by one
    screen.TextArea.insert('end -1 chars', "[ " + str(counter) + " ] " + content)

    # incremented
    counter += 1

    # function calling for deleting the content of task field
    clear_taskField()


# function for deleting the specified task
def delete():
    global counter

    # handling the empty task error
    if len(tasks_list) == 0:
        messagebox.showerror("No task")
        return

    # get the task number, which is required to delete
    number = screen.taskNumberField.get(1.0, END)

    # checking for input error when
    # empty input in task number field
    if number == "\n":
        messagebox.showerror("input error")
        return

    else:
        task_no = int(number)

    # function calling for deleting the
    # content of task number field
    clear_taskNumberField()

    # deleted specified task from the list
    tasks_list.pop(task_no - 1)

    # decremented
    counter -= 1

    # whole content of text area widget is deleted
    screen.TextArea.delete(1.0, END)

    # rewriting the task after deleting one task at a time
    for i in range(len(tasks_list)):
        screen.TextArea.insert('end -1 chars', "[ " + str(i + 1) + " ] " + tasks_list[i])


screen.gui.mainloop()