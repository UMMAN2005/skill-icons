#!/usr/bin/env python3
"""Check SVG structure and references before embedding icons into one document."""

from collections import Counter, defaultdict
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
SVG = "{http://www.w3.org/2000/svg}svg"
URL_REFERENCE = re.compile(r"url\(\s*['\"]?#([^\s)'\"]+)")


def inspect_svg(path):
    text = path.read_text(encoding="utf-8")
    try:
        root = ET.fromstring(text)
    except ET.ParseError as error:
        return [f"invalid XML: {error}"], set(), set()

    errors = []
    if root.tag != SVG:
        errors.append("root must be an SVG element in the SVG namespace")
    if path.parent.name == "assets":
        dimensions = (root.get("width", ""), root.get("height", ""))
        if any(value.removesuffix("px") != "256" for value in dimensions):
            errors.append("icon viewport must be 256 × 256")
        try:
            viewbox = [float(value) for value in root.get("viewBox", "").replace(",", " ").split()]
            if len(viewbox) != 4 or viewbox[2] <= 0 or viewbox[2] != viewbox[3]:
                errors.append("icon viewBox must have a positive, square extent")
        except ValueError:
            errors.append("invalid viewBox")

    counts = Counter(element.get("id") for element in root.iter() if element.get("id"))
    ids = set(counts)
    references = set(URL_REFERENCE.findall(text))
    for element in root.iter():
        for attribute, value in element.attrib.items():
            if attribute.rsplit("}", 1)[-1] == "href" and value.startswith("#"):
                references.add(value[1:])
    for identifier in sorted(references - ids):
        errors.append(f"undefined reference #{identifier}")
    for identifier, count in sorted(counts.items()):
        if count > 1:
            errors.append(f"duplicate id {identifier!r} ({count} occurrences)")
    return errors, ids, references


def main():
    paths = sorted((ROOT / "assets").glob("*.svg")) + sorted((ROOT / ".github").glob("*.svg"))
    errors = []
    definitions = defaultdict(set)
    referenced = set()
    for path in paths:
        issues, ids, references = inspect_svg(path)
        errors.extend(f"{path.relative_to(ROOT)}: {issue}" for issue in issues)
        if path.parent.name == "assets":
            for identifier in ids:
                definitions[identifier].add(path.stem)
            referenced.update(references)

    # Nested SVGs share a document-wide ID namespace in the API response.
    # Theme variants of one icon may intentionally share identical definitions.
    for identifier in sorted(referenced):
        stems = definitions[identifier]
        families = {re.sub(r"-(auto|dark|light)$", "", stem) for stem in stems}
        if len(families) > 1:
            errors.append(f"shared referenced id #{identifier}: {', '.join(sorted(stems))}")

    for error in errors:
        print(error)
    print(f"Checked {len(paths)} SVG files: {len(errors)} errors.")
    return bool(errors)


if __name__ == "__main__":
    sys.exit(main())
