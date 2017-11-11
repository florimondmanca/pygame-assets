# Pygame Assets

PygameAssets is a lightweight asset manager for Pygame applications and games.

PygameAssets is plug-and-play: just install it, create an `assets` folder in your project directory, drop your assets in and you're ready to go!

## Installation

Pygame Assets is available on PyPI, so use `pip` to install it:

```bash
$ pip install pygame-assets
```

## Documentation

The full documentation is hosted on [ReadTheDocs](#).

## Getting started

PygameAssets expects your assets to be in a folder called `assets`, which should be located at the root of your game project directory. Let's create this folder:

```sh
my_project $ mkdir assets/
```

Want to load an image called `player.png`?


1. Drop `player.png` into `assets/image`
2. Load the image in your game:
```python
import pygame_assets as assets

player_img = assets.load.image('player.png')
```

Bonus points: PygameAssets takes charge of any boilerplate, which means the `assets.load.image` function automatically calls `convert_alpha()` on your image if needed. Check out the documentation for more details.


In fact, much of PygameAssets' API boils down to the `pygame_assets.load` object which gives you access to PygameAssets' **loaders**.

The generic syntax for `pygame_assets.load` is the following:

```python
asset = pygame_assets.load.<loader_name>(filename, ...)
```

> Each loader will expect to find assets in the `assets/<loader_name>` folder. That's why we previously dropped our `player.png` file into `assets/image`.

### Built-in loaders

PygameAssets has the following loaders built-in: `image`, `image_with_rect`, `sound`, `music`, `font`, `freetype`.

See the documentation for full API reference of each loader.

### Custom loaders

If you ever feel the need, PygameAssets allows you to easily define your own asset loaders. Definition of custom loaders is based on the `pygame_assets.loaders.loader` decorator. Here's how to use it:

```python
# my_project/custom_loaders.py
from pygame_assets.loaders import loader

@loader()
def spritesheet(filepath):
    # load the spritesheet then return it
```

We can now use our custom loader to load a spritesheet (located in `assets/spritesheet`):

```python
# my_project/game.py
import pygame_assets as assets

walking_player = assets.load.spritesheet('player-walk.png')
```

You can check out the custom loader API in the [documentation](#documentation).

### Custom configuration

PygameAssets can be easily plugged into any project thanks to its sensible defaults. These defaults, however, may not always fit your needs.

PygameAssets allows you to set some custom configuration:

```python
import pygame_assets as assets

# Redefine the name of the assets base directory ('assets' by default)
assets.config.base = 'static'

# By default, PygameAssets loads assets from subfolders named after the loader.
# You can register other subfolders for a given loader.

assets.config.dirs['spritesheet'].append('sheets')
# PygameAssets will now also look for spritesheets in 'static/sheets'.

# By default, PygameAssets looks for custom loaders in a local custom_loaders.py file.
# You may redefine the path to that file too.
assets.config.custom_loaders_location = 'src.path.to.custom_loaders'
```
