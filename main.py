import argparse
import os

from libs.color_api import ColorApiError
from libs.draw_capture_sphere import CAPTURE_SPHERE_NAMES, draw_capture_sphere, draw_custom_capture_sphere

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')


def save(name, img):
    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, f'{name}.png')
    img.save(path)
    print(f'wrote {path} ({img.width}x{img.height})')
    return path


def generate_custom(hex_code):
    try:
        capture_sphere_name, img, _ = draw_custom_capture_sphere(hex_code)
    except ColorApiError as e:
        print(f'error: {e}')
        raise SystemExit(1)
    except ValueError as e:
        print(f'error: {e}')
        raise SystemExit(1)
    print(f'"{hex_code}" -> {capture_sphere_name} (saved to libs/palettes/{capture_sphere_name}.py)')
    save(capture_sphere_name, img)


def main():
    parser = argparse.ArgumentParser(
        description='Generate a single Capture Sphere (16x16 PNG) from a built-in palette or a custom hex color code.',
    )
    parser.add_argument(
        'capture_sphere', nargs='?',
        help=f'One of the premade Capture Spheres',
    )
    parser.add_argument(
        '--hex', '-x',
        help='Custom HEX Color (e.g. "#FF0000" or "FF0000") to generate a new Capture Sphere palette.',
    )
    args = parser.parse_args()

    if args.hex:
        generate_custom(args.hex)
        return

    capture_sphere_name = args.capture_sphere
    if not capture_sphere_name:
        print('[ERROR]: No Capture Sphere name provided.')
        print('Available Capture Spheres:')
        for sphere in CAPTURE_SPHERE_NAMES:
            print(f'  · {sphere}')

        raise SystemExit(1)
    if capture_sphere_name not in CAPTURE_SPHERE_NAMES:
        print(f'[ERROR]: Unknown Capture Sphere: {capture_sphere_name!r}')
        print('You can generate a Custom Capture Sphere with a HEX color via python main.py --hex <HEX_CODE>')
        print('You can also choose any Available Capture Spheres:')
        for sphere in CAPTURE_SPHERE_NAMES:
            print(f'  · {sphere}')
        raise SystemExit(1)

    img = draw_capture_sphere(capture_sphere_name)
    save(capture_sphere_name, img)


if __name__ == '__main__':
    main()
