import importlib
import os

from PIL import Image

from libs.shape import WIDTH, HEIGHT, PIXELS as SHAPE_PIXELS
from libs.palette_gen import build_palette
from libs.color_api import fetch_color_name, slugify

PALETTES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'palettes')


def _discover_capture_spheres():
    sphere_names = []
    for filename in os.listdir(PALETTES_DIR):
        if filename.endswith(".py") and filename != "__init__.py":
            sphere_names.append(filename[:-3])  # strip .py
    return sphere_names

CAPTURE_SPHERE_NAMES = _discover_capture_spheres()


def load_palette_module(capture_sphere_name):
    if capture_sphere_name not in CAPTURE_SPHERE_NAMES:
        raise ValueError(
            f"Unknown capture_sphere: {capture_sphere_name!r}. "
            f"Choices: {CAPTURE_SPHERE_NAMES}"
        )
    return importlib.import_module(f'libs.palettes.{capture_sphere_name}')


def _render(palette, pixels=SHAPE_PIXELS, width=WIDTH, height=HEIGHT):
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    px = img.load()
    for y, row in enumerate(pixels):
        for x, idx in enumerate(row):
            px[x, y] = palette[idx]
    return img


def draw_capture_sphere(capture_sphere_name):
    mod = load_palette_module(capture_sphere_name)
    return _render(mod.PALETTE, mod.PIXELS, mod.WIDTH, mod.HEIGHT)


def draw_all_capture_spheres():
    return {name: draw_capture_sphere(name) for name in CAPTURE_SPHERE_NAMES}


def draw_custom_capture_sphere(hex_code, save_palette=True):
    color_name, hex_used = fetch_color_name(hex_code)
    slug = slugify(color_name)
    capture_sphere_name = f'{slug}_capture_sphere'

    palette = build_palette(hex_used)
    img = _render(palette)

    if save_palette:
        _write_palette_module(capture_sphere_name, palette, color_name, hex_used)
        global CAPTURE_SPHERE_NAMES
        CAPTURE_SPHERE_NAMES = _discover_capture_spheres()

    return capture_sphere_name, img, palette


def _write_palette_module(capture_sphere_name, palette, color_name, hex_used):
    os.makedirs(PALETTES_DIR, exist_ok=True)
    path = os.path.join(PALETTES_DIR, f'{capture_sphere_name}.py')

    lines = [
        '# AUTO GENERATED - DO NOT EDIT',
        f'# Color: {color_name}',
        f'# HEX Code: #{hex_used}',
        '',
        f'WIDTH = {WIDTH}',
        f'HEIGHT = {HEIGHT}',
        '',
        'PALETTE = [',
    ]
    for c in palette:
        lines.append(f'    {tuple(c)},')
    lines.append(']')
    lines.append('')
    lines.append('PIXELS = [')
    for row in SHAPE_PIXELS:
        lines.append(f'    {row},')
    lines.append(']')
    lines.append('')

    with open(path, 'w') as f:
        f.write('\n'.join(lines))

    return path
