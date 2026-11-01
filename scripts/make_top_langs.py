# -*- coding: utf-8 -*-
import pathlib

svg_content = """<svg
  width="495"
  height="195"
  viewBox="0 0 495 195"
  fill="none"
  xmlns="http://www.w3.org/2000/svg"
>
  <style>
    .header {
      font: 600 18px 'Segoe UI', Ubuntu, Sans-Serif;
      fill: #38bdf8;
      animation: fadeInAnimation 0.8s ease-in-out forwards;
    }
    .lang-name {
      font: 400 12px 'Inter', Ubuntu, Sans-Serif;
      fill: #94a3b8;
    }
    @keyframes fadeInAnimation {
      from { opacity: 0; }
      to { opacity: 1; }
    }
  </style>

  <rect
    data-testid="card-bg"
    x="0.5"
    y="0.5"
    rx="4.5"
    height="194"
    stroke="#1e293b"
    width="494"
    fill="#0b0f19"
    stroke-opacity="0"
  />

  <g data-testid="card-title" transform="translate(25, 36)">
    <text x="0" y="0" class="header">My Programming Languages</text>
  </g>

  <g data-testid="main-card-body" transform="translate(25, 54)">
    <mask id="rect-mask">
      <rect x="0" y="0" width="445" height="8" fill="white" rx="4" />
    </mask>

    <!-- Progress Bar Segments -->
    <rect mask="url(#rect-mask)" x="0" y="0" width="187.35" height="8" fill="#3572A5" />
    <rect mask="url(#rect-mask)" x="187.35" y="0" width="144.18" height="8" fill="#f1e05a" />
    <rect mask="url(#rect-mask)" x="331.53" y="0" width="52.51" height="8" fill="#4F5D95" />
    <rect mask="url(#rect-mask)" x="384.04" y="0" width="33.38" height="8" fill="#663399" />
    <rect mask="url(#rect-mask)" x="417.42" y="0" width="18.69" height="8" fill="#e34c26" />
    <rect mask="url(#rect-mask)" x="436.11" y="0" width="8.89" height="8" fill="#f7523f" />

    <!-- Columna 1 -->
    <g transform="translate(0, 32)">
      <circle cx="5" cy="6" r="5" fill="#3572A5" />
      <text x="16" y="10" class="lang-name">Python (42.10%)</text>
    </g>

    <g transform="translate(0, 60)">
      <circle cx="5" cy="6" r="5" fill="#4F5D95" />
      <text x="16" y="10" class="lang-name">PHP (11.80%)</text>
    </g>

    <g transform="translate(0, 88)">
      <circle cx="5" cy="6" r="5" fill="#e34c26" />
      <text x="16" y="10" class="lang-name">HTML (4.20%)</text>
    </g>

    <!-- Columna 2 -->
    <g transform="translate(225, 32)">
      <circle cx="5" cy="6" r="5" fill="#f1e05a" />
      <text x="16" y="10" class="lang-name">JavaScript (32.40%)</text>
    </g>

    <g transform="translate(225, 60)">
      <circle cx="5" cy="6" r="5" fill="#663399" />
      <text x="16" y="10" class="lang-name">CSS (7.50%)</text>
    </g>

    <g transform="translate(225, 88)">
      <circle cx="5" cy="6" r="5" fill="#f7523f" />
      <text x="16" y="10" class="lang-name">Blade (2.00%)</text>
    </g>
  </g>
</svg>
"""

p = pathlib.Path(r'C:\Users\Ailyn Nicol\Desktop\Ailyn-Gomez-Dev\assets\top-langs.svg')
p.write_text(svg_content.strip(), encoding='utf-8')
print("Successfully generated assets/top-langs.svg with Python included (495x195)")
