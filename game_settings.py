from turtle import *
from game_objects import *
from random import randint

# Constants
GAME_SPEED = 15
CAR_SPAWN_TIMER = 450
TOTAL_CARS_ON_SCREEN = 0
UP_KEY = "w"
DOWN_KEY = "s"
ROAD_LENGTH = 600
ROAD_WIDTH = 110
LINE_WIDTH = 10
LINE_LENGTH = 60

class UI():
    def __init__(self) -> None:
        self.game_window = Screen()
        self.game_window.tracer(0)
        self.road_builder = Turtle()

        self.build_roads()
        self.road_builder.hideturtle()
        
    def update_screen(self) -> None:
        self.game_window.update()

    def begin_listening(self, player) -> None:
        self.game_window.listen()
        self.game_window.onkeypress(player.up, UP_KEY)
        self.game_window.onkeypress(player.down, DOWN_KEY)
        self.game_window.onkeyrelease(player.stop, UP_KEY)
        self.game_window.onkeyrelease(player.stop, DOWN_KEY)

    def build_roads(self) -> None:
        roads_needed = 4
        road_y = 275
        while roads_needed > 0:
            self.build_asphalt(0, road_y)
            road_y -= 175
            roads_needed -= 1
    
    def build_asphalt(self, x, y) -> None:
        self.road_builder.pu()
        self.road_builder.color("gray30")
        self.road_builder.goto(x-ROAD_LENGTH, y)
        self.road_builder.width(ROAD_WIDTH)
        self.road_builder.pd()
        self.road_builder.goto(x+ROAD_LENGTH, y)
        self.paint_lines()

    def paint_lines(self) -> None:
        self.road_builder.color("white")
        self.road_builder.width(LINE_WIDTH)
        random_starting_x = self.road_builder.xcor() + randint(-40, 40)
        self.road_builder.goto(random_starting_x, self.road_builder.ycor())
        lines = 20
        draw = True
        while lines > 0:
            self.road_builder.pen(pendown=draw)
            draw = not draw

            new_x = self.road_builder.xcor() - LINE_LENGTH
            self.road_builder.goto(new_x, self.road_builder.ycor())
            lines -= 1

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
            if(car.car_move(self.ui.game_window)):
                self.cars_to_be_removed.append(car)

        if len(self.cars_to_be_removed) >= 1:
            self.clean_cars()

        self.player.move()
        self.player.check_for_collision(self.current_cars)

        self.ui.update_screen()
        self.ui.game_window.ontimer(self.game_loop, GAME_SPEED)

    def spawn_car(self) -> None:
        self.ui.game_window.ontimer(self.spawn_car, CAR_SPAWN_TIMER)

        if len(self.current_cars) < TOTAL_CARS_ON_SCREEN:
            car = Car()
            car.determine_spawn(self.ui.game_window)
            self.current_cars.append(car)

    def clean_cars(self) -> None:
        for car in self.cars_to_be_removed:
            self.current_cars.remove(car)
            car.car_obj.hideturtle()
        self.cars_to_be_removed.clear()

    def run(self) -> None:
        self.ui.game_window.mainloop()