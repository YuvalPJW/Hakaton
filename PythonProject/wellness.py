import tkinter as tk

# Initialize main window
root = tk.Tk()
root.title("Rating UI")
root.geometry("400x220")

# Setup ratings data: (Emoji, Color Hex, Label)
ratings = [
    ("😡", "#ff4d4d", "Very Unwell"),
    ("😕", "#ffa64d", "Unwell"),
    ("😐", "#ffdb4d", "Neutral"),
    ("🙂", "#b3e635", "Well"),
    ("😁", "#4caf50", "Very Well")
]

selected_score = tk.IntVar(value=0)

def update_rating():
    score = selected_score.get()
    emoji, _, label = ratings[score - 1]
    result_label.config(text=f"Selected: {score}/5 - {label} {emoji}")

# Title Label
tk.Label(root, text="How are you feeling today?", font=("Arial", 14, "bold")).pack(pady=10)

# Frame to hold smiley buttons
frame = tk.Frame(root)
frame.pack(pady=5)

# Create 1-5 buttons dynamically
for score, (emoji, color, text) in enumerate(ratings, start=1):
    btn = tk.Radiobutton(
        frame,
        text=f"{emoji}\n{score}",
        value=score,
        variable=selected_score,
        indicatoron=False,        # Makes radio button look like a flat button
        font=("Segoe UI Emoji", 16),
        width=4,
        selectcolor=color,        # Highlight color when selected
        command=update_rating
    )
    btn.pack(side="left", padx=4)


def submit():
    if selected_score.get() != 0:
        root.destroy()
        return selected_score.get()
    return 0

submit_btn = tk.Button(
        root,
        text="Submit",
        font=("Arial", 11, "bold"),
        bg="#007bff",
        fg="white",
        command=submit
    )

# Output Label
result_label = tk.Label(root, text="Please pick a rating", font=("Arial", 11))
result_label.pack(pady=15)
submit_btn.pack(pady=15)


root.mainloop()