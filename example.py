import pygame

pygame.init()
screen = pygame.display.set_mode((640, 640))

# main_setup()
mouse_img = pygame.transform.scale(
    pygame.image.load("mouse_in_sweater.png"), (100, 100)
)
mouse_img.set_colorkey((0, 0, 0))
x = 0
clock = pygame.time.Clock()

delta_time = 0.1

running = True


while running:
    # main_loop()
    screen.fill((255, 255, 255))
    screen.blit(mouse_img, (x, 30))

    x += 50 * delta_time  # to handle variable frame rates

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    delta_time = clock.tick(60) / 1000  # my desired framerate is 60fps
    delta_time = max(0.001, min(0.1, delta_time))

pygame.quit()

# def main_setup():
#     mouse_img = pygame.image.load('mouse_in_sweater.png')
# def main_loop():

# Checkout the Surface documentation
# pygame.Surface
# pygame.font.Font(None, size=30)

# Pygame provides some collision detection.
