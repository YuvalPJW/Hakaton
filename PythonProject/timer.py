
import time
from tkinter import *
from tkinter import messagebox
import tasks
from playsound3 import playsound


def open_timer_popup(screen, task):
    top = Toplevel(screen.gui)
    top.geometry("300x250")

    task_name = task["label"].cget("text") if hasattr(task["label"], "cget") else "Task"
    top.title(f"Timer: {task_name}")

    hour = StringVar(value="00")
    minute = StringVar(value="00")
    second = StringVar(value="00")

    Entry(top, width=3, font=("Arial", 18), textvariable=hour).place(x=80, y=20)
    Entry(top, width=3, font=("Arial", 18), textvariable=minute).place(x=130, y=20)
    Entry(top, width=3, font=("Arial", 18), textvariable=second).place(x=180, y=20)

    timer_running = [False]

    def countdown(temp):
        if temp >= 0 and timer_running[0]:
            mins, secs = divmod(temp, 60)
            hours = 0
            if mins >= 60:
                hours, mins = divmod(mins, 60)

            hour.set(f"{hours:02d}")
            minute.set(f"{mins:02d}")
            second.set(f"{secs:02d}")

            if temp == 0:

                playsound('cat_alarm.wav')

                top.destroy()

                was_completed = messagebox.askyesno(
                    "Timer Finished",
                    f"Time's up for '{task_name}'!\nDid you complete this task?"
                )

                if was_completed:
                    tasks.finish_task(screen, task)
                return

            top.after(1000, countdown, temp - 1)

    def start_timer():
        try:
            total_seconds = int(hour.get()) * 3600 + int(minute.get()) * 60 + int(second.get())
            timer_running[0] = True
            btn.config(state=DISABLED)
            countdown(total_seconds)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numeric values")

    btn = Button(top, text="Start Countdown", bd="5", command=start_timer)
    btn.place(x=70, y=120)