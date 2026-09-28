#!/usr/bin/env python3
"""Build themed tiles from the reviewed, vendored artwork in artwork/sources.json."""

import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SVG = "http://www.w3.org/2000/svg"
XLINK = "http://www.w3.org/1999/xlink"
NS = {"s": SVG}
ET.register_namespace("", SVG)
ET.register_namespace("xlink", XLINK)


def tag(name):
    return f"{{{SVG}}}{name}"


def inline_styles(root):
    """Resolve the simple CSS rules in the source logos before combining icons."""
    for style in list(root.iter(tag("style"))):
        css = re.sub(r"/\*.*?\*/", "", style.text or "", flags=re.S)
        for selectors, declarations in re.findall(r"([^{}]+)\{([^{}]*)\}", css):
            for selector in selectors.split(","):
                selector = selector.strip()
                if selector == "svg":
                    matches = [root]
                elif re.fullmatch(r"\.[\w-]+", selector):
                    matches = [node for node in root.iter()
                               if selector[1:] in node.get("class", "").split()]
                else:
                    raise ValueError(f"Unsupported source CSS selector: {selector}")
                for node in matches:
                    # Source stylesheet rules override presentation attributes.
                    for declaration in declarations.split(";"):
                        if not declaration.strip():
                            continue
                        prop, value = declaration.split(":", 1)
                        prop, value = prop.strip(), value.strip()
                        if prop == "enable-background":
                            continue  # Obsolete Illustrator export metadata.
                        node.set(prop, value)
        for parent in root.iter():
            if style in list(parent):
                parent.remove(style)
                break
    for node in root.iter():
        node.attrib.pop("class", None)


def artwork(config, sources, prefix):
    record = sources[config["source"]]
    data = (ROOT / "artwork" / record["file"]).read_bytes()
    if hashlib.sha256(data).hexdigest() != record["sha256"]:
        raise ValueError(f"Source checksum changed: {record['file']}")
    root = ET.fromstring(data)
    inline_styles(root)
    # Do not ship editor payloads, external content, live text or raster images.
    removed = {"metadata", "title", "desc", "foreignObject"}
    for parent in list(root.iter()):
        for node in list(parent):
            if not node.tag.startswith(f"{{{SVG}}}") or node.tag.rsplit("}", 1)[-1] in removed:
                parent.remove(node)
    for node in root.iter():
        if node.tag in {tag("image"), tag("script"), tag("text")}:
            raise ValueError(f"Non-vector content in {record['file']}: {node.tag}")

    # Resolve positional selections before removing nodes, so later indexes do
    # not shift when several parts of a wordmark are excluded.
    selected = {node for expression in config.get("remove", [])
                for node in root.findall(expression, NS)}
    for parent in root.iter():
        for node in list(parent):
            if node in selected:
                parent.remove(node)

    selected = root.find(config["select"], NS) if "select" in config else root
    if selected is None:
        raise ValueError(f"Artwork selection missing in {record['file']}")
    inner = deepcopy(selected)
    shapes = {tag(name) for name in ("path", "rect", "circle", "ellipse", "polygon", "polyline", "line", "use")}
    if not any(node.tag in shapes for node in inner.iter()):
        raise ValueError(f"No visible geometry selected from {record['file']}")
    if inner.tag == tag("svg"):
        inner.tag = tag("g")
        for attr in ("width", "height", "viewBox", "version", "x", "y", "id",
                     "role", "aria-labelledby", "preserveAspectRatio"):
            inner.attrib.pop(attr, None)
    inner.set("fill", inner.get("fill", "#000000"))
    if "color" in config:
        inner.set("color", config["color"])
    # Monochrome project marks may need a contrasting published color variant.
    colors = {key.lower(): value for key, value in config.get("colors", {}).items()}
    for node in inner.iter():
        for attr in ("fill", "stroke"):
            if node.get(attr, "").lower() in colors:
                node.set(attr, colors[node.get(attr).lower()])

    identifiers = {node.get("id"): prefix + node.get("id")
                   for node in inner.iter() if node.get("id")}
    for node in inner.iter():
        for attr, value in list(node.attrib.items()):
            if attr == "id":
                node.set(attr, identifiers[value])
            elif attr.rsplit("}", 1)[-1] == "href" and value.startswith("#"):
                node.set(attr, "#" + identifiers[value[1:]])
            else:
                node.set(attr, re.sub(r"url\(\s*#([^\s)]+)\s*\)",
                                     lambda m: f"url(#{identifiers[m[1]]})", value))
        node.tail = None

    box = config.get("viewBox")
    if box is None:
        box = root.get("viewBox", f"0 0 {root.get('width')} {root.get('height')}")
    x, y, width, height = [float(v) for v in box.split()]
    size = config.get("size", 200)
    scale = size / max(width, height)
    tx, ty = (256 - width * scale) / 2 - x * scale, (256 - height * scale) / 2 - y * scale
    group = ET.Element(tag("g"), {"transform": f"translate({tx:.7g} {ty:.7g}) scale({scale:.7g})"})
    group.append(inner)
    return group


def generate(name, icon, sources, theme):
    prefix = f"{name}-{theme}-"
    root = ET.Element(tag("svg"), {"xmlns:xlink": XLINK, "width": "256", "height": "256",
                                  "viewBox": "0 0 256 256", "fill": "none"})
    backgrounds = icon.get("backgrounds", {"dark": "#242938", "light": "#F4F2ED"})
    if theme == "auto":
        style = ET.SubElement(root, tag("style"))
        css = [f".{prefix}bg {{ fill: {backgrounds['dark']}; }}"]
        light_css = [f".{prefix}bg {{ fill: {backgrounds['light']}; }}"]
        if icon["dark"] != icon["light"]:
            css.append(f".{prefix}light {{ display: none; }}")
            light_css += [f".{prefix}dark {{ display: none; }}", f".{prefix}light {{ display: inline; }}"]
        style.text = "\n    " + "\n    ".join(css) + "\n    @media (prefers-color-scheme: light) {\n      " + "\n      ".join(light_css) + "\n    }\n  "
    ET.SubElement(root, tag("rect"), {"width": "256", "height": "256", "rx": "60",
                                     "fill": backgrounds["light" if theme == "light" else "dark"],
                                     **({"class": prefix + "bg"} if theme == "auto" else {})})
    variants = ["dark", "light"] if theme == "auto" and icon["dark"] != icon["light"] else ["light" if theme == "light" else "dark"]
    for variant in variants:
        group = artwork(icon[variant], sources, prefix + variant + "-")
        if len(variants) > 1:
            group.set("class", prefix + variant)
        root.append(group)
    # ElementTree declares xlink itself when a source has use/href references.
    if any(f"{{{XLINK}}}href" in node.attrib for node in root.iter()):
        del root.attrib["xmlns:xlink"]
    return ET.tostring(root, encoding="unicode") + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail when generated assets are stale")
    args = parser.parse_args()
    manifest = json.loads((ROOT / "artwork" / "sources.json").read_text())
    stale = []
    count = 0
    for name, icon in manifest["icons"].items():
        variants = {f"{name}-{theme}.svg": theme for theme in ("auto", "dark", "light")}
        if icon.get("base"):
            variants[f"{name}.svg"] = "auto"
        for filename, theme in variants.items():
            target = ROOT / "assets" / filename
            expected = generate(name, icon, manifest["sources"], theme)
            count += 1
            if args.check:
                if not target.exists() or target.read_text() != expected:
                    stale.append(str(target.relative_to(ROOT)))
            else:
                target.write_text(expected)
    print(f"{'Checked' if args.check else 'Generated'} {count} SVGs.")
    for path in stale:
        print(f"Stale generated asset: {path}")
    return bool(stale)


if __name__ == "__main__":
    sys.exit(main())
