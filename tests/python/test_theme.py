"""HFR colours meet WCAG AA contrast (4.5 : 1) in both themes (HFR spec §4.4)."""

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
WHITE, DARKLY_BODY = "#ffffff", "#222222"   # Flatly's and Darkly's page backgrounds


def variables(name):
    """The theme file's $variables, with references to other variables resolved."""
    text = (ROOT / "theme" / name).read_text(encoding="utf-8")
    raw = dict(re.findall(r"^\$([\w-]+):\s*([^;]+);", text, re.MULTILINE))

    def resolve(value):
        value = value.strip()
        return resolve(raw[value[1:]]) if value.startswith("$") else value

    return {key: resolve(value) for key, value in raw.items()}


def luminance(colour):
    channels = [int(colour.lstrip("#")[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    linear = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast(a, b):
    high, low = sorted([luminance(a), luminance(b)], reverse=True)
    return (high + 0.05) / (low + 0.05)


def test_contrast_matches_known_values():
    assert contrast("#000000", "#ffffff") == pytest.approx(21.0)
    assert contrast("#777777", "#ffffff") == pytest.approx(4.48, abs=0.01)


@pytest.mark.parametrize("theme,background", [("hfr-light.scss", WHITE), ("hfr-dark.scss", DARKLY_BODY)])
def test_text_is_readable(theme, background):
    v = variables(theme)
    assert contrast(v["link-color"], background) >= 4.5
    assert contrast(v["navbar-fg"], v["navbar-bg"]) >= 4.5
    assert contrast("#ffffff", v["primary"]) >= 4.5          # white text on primary buttons
    if "headings-color" in v:
        assert contrast(v["headings-color"], background) >= 4.5


def test_brand_colours_are_hfr():
    light, dark = variables("hfr-light.scss"), variables("hfr-dark.scss")
    assert light["primary"].upper() == "#006DB5" and light["link-color"].upper() == "#006DB5"
    assert light["navbar-bg"].upper() == "#103379" and dark["navbar-bg"].upper() == "#103379"
