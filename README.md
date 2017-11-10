# Pygame Assets

PygameAssets is a lightweight asset manager for Pygame applications and games.

PygameAssets is plug-and-play: just install it, create an `assets` folder in your project directory, drop your assets in and you're ready to go!

## Installation

Pygame Assets is available on PyPI, so use `pip` to install it:

```bash
$ pip install pygame-assets
```

## Usage

PygameAssets expects your assets to be in a folder called `assets`, which should be located at the root of your game project directory. Let's create that folder, shall we?

```sh
my-project $ mkdir assets/
```

Now, let's say we want to load an image called `player.png`. Here's how we'd do it with PygameAssets.


1. Drop `player.png` into `assets/image`
2. Load the image in your game:
```python
import pygame_assets as assets

player_img = assets.load.image('player.png')
```

Voilà! We just loaded an image from the filesystem. Wonder about alpha conversion? PygameAssets takes charge of all that for us!

In fact, PygameAssets' whole API boils down to this `pygame_assets.load` object which takes in charge most of the Pygame asset loading boilerplate. This object gives you access to several **loaders**, each referenced by the type of asset they support (called the **asset type**).

The generic syntax for `pygame_assets.load` is then the following:

```python
asset = pygame_assets.load.<asset_type>(filename, ...)
```

### Supported asset types

PygameAssets supports the following asset types: `image`, `sound`, `music`, `font`, `freetype`, `image_with_rect`.

See the documentation for full API reference for each asset type.

### Custom asset loaders

If you ever feel the need, PygameAssets allows you to easily define your own asset loaders!

You can check out the custom loader API in the [documentation](#documentation).

### Custom configuration

PygameAssets is easily pluggable into any projects thanks to its sensible defaults. However, there might be times when these defaults don't fit your needs.

PygameAssets allows you to set some custom configuration:

```python
import pygame_assets as assets

# Redefine the name of the assets base directory ('assets' by default)
assets.config.base = 'static'

# By default, PygameAssets loads assets from subfolders named after the asset type (in singular form).
# You can register other subfolders for a given asset type.

assets.config.dirs['image'].append('icons')
# PygameAssets will now also look for images in 'static/icons'.

# By default, PygameAssets looks for custom loaders in a local custom_loaders.py file.
# You may redefine the path to that file too.
assets.config.custom_loaders_location = 'src.path.to.custom_loaders'
```


## Documentation

You can view the full documentation at [ReadTheDocs](#).
