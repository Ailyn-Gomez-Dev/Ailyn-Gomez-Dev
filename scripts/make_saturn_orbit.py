import os
import base64
import math
from PIL import Image, ImageDraw

ICONS = [
    ("React", "react.svg"),
    ("Alpine.js", "alpinejs.svg"),
    ("JavaScript", "javascript.svg"),
    ("TailwindCSS", "tailwindcss.svg"),
    ("HTML5", "html5.svg"),
    ("CSS3", "css3.svg"),
    ("Python", "python.svg"),
    ("Django", "django.svg"),
    ("PHP", "php.svg"),
    ("Laravel", "laravel.svg"),
    ("NodeJS", "nodejs.svg"),
    ("MySQL", "mysql.svg"),
    ("VSCode", "vscode.svg"),
    ("Git", "git.svg"),
    ("GitHub", "github.svg"),
]

ICONS_DIR = "assets/icons"
OUT_SVG = "assets/saturn-orbit.svg"

# Ensure github icon is visible on dark background
github_path = os.path.join(ICONS_DIR, "github.svg")
if os.path.exists(github_path):
    with open(github_path, "r", encoding="utf-8") as f:
        content = f.read()
    if 'fill=' not in content:
        content = content.replace("<path", '<path fill="#FFFFFF"')
    else:
        content = content.replace('fill="#181717"', 'fill="#FFFFFF"').replace('fill="black"', 'fill="#FFFFFF"')
    with open(github_path, "w", encoding="utf-8") as f:
        f.write(content)

# Read and base64-encode all SVGs
encoded_icons = []
for name, filename in ICONS:
    p = os.path.join(ICONS_DIR, filename)
    if os.path.exists(p):
        with open(p, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
        data_uri = f"data:image/svg+xml;base64,{b64}"
        encoded_icons.append((name, data_uri))
    else:
        print(f"Warning: {filename} not found")

N = len(encoded_icons)
DUR = 22.0  # seconds per complete orbit
CX, CY = 425, 125
RX, RY = 360, 65
TILT_DEG = -9

# Elliptical path rotated by TILT_DEG
# In SVG: path from left vertex around ellipse
path_d = f"M {CX - RX},{CY} a {RX},{RY} {TILT_DEG} 1 0 {2*RX},0 a {RX},{RY} {TILT_DEG} 1 0 -{2*RX},0"

# Generate SVG
svg_parts = [
    f'''<svg width="100%" height="240" viewBox="0 0 850 240" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <!-- Ruta eliptica del anillo de Saturno -->
    <path id="saturnOrbit" d="{path_d}" fill="none" />
    
    <!-- Filtro de resplandor para los anillos -->
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
  </defs>

  <!-- Anillos de Saturno (lineas orbitales sutiles en el fondo) -->
  <g transform="rotate({TILT_DEG} {CX} {CY})">
    <ellipse cx="{CX}" cy="{CY}" rx="{RX + 12}" ry="{RY + 3}" fill="none" stroke="#38bdf8" stroke-width="1.2" stroke-dasharray="8 6" opacity="0.25" filter="url(#glow)" />
    <ellipse cx="{CX}" cy="{CY}" rx="{RX}" ry="{RY}" fill="none" stroke="#a855f7" stroke-width="1.8" stroke-dasharray="14 8" opacity="0.4" />
    <ellipse cx="{CX}" cy="{CY}" rx="{RX - 12}" ry="{RY - 3}" fill="none" stroke="#38bdf8" stroke-width="1" stroke-dasharray="6 4" opacity="0.2" />
  </g>
'''
]

# Generate each icon orbiting one behind another
for idx, (name, data_uri) in enumerate(encoded_icons):
    delay = round((idx / N) * DUR, 3)
    
    # Scale animation: larger (42px) in front, smaller (24px) in the back
    # keyTimes: 0 (left/mid), 0.25 (front), 0.5 (right/mid), 0.75 (back), 1.0 (left/mid)
    # values: scale from 0.8 -> 1.15 -> 0.8 -> 0.6 -> 0.8
    scale_values = "0.85; 1.18; 0.85; 0.62; 0.85"
    opacity_values = "0.85; 1.0; 0.85; 0.50; 0.85"
    
    svg_parts.append(f'''
  <!-- Icono: {name} -->
  <g>
    <animateMotion dur="{DUR}s" repeatCount="indefinite" begin="-{delay}s">
      <mpath href="#saturnOrbit" />
    </animateMotion>
    <g>
      <animateTransform attributeName="transform" type="scale"
        values="{scale_values}"
        keyTimes="0; 0.25; 0.5; 0.75; 1"
        dur="{DUR}s" repeatCount="indefinite" begin="-{delay}s" />
      <animate attributeName="opacity"
        values="{opacity_values}"
        keyTimes="0; 0.25; 0.5; 0.75; 1"
        dur="{DUR}s" repeatCount="indefinite" begin="-{delay}s" />
      <image href="{data_uri}" x="-21" y="-21" width="42" height="42" />
    </g>
  </g>''')

svg_parts.append("\n</svg>\n")

full_svg = "".join(svg_parts)
with open(OUT_SVG, "w", encoding="utf-8") as f:
    f.write(full_svg)

print(f"Generated Saturn Orbit SVG at {OUT_SVG} with {N} orbiting icons!")
