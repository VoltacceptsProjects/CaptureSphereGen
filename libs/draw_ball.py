import importlib
from PIL import Image

# BALL_NAME -> PALETTE MODULE
# Must match a module in libs/palettes
BALL_NAMES = [
    'azure_ball',
    'citrine_ball',
    'poke_ball',
    'roseate_ball',
    'slate_ball',
    'verdant_ball',
]


def load_palette_module(ball_name):
    if ball_name not in BALL_NAMES:
        raise ValueError(f'Unknown ball: {ball_name!r}. Choices: {BALL_NAMES}')
    return importlib.import_module(f'libs.palettes.{ball_name}')


def draw_ball(ball_name):
    mod = load_palette_module(ball_name)
    img = Image.new('RGBA', (mod.WIDTH, mod.HEIGHT), (0, 0, 0, 0))
    px = img.load()
    palette = mod.PALETTE
    for y, row in enumerate(mod.PIXELS):
        for x, idx in enumerate(row):
            px[x, y] = palette[idx]
    return img


def draw_all_balls():
    return {name: draw_ball(name) for name in BALL_NAMES}
