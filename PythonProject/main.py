
from wellness import get_satisfaction_rating

user_rating = get_satisfaction_rating()
print(f"User rating received: {user_rating}")

import screen
import tasks
import client

client.setup_chat_client(
    screen.left_frame,
    username="User"
)

screen.submit_button.config(
    command=lambda: tasks.add_task(screen)
)


screen.delete_button.config(
    command=lambda: tasks.delete_task(screen)
)


screen.enter_task_field.bind(
    "<Return>",
    lambda event: tasks.add_task(screen)
)


tasks.initialize_tasks(
    screen
)

screen.gui.mainloop()