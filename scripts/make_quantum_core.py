# -*- coding: utf-8 -*-
"""
Generates an ultra-aesthetic 3D Neon Quantum Core / Cyberpunk Hologram GIF
with volumetric glow, multi-axis gyroscopic rings, pulsing core, and orbiting particles.
Enlarged to fill the 320x320 canvas with stunning presence and optimal margins.
"""

import math
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

W, H = 320, 320
CX, CY = W / 2, H / 2
NUM_FRAMES = 60
BG_COLOR = (11, 15, 25)  # #0b0f19 to seamlessly match TokyoNight palette

def rot_x(x, y, z, ang):
    c, s = math.cos(ang), math.sin(ang)
    return x, y * c - z * s, y * s + z * c

def rot_y(x, y, z, ang):
    c, s = math.cos(ang), math.sin(ang)
    return x * c + z * s, y, -x * s + z * c

def rot_z(x, y, z, ang):
    c, s = math.cos(ang), math.sin(ang)
    return x * c - y * s, x * s + y * c, z

def project(x, y, z, cam_dist=420):
    denom = max(100.0, cam_dist + z)
    dist = cam_dist / denom
    px = CX + x * dist
    py = CY + y * dist
    return px, py, z

# Precompute icosahedron vertices for the outer quantum cage
phi = (1 + math.sqrt(5)) / 2
base_verts = [
    (-1,  phi, 0), ( 1,  phi, 0), (-1, -phi, 0), ( 1, -phi, 0),
    (0, -1,  phi), (0,  1,  phi), (0, -1, -phi), (0,  1, -phi),
    ( phi, 0, -1), ( phi, 0,  1), (-phi, 0, -1), (-phi, 0,  1)
]
norm_verts = []
for vx, vy, vz in base_verts:
    l = math.sqrt(vx*vx + vy*vy + vz*vz)
    norm_verts.append((vx/l, vy/l, vz/l))

edges = []
for i in range(len(norm_verts)):
    for j in range(i + 1, len(norm_verts)):
        dx = norm_verts[i][0] - norm_verts[j][0]
        dy = norm_verts[i][1] - norm_verts[j][1]
        dz = norm_verts[i][2] - norm_verts[j][2]
        dist = math.sqrt(dx*dx + dy*dy + dz*dz)
        if abs(dist - 1.05) < 0.15:
            edges.append((i, j))

# Quantum particles (enlarged orbital radius)
np.random.seed(42)
NUM_PARTICLES = 36
particle_r = np.random.uniform(96, 138, NUM_PARTICLES)
particle_theta = np.random.uniform(0, 2 * math.pi, NUM_PARTICLES)
particle_phi = np.random.uniform(-math.pi/2, math.pi/2, NUM_PARTICLES)
particle_speed = np.random.uniform(0.8, 1.4, NUM_PARTICLES)
particle_color_type = np.random.choice([0, 1, 2], NUM_PARTICLES)

frames = []

for f in range(NUM_FRAMES):
    progress = f / NUM_FRAMES
    angle = progress * 2 * math.pi

    # Base canvas
    base_im = Image.new("RGBA", (W, H), (*BG_COLOR, 255))
    draw = ImageDraw.Draw(base_im)

    # Glow layer for additive blending
    glow_im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_im)

    # 1. Central Pulsing Energy Core
    pulse = math.sin(angle * 3) * 0.14 + 0.86
    core_rad = 28 * pulse

    # Radial ambient volumetric glow
    for r in range(75, 8, -6):
        alpha = int(32 * (1 - r / 75) * pulse)
        glow_draw.ellipse(
            [CX - r, CY - r, CX + r, CY + r],
            fill=(168, 85, 247, alpha)  # Neon purple ambient
        )
    for r in range(46, 3, -4):
        alpha = int(85 * (1 - r / 46) * pulse)
        glow_draw.ellipse(
            [CX - r, CY - r, CX + r, CY + r],
            fill=(56, 189, 248, alpha)  # Electric cyan inner
        )

    render_queue = []

    # 2. Concentric Gyroscopic Rings
    # Ring A: Electric Cyan horizontal tilt
    ring_r_a = 90
    num_pts = 52
    ring_a_pts = []
    for i in range(num_pts):
        th = (i / num_pts) * 2 * math.pi
        x = ring_r_a * math.cos(th)
        y = ring_r_a * math.sin(th) * 0.28
        z = ring_r_a * math.sin(th) * 0.95
        x, y, z = rot_x(x, y, z, angle * 1.0 + 0.3)
        x, y, z = rot_y(x, y, z, angle * 0.7)
        px, py, pz = project(x, y, z)
        ring_a_pts.append((px, py, pz))

    for i in range(num_pts):
        p1 = ring_a_pts[i]
        p2 = ring_a_pts[(i + 1) % num_pts]
        avg_z = (p1[2] + p2[2]) / 2
        render_queue.append(('line', avg_z, p1, p2, (0, 240, 255), 2.8, 'ring_cyan'))

    # Ring B: Cyberpunk Purple vertical tilt
    ring_r_b = 114
    ring_b_pts = []
    for i in range(num_pts):
        th = (i / num_pts) * 2 * math.pi
        x = ring_r_b * math.sin(th) * 0.32
        y = ring_r_b * math.cos(th)
        z = ring_r_b * math.sin(th) * 0.95
        x, y, z = rot_y(x, y, z, -angle * 1.2 + 0.5)
        x, y, z = rot_z(x, y, z, angle * 0.5)
        px, py, pz = project(x, y, z)
        ring_b_pts.append((px, py, pz))

    for i in range(num_pts):
        p1 = ring_b_pts[i]
        p2 = ring_b_pts[(i + 1) % num_pts]
        avg_z = (p1[2] + p2[2]) / 2
        render_queue.append(('line', avg_z, p1, p2, (189, 0, 255), 2.4, 'ring_purple'))

    # Ring C: Outer Magenta / Starlight ring
    ring_r_c = 135
    ring_c_pts = []
    for i in range(num_pts):
        th = (i / num_pts) * 2 * math.pi
        x = ring_r_c * math.cos(th)
        y = ring_r_c * math.sin(th)
        z = 0
        x, y, z = rot_x(x, y, z, angle * 0.6)
        x, y, z = rot_y(x, y, z, angle * 0.9)
        x, y, z = rot_z(x, y, z, angle * 0.3)
        px, py, pz = project(x, y, z)
        ring_c_pts.append((px, py, pz))

    for i in range(num_pts):
        p1 = ring_c_pts[i]
        p2 = ring_c_pts[(i + 1) % num_pts]
        avg_z = (p1[2] + p2[2]) / 2
        render_queue.append(('line', avg_z, p1, p2, (255, 60, 180), 2.0, 'ring_magenta'))

    # 3. Rotating 3D Quantum Geometric Cage (Icosahedron)
    cage_scale = 75 + 5 * math.sin(angle * 2)
    proj_verts = []
    for vx, vy, vz in norm_verts:
        x = vx * cage_scale
        y = vy * cage_scale
        z = vz * cage_scale
        x, y, z = rot_x(x, y, z, angle * 1.5)
        x, y, z = rot_y(x, y, z, angle * 1.0)
        px, py, pz = project(x, y, z)
        proj_verts.append((px, py, pz))

    for i, j in edges:
        p1 = proj_verts[i]
        p2 = proj_verts[j]
        avg_z = (p1[2] + p2[2]) / 2
        render_queue.append(('line', avg_z, p1, p2, (220, 240, 255), 2.2, 'cage'))

    for idx, pt in enumerate(proj_verts):
        render_queue.append(('node', pt[2], pt, (0, 240, 255), 4.2))

    # 4. Orbiting Quantum Particles
    for i in range(NUM_PARTICLES):
        th = particle_theta[i] + angle * particle_speed[i]
        ph = particle_phi[i]
        rad = particle_r[i]
        x = rad * math.cos(ph) * math.cos(th)
        y = rad * math.sin(ph)
        z = rad * math.cos(ph) * math.sin(th)
        x, y, z = rot_x(x, y, z, 0.4)
        x, y, z = rot_y(x, y, z, angle * 0.4)
        px, py, pz = project(x, y, z)

        ctype = particle_color_type[i]
        if ctype == 0:
            color = (0, 240, 255)
        elif ctype == 1:
            color = (189, 0, 255)
        else:
            color = (255, 255, 255)

        render_queue.append(('particle', pz, (px, py, pz), color, 3.2))

    # Add core to queue
    render_queue.append(('core', 0, (CX, CY, 0), None, core_rad))

    # Sort back-to-front (lowest z is deepest in screen)
    render_queue.sort(key=lambda item: item[1])

    # Draw everything with depth-aware brightness & glow
    for item in render_queue:
        itype = item[0]
        z = item[1]
        depth_factor = (z + 180) / 360.0
        depth_factor = max(0.25, min(1.0, depth_factor))

        if itype == 'core':
            c_r = item[4]
            glow_draw.ellipse(
                [CX - c_r, CY - c_r, CX + c_r, CY + c_r],
                fill=(0, 240, 255, 230)
            )
            inner_r = c_r * 0.55
            glow_draw.ellipse(
                [CX - inner_r, CY - inner_r, CX + inner_r, CY + inner_r],
                fill=(255, 255, 255, 255)
            )

        elif itype == 'line':
            p1, p2, col, base_w, ltype = item[2], item[3], item[4], item[5], item[6]
            w = max(1.2, base_w * depth_factor)
            alpha = int(255 * (0.35 + 0.65 * depth_factor))
            line_col = (*col, alpha)

            if depth_factor > 0.50:
                glow_draw.line(
                    [(p1[0], p1[1]), (p2[0], p2[1])],
                    fill=(*col, int(115 * depth_factor)),
                    width=int(w + 3.5)
                )

            draw.line([(p1[0], p1[1]), (p2[0], p2[1])], fill=line_col, width=int(w))

        elif itype == 'node':
            pt, col, base_r = item[2], item[3], item[4]
            r = max(2.0, base_r * depth_factor)
            alpha = int(255 * (0.4 + 0.6 * depth_factor))
            draw.ellipse(
                [pt[0] - r, pt[1] - r, pt[0] + r, pt[1] + r],
                fill=(*col, alpha)
            )
            if depth_factor > 0.55:
                glow_draw.ellipse(
                    [pt[0] - r*2.2, pt[1] - r*2.2, pt[0] + r*2.2, pt[1] + r*2.2],
                    fill=(*col, 120)
                )

        elif itype == 'particle':
            pt, col, base_r = item[2], item[3], item[4]
            r = max(1.4, base_r * depth_factor)
            alpha = int(255 * (0.3 + 0.7 * depth_factor))
            draw.ellipse(
                [pt[0] - r, pt[1] - r, pt[0] + r, pt[1] + r],
                fill=(*col, alpha)
            )
            if depth_factor > 0.6:
                glow_draw.ellipse(
                    [pt[0] - r*2.8, pt[1] - r*2.8, pt[0] + r*2.8, pt[1] + r*2.8],
                    fill=(*col, 100)
                )

    # Soft blur on glow layer
    glow_blurred = glow_im.filter(ImageFilter.GaussianBlur(radius=2.2))
    # Composite glow onto base
    final_frame = Image.alpha_composite(base_im, glow_blurred)

    # Convert to RGB with TokyoNight background
    rgb_frame = Image.new("RGB", (W, H), BG_COLOR)
    rgb_frame.paste(final_frame, mask=final_frame.split()[3])
    frames.append(rgb_frame)

out_gif = r'C:\Users\Ailyn Nicol\Desktop\Ailyn-Gomez-Dev\assets\tesseract.gif'
print(f"Saving {len(frames)} frames to {out_gif}...")
frames[0].save(
    out_gif,
    save_all=True,
    append_images=frames[1:],
    duration=45,  # 45ms per frame = ~22 FPS smooth animation
    loop=0,
    optimize=True
)
print(f"Generated enlarged Quantum Core GIF successfully: {os.path.getsize(out_gif)} bytes!")
