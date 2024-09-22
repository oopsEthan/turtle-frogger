from turtle import *
from game_objects import *

# Constants
GAME_SPEED = 20
CAR_SPAWN_TIMER = 350
TOTAL_CARS_ON_SCREEN = 20
UP_KEY = "w"
DOWN_KEY = "s"

class UI():
    def __init__(self) -> None:
        self.game_window = Screen()
        self.game_window.tracer(0)
        
    def update_screen(self) -> None:
        self.game_window.update()

    def begin_listening(self, player) -> None:
        self.game_window.listen()
        self.game_window.onkeypress(player.up, UP_KEY)
        self.game_window.onkeypress(player.down, DOWN_KEY)
        self.game_window.onkeyrelease(player.stop, UP_KEY)
        self.game_window.onkeyrelease(player.stop, DOWN_KEY)


class Game():
    def __init__(self) -> None:
        self.ui = UI()
        self.current_cars = []
        self.cars_to_be_removed = []
        self.spawn_car()

        self.player = Player()

        self.ui.begin_listening(self.player)

        self.game_loop()

    def game_loop(self) -> None:
        for car in self.current_cars:
            if(car.car_move()):
                self.cars_to_be_removed.append(car)
        self.clean_cars()
        self.ui.update_screen()
        self.player.move()
        self.player.check_for_collision(self.current_cars)
        self.ui.game_window.ontimer(self.game_loop, GAME_SPEED)

    def spawn_car(self) -> None:
        self.ui.game_window.ontimer(self.spawn_car, CAR_SPAWN_TIMER)

        if len(self.current_cars) < TOTAL_CARS_ON_SCREEN:
            car = Car()
            self.current_cars.append(car)

    def clean_cars(self) -> None:
        for car in self.cars_to_be_removed:
            self.current_cars.remove(car)
            car.car_obj.hideturtle()
        self.cars_to_be_removed.clear()

    def run(self) -> None:
        self.ui.game_window.mainloop()