import os
import base64

ICONS = [
    ("React", "react.svg"),
    ("Flutter", "flutter.svg"),
    ("Dart", "dart.svg"),
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

# Fix GitHub icon fill for dark mode (pure white)
github_path = os.path.join(ICONS_DIR, "github.svg")
if os.path.exists(github_path):
    with open(github_path, "r", encoding="utf-8") as f:
        c = f.read()
    c = c.replace('fill="#181616"', 'fill="#FFFFFF"').replace('fill="#181717"', 'fill="#FFFFFF"')
    with open(github_path, "w", encoding="utf-8") as f:
        f.write(c)

# Fix Django icon fill to be bright vibrant emerald instead of very dark green
django_path = os.path.join(ICONS_DIR, "django.svg")
if os.path.exists(django_path):
    with open(django_path, "r", encoding="utf-8") as f:
        c = f.read()
    c = c.replace('fill="#092e20"', 'fill="#2ba977"')
    with open(django_path, "w", encoding="utf-8") as f:
        f.write(c)

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
CX, CY = 440, 140
RX, RY = 360, 75
TILT_DEG = -9
BASE_SIZE = 54  # Much larger icons (54px base, scales up to ~73px in front)
HALF_SIZE = BASE_SIZE / 2

path_d = f"M {CX - RX},{CY} a {RX},{RY} {TILT_DEG} 1 0 {2*RX},0 a {RX},{RY} {TILT_DEG} 1 0 -{2*RX},0"

svg_parts = [
    f'''<svg width="100%" height="280" viewBox="0 0 880 280" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <!-- Ruta eliptica del anillo de Saturno -->
    <path id="saturnOrbit" d="{path_d}" fill="none" />
    
    <!-- Filtro de resplandor para los anillos -->
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3.5" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
  </defs>

  <!-- Anillos de Saturno (lineas orbitales cosmicas en el fondo) -->
  <g transform="rotate({TILT_DEG} {CX} {CY})">
    <ellipse cx="{CX}" cy="{CY}" rx="{RX + 14}" ry="{RY + 3}" fill="none" stroke="#38bdf8" stroke-width="1.4" stroke-dasharray="9 7" opacity="0.3" filter="url(#glow)" />
    <ellipse cx="{CX}" cy="{CY}" rx="{RX}" ry="{RY}" fill="none" stroke="#a855f7" stroke-width="2.0" stroke-dasharray="16 9" opacity="0.45" />
    <ellipse cx="{CX}" cy="{CY}" rx="{RX - 14}" ry="{RY - 3}" fill="none" stroke="#38bdf8" stroke-width="1.2" stroke-dasharray="7 5" opacity="0.25" />
  </g>
'''
]

# Keyframe scales: larger (1.35x -> ~73px) in front, legible (0.76x -> ~41px) in back
scale_values = "0.95; 1.35; 0.95; 0.76; 0.95"
opacity_values = "0.92; 1.0; 0.92; 0.68; 0.92"

for idx, (name, data_uri) in enumerate(encoded_icons):
    delay = round((idx / N) * DUR, 3)
    
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
      <image href="{data_uri}" x="-{HALF_SIZE}" y="-{HALF_SIZE}" width="{BASE_SIZE}" height="{BASE_SIZE}" />
    </g>
  </g>''')

svg_parts.append("\n</svg>\n")

full_svg = "".join(svg_parts)
with open(OUT_SVG, "w", encoding="utf-8") as f:
    f.write(full_svg)

print(f"Regenerated Saturn Orbit SVG at {OUT_SVG} with bigger icons!")
