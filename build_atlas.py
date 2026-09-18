#!/usr/bin/env python3
"""Assemble src/ into the standalone body_atlas.html.

Three.js and the region data are inlined so the result is a single file that
runs offline from disk with no network, no server, and no build step for the
person using it.
"""
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"
OUT = ROOT / "body_atlas.html"

INJECTIONS = {
    "<!--INJECT:THREE-->": (SRC / "vendor/three.min.js", "Three.js r128 — bundled locally (MIT License, https://threejs.org)"),
    "<!--INJECT:ORBIT-->": (SRC / "vendor/OrbitControls.js", "Three.js OrbitControls — bundled locally (MIT License)"),
    "<!--INJECT:DATA-->": (SRC / "atlas-data.js", "Region data — see src/atlas-data.js"),
}


def main() -> None:
    html = (SRC / "atlas.html").read_text(encoding="utf-8")
    for marker, (path, banner) in INJECTIONS.items():
        if marker not in html:
            raise SystemExit(f"marker {marker} missing from src/atlas.html")
        body = path.read_text(encoding="utf-8")
        html = html.replace(marker, f"<script>\n/* {banner} */\n{body}\n</script>")
    OUT.write_text(html, encoding="utf-8")
    print(f"built {OUT.name}  ({OUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
