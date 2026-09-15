import tkinter
from pathlib import Path
from PIL import Image, ImageTk


# ---------------- FILE PATHS ----------------

BASE_DIR = Path(__file__).resolve().parent


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


# ---------------- PET AREA ----------------

pet_canvas = tkinter.Canvas(
    top_right_frame,
    bd=0,
    highlightthickness=0
)

pet_canvas.pack(
    fill="both",
    expand=True
)


# ---------------- LOAD IMAGES ----------------

background_image = Image.open(
    BASE_DIR / "cat house.jfif"
).convert("RGBA")


sad_pet_image = Image.open(
    BASE_DIR / "sad_cat.png"
).convert("RGBA")


hungry_pet_image = Image.open(
    BASE_DIR / "hungery_cat.png"
).convert("RGBA")


normal_pet_image = Image.open(
    BASE_DIR / "normal_cat.png"
).convert("RGBA")


happy_pet_image = Image.open(
    BASE_DIR / "happy_cat.png"
).convert("RGBA")


current_pet_image = sad_pet_image


# ---------------- CREATE IMAGES ON CANVAS ----------------

background_item = pet_canvas.create_image(
    0,
    0,
    anchor="nw"
)


pet_item = pet_canvas.create_image(
    0,
    0,
    anchor="center"
)


background_photo = None
pet_photo = None


# ---------------- RESIZE PET AREA ----------------

def resize_pet_area(event=None):

    global background_photo
    global pet_photo

    frame_width = pet_canvas.winfo_width()
    frame_height = pet_canvas.winfo_height()


    if frame_width < 2 or frame_height < 2:
        return


    # ---------- BACKGROUND ----------

    resized_background = background_image.resize(
        (frame_width, frame_height),
        Image.Resampling.LANCZOS
    )


    background_photo = ImageTk.PhotoImage(
        resized_background
    )


    pet_canvas.itemconfig(
        background_item,
        image=background_photo
    )


    # ---------- PET ----------

    pet_width = int(frame_width * 0.34)
    pet_height = int(frame_height * 0.42)


    resized_pet = current_pet_image.copy()


    resized_pet.thumbnail(
        (pet_width, pet_height),
        Image.Resampling.LANCZOS
    )


    pet_photo = ImageTk.PhotoImage(
        resized_pet
    )


    pet_canvas.itemconfig(
        pet_item,
        image=pet_photo
    )


    # position of cat in the room
    pet_canvas.coords(
        pet_item,
        int(frame_width * 0.47),
        int(frame_height * 0.76)
    )


    # pet should always be above background
    pet_canvas.tag_raise(
        pet_item
    )


pet_canvas.bind(
    "<Configure>",
    resize_pet_area
)


# ---------------- SHOW PET ----------------

def show_pet(state):

    global current_pet_image


    if state == "sad":

        current_pet_image = sad_pet_image


    elif state == "hungry":

        current_pet_image = hungry_pet_image


    elif state == "normal":

        current_pet_image = normal_pet_image


    elif state == "happy":

        current_pet_image = happy_pet_image


    else:

        current_pet_image = normal_pet_image


    resize_pet_area()


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
    pady=8
)

submit_button.pack(
    side="left",
    padx=(10, 0)
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

def update_scroll(event=None):

    task_canvas.configure(
        scrollregion=task_canvas.bbox("all")
    )


def resize_tasks_frame(event):

    task_canvas.itemconfig(
        canvas_window,
        width=event.width
    )


def mouse_scroll(event):

    task_canvas.yview_scroll(
        int(-1 * (event.delta / 120)),
        "units"
    )


tasks_frame.bind(
    "<Configure>",
    update_scroll
)


task_canvas.bind(
    "<Configure>",
    resize_tasks_frame
)


task_canvas.bind_all(
    "<MouseWheel>",
    mouse_scroll
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
    pady=6
)

delete_button.pack(
    side="left"
)


# ---------------- TASK DISPLAY FUNCTIONS ----------------

def create_task_row(task_number, task_text):

    one_task_frame = tkinter.Frame(
        tasks_frame,
        bg="#f7f7f7"
    )

    one_task_frame.pack(
        fill="x",
        pady=4
    )


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


    return {
        "frame": one_task_frame,
        "number": number_label,
        "label": task_label,
        "button": done_button
    }


def show_task_completed(task):

    task["button"].config(
        text="✓",
        fg="#4f6bed"
    )

    task["label"].config(
        fg="#888888",
        font=("Arial", 13, "overstrike")
    )


def show_task_uncompleted(task):

    task["button"].config(
        text="☐",
        fg="black"
    )

    task["label"].config(
        fg="#222222",
        font=("Arial", 13)
    )


def display_task_order(tasks_list):

    for task in tasks_list:

        task["frame"].pack_forget()


    for index in range(len(tasks_list)):

        tasks_list[index]["frame"].pack(
            fill="x",
            pady=4
        )

        tasks_list[index]["number"].config(
            text=str(index + 1) + "."
        )


    refresh_task_scroll()


def refresh_task_scroll():

    gui.update_idletasks()

    task_canvas.configure(
        scrollregion=task_canvas.bbox("all")
    )