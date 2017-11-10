"""Example Pygame app showcasing the usage of pygame-assets."""

import pygame
import pygame_assets as assets

# Configure the assets base directory, the default being 'assets'.
assets.config.base = 'static'

# You can register new directories for assets.
# The line below means pygame-assets will also look for images in the
# static/icons folder.
assets.config.dirs['image'].append('icons')

# You can change the location where pygame-assets finds your custom loaders.
# Useful just in case the default 'custom_loaders.py' collides with one of
# your existing modules (not so likely, though).
assets.config.custom_loaders_module = 'myloaders'

# Only required because the default config was changed.
# Note: it is safe to initialize pygame-assets several times.
assets.init()


def mainloop():
    """Example game loop.

    You can move the player right or left!
    """
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    icon = assets.load.image('icon.png')
    pygame.display.set_icon(icon)

    # let's load a player sprite!
    player, player_rect = assets.load.image_with_rect('player.png')
    player_rect.center = (400, 300)
    player_speed = 200
    move_left = False
    move_right = False

    # we could create a spritesheet using our custom spritesheet loader!
    spritesheet = assets.load.spritesheet('some_name.png')
    assert spritesheet == 'dummy spritesheet'
    # we would only have to define a real loader
    # and add some spritesheet to the assets/spritesheet/ folder. :)

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
