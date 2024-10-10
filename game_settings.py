from turtle import *
from random import randint
from game_objects import *

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
DEFAULT_DIFFICULTY = 5

class UI(Turtle):
    def __init__(self) -> None:
        super().__init__()
        self.game_window = Screen()
        self.game_window.setup(1024, 768)
        
        # Adjust for FPS
        self.game_window.tracer(0)  # or tracer(8) based on preference

        self.graphics = Graphics_Drawer()
        self.graphics.draw_finish_line()
        self.graphics.draw_roads()

        self.text_turtle = Turtle()
        self.text_turtle.pen(pendown=False, shown=False)

    def update_screen(self) -> None:
        self.game_window.update()

    def begin_listening(self, player: 'Player') -> None:
        self.game_window.listen()
        self.game_window.onkeypress(player.up, UP_KEY)
        self.game_window.onkeypress(player.down, DOWN_KEY)
        self.game_window.onkeyrelease(player.stop, UP_KEY)
        self.game_window.onkeyrelease(player.stop, DOWN_KEY)

    # Draw text on the screen
    def draw_words(self, string: str, sub_string: str) -> None:
        self.move_text_position(0, 170)
        self.write(f"{string}", align="center", font=("Courier", 32, "bold"))
        self.draw_sub_words(sub_string)

    def draw_sub_words(self, string: str) -> None:
        self.move_text_position(0, -5)
        self.write(f"{string}", align="center", font=("Courier", 24, "bold"))

    def clear_words(self) -> None:
        self.clear()

    def move_text_position(self, x: int, y: int) -> None:
        self.pu()
        self.goto(x, y)
        self.pd()

class Graphics_Drawer(Turtle):
    def __init__(self) -> None:
        super().__init__()
        self.left_lane_spawn_points = []
        self.right_lane_spawn_points = []
        self.lane_spawn_points = [self.left_lane_spawn_points, self.right_lane_spawn_points]

    def draw_roads(self) -> None:
        roads_needed = 4
        road_y = 275
        while roads_needed > 0:
            self.draw_individual_road(0, road_y)
            road_y -= 175
            roads_needed -= 1
        self.pen(pendown=False, shown=False)
    
    def draw_individual_road(self, x, y) -> None:
        self.pen(pendown=False, pencolor="gray30", pensize=ROAD_WIDTH)
        self.goto(x-ROAD_LENGTH, y)
        self.pd()
        self.goto(x+ROAD_LENGTH, y)
        self.update_spawn_points(y)
        self.draw_lines()

    def draw_lines(self) -> None:
        self.pen(pencolor="white", pensize=LINE_WIDTH)
        random_starting_x = self.xcor() + randint(-40, 40)
        self.goto(random_starting_x, self.ycor())
        lines = 20
        draw = True
        while lines > 0:
            self.pen(pendown=draw)
            draw = not draw
            new_x = self.xcor() - LINE_LENGTH
            self.goto(new_x, self.ycor())
            lines -= 1
            
    def update_spawn_points(self, spawn_point) -> None:
        self.left_lane_spawn_points.append(spawn_point - SPAWN_POINT_OFFSET)
        self.right_lane_spawn_points.append(spawn_point + SPAWN_POINT_OFFSET)

    def draw_finish_line(self) -> None:
        self.pen(pendown=False)
        self.goto(-ROAD_LENGTH, FINISH_LINE_Y)
        self.pen(pendown=True, pencolor="green2", pensize=10)
        self.goto(ROAD_LENGTH, FINISH_LINE_Y)

class Game():
    def __init__(self) -> None:
        self.ui = UI()
        self.current_cars = []
        self.cars_to_be_removed = []
        self.prev_y = 0
        self.car_timer = CAR_SPAWN_TIMER
        self.difficulty = DEFAULT_DIFFICULTY
        self.ui.update_screen()  # for initial setup

        self.player = Player()
        self.ui.begin_listening(self.player)

        self.game_loop()
        self.spawn_car()

    def game_loop(self) -> None:
        if not self.player.check_for_finish(FINISH_LINE_Y) and not self.player.check_for_collision(self.current_cars):
            self.cars_to_be_removed = [car for car in self.current_cars if car.car_move(self.ui.game_window)]

            self.player.move()
            self.ui.update_screen()

            if len(self.cars_to_be_removed) >= 1:
                self.clean_cars()

            self.ui.game_window.ontimer(self.game_loop, GAME_SPEED)
        elif self.player.check_for_finish(FINISH_LINE_Y):
            self.reached_end()
        elif self.player.check_for_collision(self.current_cars):
            self.hit_by_car()

    def spawn_car(self) -> None:
        if len(self.current_cars) < TOTAL_CARS_ON_SCREEN:
            car = Car(self.prev_y, self.difficulty)
            self.prev_y = car.determine_spawn(self.ui.game_window, self.ui.graphics.lane_spawn_points)
            self.current_cars.append(car)
            self.car_timer += 10
        self.ui.game_window.ontimer(self.spawn_car, self.car_timer)

    def clean_cars(self) -> None:
        for car in self.cars_to_be_removed:
            self.current_cars.remove(car)
            car.hideturtle()
            del car
        self.cars_to_be_removed.clear()

    def reached_end(self) -> None:
        self.ui.draw_words("You Win!", "Click to continue")
        self.ui.game_window.onclick(self.reset_screen)

    def hit_by_car(self) -> None:
        self.ui.draw_words("Game Over!", "Click to restart")
        self.ui.game_window.onclick(self.reset_screen)

    def reset_screen(self, x: int = None, y: int = None) -> None:
        self.ui.clear_words()
        for car in self.current_cars:
            self.cars_to_be_removed.append(car)
        self.clean_cars()
        self.car_timer = CAR_SPAWN_TIMER
        self.player.reset_player()
        self.ui.update_screen()
        self.game_loop()

    def run(self) -> None:
        self.ui.game_window.mainloop()