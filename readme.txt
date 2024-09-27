Started 9/21/24

Frogger but made in Python Turtle

Goals:
    - Create classes for game, car, screen, player, etc.
    - Player must be able to cross from one side to the other
    - Cars will spawn randomly and drive across screen
    - Levels that increase car spawn rate and car speed

Focus on:
    - Reducing repetition
    - Consistent Git commit messages
    - Constants were able
    - Indicate what is being returned with -> None

Improvements:
    - Game is laggy after a few car spawns - too much being called on game_loop?
        - Moving towards four lanes - add depth as cars can go both way
        - May help with lag a bit as it will have less cars on the road?
        - Difficulty may either increase speed or vary spawn/speed in some wa

Current Bugs:
    - Ongoing issue with cars on the left side of the road not driving properly, they sort of just... park