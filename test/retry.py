class User:
    def __init__(self, id, username, goal_burpees):
        self.id = id
        self.username = username
        self.goal_burpees = goal_burpees
        

warrior = User(1,"FADEXxx", 50)

print(f"User({warrior.id}): {warrior.username} has a goal of {warrior.goal_burpees} burpees")