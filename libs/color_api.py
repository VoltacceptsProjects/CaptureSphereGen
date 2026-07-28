"""
Small client for TheColorAPI (https://www.thecolorapi.com/), used to turn a
hex code the user provides into a human-readable color name (e.g. "3388FF"
-> "Cerulean Blue"), which becomes the custom capture_sphere's name.
"""

import json
import re
import urllib.error
import urllib.request

API_URL = "https://www.thecolorapi.com/id"
TIMEOUT_SECONDS = 10

HEX_RE = re.compile(r'^[0-9a-fA-F]{6}$')


class ColorApiError(RuntimeError):
    """Raised when TheColorAPI can't be reached or returns something unusable."""


def normalize_hex(hex_code):
    """Turn '#3388FF', '3388FF', or the 3-digit shorthand '38F' into 'RRGGBB' (uppercase)."""
    h = hex_code.strip().lstrip('#')
    if len(h) == 3 and re.fullmatch(r'[0-9a-fA-F]{3}', h):
        h = ''.join(ch * 2 for ch in h)
    if not HEX_RE.match(h):
        raise ValueError(
            f'{hex_code!r} is not a valid hex color. '
            f'Use a 6-digit hex code like "3388FF" or "#3388FF".'
        )
    return h.upper()


def fetch_color_name(hex_code):
    """
    Look up the name of a hex color via TheColorAPI.

    Returns (name, normalized_hex). Raises ColorApiError if the request
    fails (network issue, bad response, etc).
    """
    h = normalize_hex(hex_code)
    url = f'{API_URL}?hex={h}'
    req = urllib.request.Request(url, headers={'User-Agent': 'PokeGen/1.0'})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
            data = json.loads(resp.read().decode('utf-8'))
    except (urllib.error.URLError, TimeoutError) as e:
        raise ColorApiError(f'Could not reach TheColorAPI: {e}') from e
    except (json.JSONDecodeError, ValueError) as e:
        raise ColorApiError(f'TheColorAPI returned an unexpected response: {e}') from e

    name = data.get('name', {}).get('value')
    if not name:
        raise ColorApiError('TheColorAPI response did not include a color name.')
    return name, h


def slugify(name):
    """'Cerulean Blue' -> 'cerulean_blue'"""
    slug = re.sub(r'[^a-z0-9]+', '_', name.lower()).strip('_')
    return slug or 'custom'
