from libs.color_api import normalize_hex

# Luminance ramp (0-255) sampled from the reference orb image, darkest rim
# (index 1) to brightest specular highlight (index 15).
LUMINANCE_RAMP = [44, 47, 56, 60, 69, 76, 81, 95, 112, 122, 129, 161, 188, 196, 211]

# The first STRUCTURAL_STEPS ramp entries (indices 1-5) belong to the top
# nub and the seam line across the middle. Those stay plain gray. The
# outline (6-8) and the body/highlight (9-15) both get the color
# multiply-blended in.
STRUCTURAL_STEPS = 5

# Within the structural range, the nub/seam steps (indices 1-5) are already
# dark (44-69). The raw outline steps (indices 6-8) were lighter (76-95),
# so we rescale the whole structural sub-ramp to fit inside the nub/seam's
# dark range, keeping the shading order but darkening the outline to match.
_structural_raw = LUMINANCE_RAMP[:STRUCTURAL_STEPS]
_src_min, _src_max = min(_structural_raw), max(_structural_raw)
_target_min, _target_max = 44, 69
STRUCTURAL_RAMP = [
    round(_target_min + (v - _src_min) * (_target_max - _target_min) / (_src_max - _src_min))
    for v in _structural_raw
]


def _multiply_blend(gray, r, g, b):
    gn = gray / 255.0
    return (round(gn * r), round(gn * g), round(gn * b), 255)


def build_palette(hex_code):
    h6 = normalize_hex(hex_code)
    r, g, b = int(h6[0:2], 16), int(h6[2:4], 16), int(h6[4:6], 16)

    palette = [(0, 0, 0, 0)]
    for i, gray in enumerate(LUMINANCE_RAMP):
        if i < STRUCTURAL_STEPS:
            gray = STRUCTURAL_RAMP[i]
            palette.append((gray, gray, gray, 255))
        else:
            palette.append(_multiply_blend(gray, r, g, b))
    return palette
