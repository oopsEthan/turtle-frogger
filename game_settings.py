from turtle import *

class UI():
    def __init__(self) -> None:
        self.game_window = Screen()

class Game():
    def __init__(self) -> None:
        self.ui = UI()

    def run(self):
        self.ui.game_window.mainloop()