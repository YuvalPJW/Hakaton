import tkinter as tk

def get_satisfaction_rating():
    rating_result = {"score": 0}

    root = tk.Tk()
    root.title("Rating UI")
    root.geometry("400x220")

    ratings = [
        ("😡", "#ff4d4d", "Very Unwell"),
        ("😕", "#ffa64d", "Unwell"),
        ("😐", "#ffdb4d", "Neutral"),
        ("🙂", "#b3e635", "Well"),
        ("😁", "#4caf50", "Very Well")
    ]

    selected_score = tk.IntVar(value=0)

    tk.Label(root, text="How satisfied are you?", font=("Arial", 14, "bold")).pack(pady=10)

    frame = tk.Frame(root)
    frame.pack(pady=5)

    for score, (emoji, color, text) in enumerate(ratings, start=1):
        btn = tk.Radiobutton(
            frame,
            text=f"{emoji}\n{score}",
            value=score,
            variable=selected_score,
            indicatoron=False,
            font=("Segoe UI Emoji", 16),
            width=4,
            selectcolor=color
        )
        btn.pack(side="left", padx=4)

    def submit():
        if selected_score.get() != 0:
            rating_result["score"] = selected_score.get()
            root.destroy()  # Close rating window to continue execution

    tk.Button(
        root,
        text="Submit",
        font=("Arial", 11, "bold"),
        bg="#007bff",
        fg="white",
        command=submit
    ).pack(pady=15)

    root.mainloop()

    return rating_result["score"]

