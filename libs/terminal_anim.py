import os
import sys
import time

RESET = '\033[0m'
HIDE_CURSOR = '\033[?25l'
SHOW_CURSOR = '\033[?25h'
CLEAR_SCREEN = '\033[2J'
HOME = '\033[H'

# Two half-width blocks = one roughly-square "pixel" in most terminals.
CELL = '██'
EMPTY = '  '

HEADER_LINES = 2  # title line + blank line before the grid starts
DELAY = 0.012  # seconds between each pixel


def _enable_windows_ansi():
    """
    Classic Command Prompt (and old PowerShell hosts) don't interpret ANSI
    escape codes unless "virtual terminal processing" is turned on for the
    console — otherwise the raw escape sequences just get printed as text.
    Turns it on for stdout. Returns True if ANSI codes will render.
    """
    if os.name != 'nt':
        return True
    try:
        import ctypes

        ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
        STD_OUTPUT_HANDLE = -11

        kernel32 = ctypes.windll.kernel32
        handle = kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

        mode = ctypes.c_uint32()
        if not kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
            return False
        if not kernel32.SetConsoleMode(handle, mode.value | ENABLE_VIRTUAL_TERMINAL_PROCESSING):
            return False

        # Classic consoles also default to a non-UTF-8 codepage, which can
        # mangle the block characters even once ANSI colors work.
        CP_UTF8 = 65001
        kernel32.SetConsoleOutputCP(CP_UTF8)
        if hasattr(sys.stdout, 'reconfigure'):
            try:
                sys.stdout.reconfigure(encoding='utf-8')
            except Exception:
                pass

        return True
    except Exception:
        return False


def _fg(rgb):
    r, g, b = rgb
    return f'\033[38;2;{r};{g};{b}m'


def _goto(line, col):
    return f'\033[{line};{col}H'


def animate_capture_sphere(name, pixels, palette, width, height):
    """
    Draw `pixels` (rows of palette indices) into the terminal one cell at a
    time, in the same order the PNG is rendered, using the same RGBA
    palette so what you see matches the saved file.

    No-op when stdout isn't a real terminal (e.g. piped/redirected output),
    or when the console can't be switched into ANSI mode (very old Windows
    consoles) — in that case the escape codes would just print as garbage
    text, so we skip straight to saving the PNG instead.
    """
    if not sys.stdout.isatty():
        return
    if not _enable_windows_ansi():
        return

    out = sys.stdout
    out.write(HIDE_CURSOR)
    out.write(CLEAR_SCREEN + HOME)
    out.write(f'Capture Sphere: {name}\n\n')
    # Reserve blank rows so cursor addressing below always lands inside the
    # scrollback-safe region we just printed.
    out.write('\n' * height)
    out.flush()

    try:
        for y, row in enumerate(pixels):
            for x, idx in enumerate(row):
                r, g, b, a = palette[idx]
                col = x * len(CELL) + 1
                line = HEADER_LINES + 1 + y
                out.write(_goto(line, col))
                if a == 0:
                    out.write(EMPTY)
                else:
                    out.write(_fg((r, g, b)) + CELL + RESET)
                out.flush()
                time.sleep(DELAY)
        out.write(_goto(HEADER_LINES + 1 + height, 1))
        out.flush()
        time.sleep(0.2)
    finally:
        out.write(SHOW_CURSOR + '\n')
        out.flush()
