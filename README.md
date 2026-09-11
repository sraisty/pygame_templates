# PyGame Movement Demo

A small PyGame project demonstrating common player movement patterns and collision handling.

This repo is primarily a learning/demo project for experimenting with common 2D game movement patterns in PyGame.

I use these files in my tutoring business, where I teach kids how to code their own games using Python.

## Features

* Base `Player` class with position, velocity, health, sprite surface, and bounding rectangle
* `PlatformerPlayer`

  * Left/right movement
  * Jumping and gravity
  * Platform collision detection
  * Collision handling from above and below
* `HeadingPlayer`

  * Rotation
  * Forward/backward movement in the direction the player is facing
* Player sprites drawn as circles or polygons
* Frame-rate-independent movement using `dt`
* Platforms stored as part of the game state
* Basic screen wrapping support

## Controls

### Platformer

* `Left Arrow` / `A` — move left
* `Right Arrow` / `D` — move right
* `Space` / `W` / `Up Arrow` — jump

### Heading Player

* `Left Arrow` — rotate left
* `Right Arrow` — rotate right
* `Up Arrow` — move forward
* `Down Arrow` — move backward

## Running

Install PyGame:

```bash
pip install pygame
```

Run the game:

```bash
python main.py
```

## Structure

```text
main.py
    Game setup
    GameState
    Event processing
    Update/draw loop
    Platforms

player.py
    Player
    PlatformerPlayer
    HeadingPlayer
    Movement and collision logic
```


