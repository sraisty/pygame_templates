# PyGame template.
# NOTES ABOUT PYGAME
# position [0,0] is the upper left corner of the window.  no negative numbers.

# Import standard modules.
from dataclasses import dataclass, field
import sys

# Import non-standard modules.
import pygame as pg
from player import Player, PlatformerPlayer, HeadingPlayer

# Window HEIGHT=0 and WIDTH=0 will actually create a window that is the max size of the monitor display.
WIDTH, HEIGHT = 0, 0
FPS = 60
GRAVITY = 1800
FLOOR_Y = 800


# a dataclass automatically adds an  __init__() and __repr() methods to the class
@dataclass
class GameState:
    game_type: str
    screen: pg.Surface
    fps_clock: pg.time.Clock
    player: Player
    # if platforms is not provided, make it a non-mutable empty list that won't be shared among
    # GameState instances
    platforms: list[pg.Rect] = field(default_factory=list)
    is_running: bool = True


############### Top-level functions
def setup(game_type: str) -> GameState:

    pg.init()

    # Set up the clock. This will tick every frame and thus maintain a relatively constant
    # frame rate. Hopefully.
    fps_clock = pg.time.Clock()

    # Set up the window.
    # screen is the surface representing the window.
    # PyGame surfaces can be thought of as screen sections that you can draw onto.
    # You can also draw surfaces onto other surfaces, rotate surfaces, and transform surfaces.
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Movement Demo")

    if game_type == "heading":
        return GameState(
            screen=screen,
            fps_clock=fps_clock,
            player=HeadingPlayer(),
            game_type="heading",
        )

    elif game_type == "platformer":
        # Only setup platforms if it is a platformer game. Comment this out otherwise.
        FLOOR_WRAP_SAFETY_MARGIN = 50
        platforms = [
            pg.Rect(
                -FLOOR_WRAP_SAFETY_MARGIN,
                FLOOR_Y,
                screen.get_width() + 2 * FLOOR_WRAP_SAFETY_MARGIN,
                15,
            ),  ## Floor
            pg.Rect(250, 400, 180, 25),
            pg.Rect(600, 320, 150, 25),
            pg.Rect(900, 500, 180, 25),
            pg.Rect(0, 0, screen.get_width(), 15),
        ]

        return GameState(
            screen=screen,
            fps_clock=fps_clock,
            player=PlatformerPlayer(),
            platforms=platforms,
            game_type="platformer",
        )
    else:
        raise ValueError(f"Unknown game type: {game_type}")


def process_events(game: GameState) -> None:
    # Go through events that are passed to the script by the window.
    for event in pg.event.get():
        # We need to handle these events. Initially the only one you'll want to care
        # about is the QUIT event, because if you don't handle it, your game will crash
        # whenever someone tries to exit.
        if event.type == pg.QUIT:
            game.is_running = False
        # Handle other events as you wish.


def update(game: GameState, dt: float) -> None:
    """
    Update game. Called once per frame.
    dt is the amount of time passed since last frame.
    If you want to have constant apparent movement no matter your framerate,
    what you can do is something like
    x += v * dt
    and this will scale your velocity based on time. Extend as necessary.
    """
    # game.player.update(dt)  # platformer_player
    game.player.update(dt, game.screen.get_size(), game.platforms)
    # ==> Insert your frame update code here


def draw(game: GameState) -> None:
    """
    Draw things to the window. Called once per frame.
    """
    game.screen.fill("darkgreen")  # Fill the screen

    for platform in game.platforms:
        pg.draw.rect(game.screen, "white", platform)

    game.player.draw(game.screen)
    # ===> Redraw screen here.  Add your code.
    # img = pg.transform.scale(pg.image.load("my_image.png"), (100, 100))
    # screen.blit(img, (x, 30)). # Blit = draw one image onto another

    # Update the full display Surface to the screen.
    pg.display.flip()


def main():
    game = setup("platformer")

    # dt is the elapsed time since previous frame, so the movement is not tied to the computer's
    # frame rate.  Can now deal with variable frame rates.
    # Clock.tick returns the number of milliseconds passed since previous call.  It will prevent
    # the game from running any faster than FPS frames per second.  dt is the elapsed time since last call in SECONDS.

    while game.is_running:  # Loop forever!
        # calculating dt needs to be done INSIDE the loop, because clock.tick() must be called
        # each time in order to return the number of milliseconds since it was last called.
        dt = game.fps_clock.tick(FPS) / 1000.0
        process_events(game)
        update(game, dt)
        draw(game)

    pg.quit()  # Opposite of pygame.init
    sys.exit()  # Not including this line crashes the script on Windows. Possibly
    # on other operating systems too, but I don't know for sure.


### MAIN LOOP


main()
