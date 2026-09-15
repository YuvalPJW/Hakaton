from PIL import Image, ImageTk
import tkinter


cat_label = None
current_cat = "hungry"

original_images = {}


def load_images():
    original_images["hungry"] = Image.open("hungery_cat.png")
    original_images["sad"] = Image.open("sad_cat.png")
    original_images["normal"] = Image.open("normal_cat.png")
    original_images["happy"] = Image.open("happy_cat.png")


def create_cat(screen):
    global cat_label

    load_images()

    cat_label = tkinter.Label(
        screen.left_frame,
        bg="#f5f5f5"
    )

    cat_label.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=30
    )

    show_cat(screen, "hungry")


def show_cat(screen, cat_state):
    global current_cat

    current_cat = cat_state

    image = original_images[cat_state].copy()

    image.thumbnail((500, 500))

    cat_image = ImageTk.PhotoImage(image)

    cat_label.config(
        image=cat_image
    )

    cat_label.image = cat_image


def update_cat(screen, completed_tasks):
    if completed_tasks == 0:
        show_cat(screen, "hungry")

    elif completed_tasks == 1:
        show_cat(screen, "sad")

    elif completed_tasks == 2:
        show_cat(screen, "normal")

    else:
        show_cat(screen, "happy")