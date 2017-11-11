"""Example Pygame app to showcase the usage of pygame-assets."""

import pygame
import pygame_assets as assets  # let's see what we can do with this!

# Add the icons folders in search directories for the image loader.
assets.config.dirs['image'].append('icons')


def mainloop():
    """Example game loop.

    You can move the player right or left. :)
    """
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    # every asset loader is available through the `assets.load` object.

    # let's load the icon file and use it as our game's icon.
    icon = assets.load.image('icon.png')
    pygame.display.set_icon(icon)

    # let's create a player sprite!
    player, player_rect = assets.load.image_with_rect('player.png')
    player_rect.center = (400, 300)
    player_speed = 200
    move_left = False
    move_right = False

    # below: just to have a simple game loop, the magic happened before. ;)
    running = True
    while running:
        screen.fill((255, 255, 255))
        dt = clock.tick(60) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # infer movement from directional keys
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move_left = True
                if event.key == pygame.K_RIGHT:
                    move_right = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    move_left = False
                if event.key == pygame.K_RIGHT:
                    move_right = False

        # move the rect
        dx = dy = 0
        if move_left:
            dx += -player_speed * dt
        if move_right:
            dx += player_speed * dt
        player_rect.move_ip(dx, dy)

        # display on screen
        screen.blit(player, player_rect)
        pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    mainloop()
