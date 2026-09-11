# Import non-standard modules.
import pygame as pg

DEFAULT_PLAYER_X = 50
DEFAULT_PLAYER_Y = 750
DEFAULT_JUMP_STRENGTH = 1300.0
DEFAULT_SPEED = 200  # px/second
PLAYER_POLYGON_POINTS = [[0, 0], [0, 30], [60, 15]]
DEFAULT_HEALTH = 100

PLAYER_CIRCLE_RADIUS = 20

DEFAULT_GRAVITY = 1800


def get_bounding_rect_polygon(points):
    xs = [x for x, y in points]
    ys = [y for x, y in points]
    min_x = min(xs)
    max_x = max(xs)
    min_y = min(ys)
    max_y = max(ys)
    width = max_x - min_x
    height = max_y - min_y

    return pg.Rect(min_x, min_y, width, height)


def get_bounding_rect_circle(center: tuple[int, int], radius: float):
    cx, cy = center
    return pg.Rect(cx - radius, cy - radius, 2 * radius, 2 * radius)


class Player:
    def __init__(self, position=None, shape="circle"):
        if position is None:
            position = pg.Vector2(DEFAULT_PLAYER_X, DEFAULT_PLAYER_Y)
        self.health = DEFAULT_HEALTH
        self.position = pg.Vector2(position)
        self.speed = DEFAULT_SPEED
        self.velocity = pg.Vector2(0, 0)  # speed broken into x and y component
        # Note that self.velocity.y < 0 means player is moving UP the screen
        # and self.velocity.y > 0 means player is moving DOWN the screen
        self.shape = shape
        if shape == "circle":
            self.__init_circle_player()
        elif shape == "polygon":
            self.__init_polygon_player()
        elif shape == "image":
            self.__init_image_player()
            raise NotImplementedError(f"player with shape 'image'")
        else:
            raise ValueError(f"Unknown player shape: {shape}")

        self.rect = self.sprite_surface.get_rect(center=self.position)

    def __init_circle_player(self):
        diameter = PLAYER_CIRCLE_RADIUS * 2
        self.sprite_surface = pg.Surface((diameter, diameter), pg.SRCALPHA)
        pg.draw.circle(
            self.sprite_surface,
            "red",
            (
                PLAYER_CIRCLE_RADIUS,
                PLAYER_CIRCLE_RADIUS,
            ),
            PLAYER_CIRCLE_RADIUS,
        )

    def __init_polygon_player(self):

        bounds = get_bounding_rect_polygon(PLAYER_POLYGON_POINTS)
        self.sprite_surface = pg.Surface((bounds.width, bounds.height), pg.SRCALPHA)
        shifted_points = [
            (x - bounds.left, y - bounds.top) for x, y in PLAYER_POLYGON_POINTS
        ]
        pg.draw.polygon(self.sprite_surface, "red", shifted_points)

    # def __init_image_player(self):
    #     ## NEED HELP

    def update(self, dt: float, platforms: list[pg.Rect] | None = None) -> None:
        pass  # subclasses should define this

    def draw(self, screen: pg.Surface) -> None:
        self.rect.center = self.position
        screen.blit(self.sprite_surface, self.rect)


class PlatformerPlayer(Player):
    """
    Platformer games are where a game player has to jump over things and moves right/left and jumps.
    Like Mario
    """

    def __init__(self, position=None, shape="circle"):
        super().__init__(position=position, shape=shape)
        self.jump_strength = DEFAULT_JUMP_STRENGTH
        self.gravity = DEFAULT_GRAVITY
        self.on_ground = True

    def update(
        self,
        dt: float,
        screen_size: tuple[int, int],
        platforms: list[pg.Rect] | None = None,
    ) -> None:
        keys = pg.key.get_pressed()
        self.update_horizontal_movement(keys, dt)
        self.update_jump(keys)

        # unless collision detection proves otherwise, assume we're no longer
        # standing on a platform or floor (to prevent jumps after falling starts)
        self.on_ground = False
        self.update_gravity(dt)
        self.resolve_platform_collision(platforms or [])
        self.__position_wrap_around(screen_size)

    def update_horizontal_movement(
        self, keys: pg.key.ScancodeWrapper, dt: float
    ) -> None:

        # Can't change direction or speed while in the air
        if self.on_ground:
            if keys[pg.K_LEFT] or keys[pg.K_a]:
                # new_horizontal_direction -= 1
                self.velocity.x = -self.speed
            elif keys[pg.K_RIGHT] or keys[pg.K_d]:
                self.velocity.x = self.speed
            else:
                self.velocity.x = 0
        self.position.x += self.velocity.x * dt

    def __position_wrap_around(self, screen_size: tuple[int, int]) -> None:
        width, height = screen_size

        half_w = self.rect.width / 2
        half_h = self.rect.height / 2

        if self.position.x < -half_w:
            self.position.x = width + half_w
        elif self.position.x > width + half_w:
            self.position.x = -half_w

        if self.position.y < -half_h:
            self.position.y = height + half_h
        elif self.position.y > height + half_h:
            self.position.y = -half_h

    def update_jump(self, keys: pg.key.ScancodeWrapper) -> None:
        if (keys[pg.K_SPACE] or keys[pg.K_w] or keys[pg.K_UP]) and self.on_ground:
            self.velocity.y = -self.jump_strength
            self.on_ground = False

    def update_gravity(self, dt: float):
        self.previous_rect = self.rect.copy()
        self.velocity.y += self.gravity * dt
        self.position.y += self.velocity.y * dt
        self.rect.center = self.position

    def resolve_platform_collision(self, platforms: list[pg.Rect]) -> None:
        # if self.velocity.y < 0:
        # not falling
        # TODO - knockback when hitting a platform from side or below
        # return

        for platform in platforms:
            touching_platform_top = (
                self.previous_rect.bottom <= platform.top
                and self.rect.bottom >= platform.top
            )
            touching_platform_underside = (
                self.previous_rect.top >= platform.bottom
                and self.rect.top <= platform.bottom
            )

            # player at least partially overlaps with the platform
            horizontal_overlap = (
                self.rect.right > platform.left and self.rect.left < platform.right
            )

            # Player is landing on top of the platform
            if (
                touching_platform_top
                and horizontal_overlap
                and self.velocity.y > 0  # heading downward
            ):
                self.rect.bottom = platform.top
                self.position.y = self.rect.centery
                self.on_ground = True
                self.velocity.y = 0
                break

            # Player is bumping into underside of platform
            if (
                touching_platform_underside
                and horizontal_overlap
                and self.velocity.y < 0  # heading upward
            ):
                self.velocity.y = 0  # bound back slow
                # self.velocity.y = -self.velocity.y  # bounce back fast
                self.rect.top = platform.bottom
                self.position.y = self.rect.centery
                break


class HeadingPlayer(Player):
    """
    Heading players are ones where the player rotates the player left or right and then goes forward in the direction the player is headed.  Examples: Asteroids, Driving Car, ...
    """

    def __init__(self, position=None, shape="polygon"):
        super().__init__(position=position, shape=shape)
        self.heading = 0.0  # In degrees, where 0 degrees is facing "East"
        self.turn_speed = 180  # degrees per second

    def update(self, dt: float, platforms: list[pg.Rect] | None = None) -> None:
        keys = pg.key.get_pressed()
        self.update_rotation_and_pos(keys, dt)

    def update_rotation_and_pos(self, keys: pg.key.ScancodeWrapper, dt: float) -> None:
        if keys[pg.K_LEFT]:
            self.heading += self.turn_speed * dt
        if keys[pg.K_RIGHT]:
            self.heading -= self.turn_speed * dt
        direction = pg.Vector2(1, 0).rotate(-self.heading)
        if keys[pg.K_UP]:
            self.position += direction * self.speed * dt
        if keys[pg.K_DOWN]:
            self.position -= direction * self.speed * dt

    def draw(self, screen: pg.Surface) -> None:
        rotated_sprite_surface = pg.transform.rotate(self.sprite_surface, self.heading)
        rotated_rect = rotated_sprite_surface.get_rect(center=self.position)
        screen.blit(rotated_sprite_surface, rotated_rect)
