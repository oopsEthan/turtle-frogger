from turtle import *
from game_objects import *
from random import randint

# Constants
GAME_SPEED = 15
CAR_SPAWN_TIMER = 450
TOTAL_CARS_ON_SCREEN = 30
UP_KEY = "w"
DOWN_KEY = "s"
ROAD_LENGTH = 550
ROAD_WIDTH = 110
LINE_WIDTH = 10
LINE_LENGTH = 60
FINISH_LINE_Y = 360
SPAWN_POINT_OFFSET = 30

class UI():
    def __init__(self) -> None:
        self.game_window = Screen()
        self.game_window.setup(1024, 768)
        self.game_window.tracer(0)  # Adjust for FPS

        self.gameplay_turtle = Turtle()
        self.gameplay_turtle.pen(pendown=False, shown=False)

        self.text_turtle = Turtle()
        self.text_turtle.pen(pendown=False, shown=False)

        self.draw_finish_line()
        self.roads = Road_Builder()

    def update_screen(self) -> None:
        self.game_window.update()

    def begin_listening(self, player) -> None:
        self.game_window.listen()
        self.game_window.onkeypress(player.up, UP_KEY)
        self.game_window.onkeypress(player.down, DOWN_KEY)
        self.game_window.onkeyrelease(player.stop, UP_KEY)
        self.game_window.onkeyrelease(player.stop, DOWN_KEY)

    def draw_finish_line(self) -> None:
        self.gameplay_turtle.goto(-ROAD_LENGTH, FINISH_LINE_Y)
        self.gameplay_turtle.pen(pendown=True, pencolor="green2", pensize=10)
        self.gameplay_turtle.goto(ROAD_LENGTH, FINISH_LINE_Y)

    def draw_words(self, string, sub_string) -> None:
        self.text_turtle.pen(pendown=False)
        self.text_turtle.goto(0, 170)
        self.text_turtle.pen(pendown=True)
        self.text_turtle.write(f"{string}", align="center", font=("Courier", 32, "bold"))
        self.draw_sub_words(sub_string)

    def draw_sub_words(self, string) -> None:
        self.text_turtle.pen(pendown=False)
        self.text_turtle.goto(0, -5)
        self.text_turtle.pen(pendown=True)
        self.text_turtle.write(f"{string}", align="center", font=("Courier", 24, "bold"))

    def clear_words(self) -> None:
        self.text_turtle.clear()

class Road_Builder():
    def __init__(self) -> None:
        self.road_builder = Turtle()
        self.left_lane_spawn_points = []
        self.right_lane_spawn_points = []
        self.lane_spawn_points = [self.left_lane_spawn_points, self.right_lane_spawn_points]
        self.draw_roads()

    def draw_roads(self) -> None:
        roads_needed = 4
        road_y = 275
        while roads_needed > 0:
            self.draw_individual_road(0, road_y)
            road_y -= 175
            roads_needed -= 1
        self.road_builder.pen(pendown=False)

    def draw_individual_road(self, x, y) -> None:
        self.road_builder.pen(pendown=False, pencolor="gray30", pensize=ROAD_WIDTH)
        self.road_builder.goto(x - ROAD_LENGTH, y)
        self.road_builder.pendown()
        self.road_builder.goto(x + ROAD_LENGTH, y)
        self.update_spawn_points(y)
        self.draw_lines()

    def draw_lines(self) -> None:
        self.road_builder.pen(pencolor="white", pensize=LINE_WIDTH)
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

    def update_spawn_points(self, spawn_point):
        self.left_lane_spawn_points.append(spawn_point - SPAWN_POINT_OFFSET)
        self.right_lane_spawn_points.append(spawn_point + SPAWN_POINT_OFFSET)

class Game():
    def __init__(self) -> None:
        self.ui = UI()
        self.current_cars = []
        self.cars_to_be_removed = []
        self.prev_y = 0
        self.spawn_car()

        self.win = False
        self.collision_detected = False
        self.player = Player()

        self.ui.begin_listening(self.player)
        self.game_loop()

    def game_loop(self) -> None:
        if not self.win and not self.collision_detected:
            for car in self.current_cars:
                if car.car_move(self.ui.game_window):
                    self.cars_to_be_removed.append(car)

            self.player.move()
            self.collision_detected = self.player.check_for_collision(self.current_cars)
            self.win = self.player.check_for_finish(FINISH_LINE_Y)

            if len(self.cars_to_be_removed) >= 1:
                self.clean_cars(self.cars_to_be_removed)

            self.ui.update_screen()

            self.ui.game_window.ontimer(self.game_loop, GAME_SPEED)

        elif self.collision_detected:
            self.hit_by_car()

        elif self.win:
            self.reached_end()

    def spawn_car(self) -> None:
        if len(self.current_cars) < TOTAL_CARS_ON_SCREEN:
            car = Car(self.prev_y)
            self.prev_y = car.determine_spawn(self.ui.game_window, self.ui.roads.lane_spawn_points)
            self.current_cars.append(car)
        self.ui.game_window.ontimer(self.spawn_car, CAR_SPAWN_TIMER)

    def clean_cars(self, car_list_to_clean) -> None:
        for car in car_list_to_clean:
            self.current_cars.remove(car)
            car.car_obj.hideturtle()
            car.car_obj.clear()
            del car
        car_list_to_clean.clear()

    def reached_end(self):
        self.ui.draw_words("You Win!", "Click to continue")
        self.ui.game_window.listen()
        self.ui.game_window.onclick(self.reset_and_increase_difficulty)

    def hit_by_car(self):
        self.ui.draw_words("Game Over!", "Click to restart")
    
    def reset_and_increase_difficulty(self, x=None, y=None):
        print("DEBUG: Click detected!")
        self.clean_cars(self.cars_to_be_removed)
        self.clean_cars(self.current_cars)
        self.ui.update_screen()
        self.win = False
        self.game_loop()

    def run(self) -> None:
        self.ui.game_window.mainloop()