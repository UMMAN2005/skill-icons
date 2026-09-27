#!/usr/bin/env python3
"""Render reviewed icons and optional profile strips in Chromium (Pillow + Playwright)."""

import argparse
import base64
import io
import json
from pathlib import Path
import re
import sys
from urllib.parse import parse_qs, urlparse
import xml.etree.ElementTree as ET

from PIL import Image, ImageChops, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
SVG = "{http://www.w3.org/2000/svg}"
ET.register_namespace("", SVG[1:-1])

RENDER = """async svg => {
  const img = new Image();
  img.src = 'data:image/svg+xml;base64,' + btoa(unescape(encodeURIComponent(svg)));
  await img.decode();
  const canvas = document.createElement('canvas');
  canvas.width = img.width; canvas.height = img.height;
  canvas.getContext('2d').drawImage(img, 0, 0);
  return canvas.toDataURL('image/png').split(',')[1];
}"""


def changed_pixels(first, second):
    delta = ImageChops.difference(first.convert("RGBA"), second.convert("RGBA"))
    return sum(max(pixel) > 8 for pixel in delta.getdata())


def composite(svgs):
    # Match the API's nesting at an integer 64px scale. Fractional 48px
    # placement would add antialiasing differences unrelated to CSS leakage.
    width = len(svgs) * 75 - 11
    groups = "".join(f'<g transform="translate({i * 300} 0)">{svg}</g>'
                     for i, svg in enumerate(svgs))
    return (f'<svg xmlns="{SVG[1:-1]}" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{width}" height="64" viewBox="0 0 {width * 4} 256" fill="none">'
            f'{groups}</svg>')


def render(page, svg):
    return Image.open(io.BytesIO(base64.b64decode(page.evaluate(RENDER, svg)))).convert("RGBA")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", type=Path, help="Profile README whose actual icon URLs should be checked")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    assets = {path.stem: path.read_text() for path in (ROOT / "assets").glob("*.svg")}
    manifest = json.loads((ROOT / "artwork/sources.json").read_text())
    names = list(manifest["icons"])
    api = (ROOT / "api/index.go").read_text()
    aliases = dict(re.findall(r'"([^"]+)"\s*:\s*"([^"]+)"',
                             api.split("var shortNames =", 1)[1].split("\n}", 1)[0]))

    def resolve(name, theme):
        if name in assets:
            return name + "-" + theme if theme != "auto" and name + "-" + theme in assets else name
        if name + "-" + theme in assets:
            return name + "-" + theme
        target = aliases.get(name, name)
        return target + "-" + theme if target + "-" + theme in assets else target

    strips = [names, ["certmanager", "springdatajpa"]]
    if args.profile:
        for url in re.findall(r'https://[^\s)"<>]+/api/icons\?[^\s)"<>]+', args.profile.read_text()):
            strips.append(parse_qs(urlparse(url).query)["i"][0].split(","))
    failures = []
    checked = 0
    previews = {}
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()
        page.route("http://**/*", lambda route: route.abort())
        page.route("https://**/*", lambda route: route.abort())
        for scheme in ("dark", "light"):
            page.emulate_media(color_scheme=scheme)
            for name in names:
                auto = render(page, composite([assets[name + "-auto"]]))
                fixed = render(page, composite([assets[name + "-" + scheme]]))
                if changed_pixels(auto, fixed) > 32:
                    failures.append(f"{name}: auto/{scheme} differs from explicit theme")
                previews[name, scheme] = auto
                root = ET.fromstring(assets[name + "-" + scheme])
                root.remove(root.find(SVG + "rect"))
                foreground = render(page, composite([ET.tostring(root, encoding="unicode")]))
                bounds = foreground.getchannel("A").getbbox()
                if bounds is None:
                    failures.append(f"{name}/{scheme}: empty artwork")
                elif min(bounds[:2]) < 3 or max(bounds[2:]) > 61:
                    failures.append(f"{name}/{scheme}: artwork touches tile edge: {bounds}")
                checked += 1
            for index, strip in enumerate(strips):
                for theme in ("auto", "dark", "light"):
                    resolved = [resolve(name, theme) for name in strip]
                    missing = [name for name in resolved if name not in assets]
                    if missing:
                        failures.append(f"strip {index}: missing {missing}")
                        continue
                    image = render(page, composite([assets[name] for name in resolved]))
                    for i, name in enumerate(resolved):
                        single = render(page, composite([assets[name]]))
                        combined = image.crop((i * 75, 0, i * 75 + 64, 64))
                        changed = changed_pixels(single, combined)
                        if changed > 32:
                            failures.append(f"{name}/{scheme} in strip {index}/{theme}: {changed} changed pixels")
                        checked += 1
                    if theme == "auto":
                        image.save(args.output / f"strip-{index:02d}-{scheme}.png")
        browser.close()

    font = ImageFont.load_default(size=14)
    sheet = Image.new("RGB", (4 * 196, ((len(names) + 3) // 4) * 110), "#242938")
    draw = ImageDraw.Draw(sheet)
    for i, name in enumerate(names):
        x, y = (i % 4) * 196, (i // 4) * 110
        draw.text((x + 8, y + 4), name, fill="white", font=font)
        for offset, scheme in enumerate(("dark", "light")):
            tile = previews[name, scheme]
            sheet.paste(tile, (x + 12 + offset * 85, y + 28), tile)
    sheet.save(args.output / "reviewed-icons.png")
    result = {"checks": checked, "reviewed_icons": len(names), "strips": len(strips), "failures": failures}
    (args.output / "report.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    return bool(failures)


if __name__ == "__main__":
    sys.exit(main())
