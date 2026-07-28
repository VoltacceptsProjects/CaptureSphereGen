import os
from PIL import Image
from libs.draw_ball import draw_all_balls

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    balls = draw_all_balls()
    for name, img in balls.items():
        native_path = os.path.join(OUT_DIR, f'{name}.png')
        img.save(native_path)
        print(f'wrote {native_path} ({img.width}x{img.height})')


if __name__ == '__main__':
    main()
