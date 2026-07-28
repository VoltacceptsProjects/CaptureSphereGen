import colorsys

from libs.color_api import normalize_hex

BAND_GRAYS = [
    (40, 40, 40, 255),
    (83, 77, 82, 255),
    (51, 51, 51, 255),
    (33, 33, 33, 255),
    (154, 147, 153, 255),
    (233, 230, 233, 255),
    (207, 203, 207, 255),
    (107, 100, 106, 255),
    (177, 170, 176, 255),
]
NEAR_WHITE = (240, 240, 240, 255)
SHADE_FACTORS = {
    'dark':          (1.12, 0.50),
    'mid_dark':      (1.12, 0.65),
    'mid_bright':    (1.10, 0.88),
    'pale_highlight': (0.35, 1.03),
    'secondary_mid': (1.12, 0.75),
    'darkest':       (0.95, 0.33),
}


def _clamp01(x):
    return max(0.0, min(1.0, x))


def _shade(h, s, v, s_mult, v_mult):
    s2 = _clamp01(s * s_mult)
    v2 = _clamp01(v * v_mult)
    r, g, b = colorsys.hsv_to_rgb(h, s2, v2)
    return (round(r * 255), round(g * 255), round(b * 255), 255)


def build_palette(hex_code):
    h6 = normalize_hex(hex_code)
    r, g, b = int(h6[0:2], 16), int(h6[2:4], 16), int(h6[4:6], 16)
    hh, ss, vv = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)

    palette = [(0, 0, 0, 0)]
    palette.append(_shade(hh, ss, vv, *SHADE_FACTORS['dark']))
    palette.append(_shade(hh, ss, vv, *SHADE_FACTORS['mid_dark']))
    palette.append(_shade(hh, ss, vv, *SHADE_FACTORS['mid_bright']))
    palette.append((r, g, b, 255))
    palette.append(_shade(hh, ss, vv, *SHADE_FACTORS['pale_highlight']))
    palette.append(NEAR_WHITE)
    palette.append(_shade(hh, ss, vv, *SHADE_FACTORS['secondary_mid']))
    palette.append(_shade(hh, ss, vv, *SHADE_FACTORS['darkest']))
    palette.extend(BAND_GRAYS)
    return palette
