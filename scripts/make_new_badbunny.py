import imageio.v2 as iio
from PIL import Image, ImageDraw, ImageFont
import os

video_path = 'scripts/new_video.mp4'
out_gif = r'C:\Users\Ailyn Nicol\Desktop\Ailyn-Gomez-Dev\assets\badbunny.gif'

reader = iio.get_reader(video_path)
fps = reader.get_meta_data()['fps']
total_frames = reader.count_frames()
print(f"Video FPS: {fps}, Total frames: {total_frames}")

# Try loading font for macOS header
font = None
for fpath in ["consola.ttf", "cour.ttf", "arial.ttf"]:
    try:
        font = ImageFont.truetype(fpath, 12)
        break
    except Exception:
        pass
if font is None:
    font = ImageFont.load_default()

W, H = 370, 400
header_h = 30
radius = 10

# Create mask for rounded corners
mask = Image.new("L", (W, H), 0)
mask_draw = ImageDraw.Draw(mask)
mask_draw.rounded_rectangle([(0, 0), (W - 1, H - 1)], radius=radius, fill=255)

def build_gif_from_range(start_sec, end_sec, step=2, crop_y=45):
    start_f = int(start_sec * fps)
    end_f = min(int(end_sec * fps), total_frames)
    
    frames = []
    for f_idx in range(start_f, end_f, step):
        frame_arr = reader.get_data(f_idx)
        raw_im = Image.fromarray(frame_arr)
        # raw_im is 234 x 416
        # Crop square: 234 x 234 starting at crop_y
        crop = raw_im.crop((0, crop_y, 234, min(crop_y + 234, 416)))
        # Resize to square video area: 370 x 370
        im_video = crop.resize((W, H - header_h), Image.Resampling.LANCZOS)
        
        # Build canvas
        canvas = Image.new("RGBA", (W, H), (11, 15, 25, 255))
        draw = ImageDraw.Draw(canvas)
        
        # Header background
        draw.rectangle([(0, 0), (W, header_h)], fill=(17, 24, 39, 255))
        draw.line([(0, header_h - 1), (W, header_h - 1)], fill=(30, 41, 59, 255), width=1)
        
        # macOS Dots
        draw.ellipse([(14, 10), (24, 20)], fill=(244, 63, 94, 255))   # Red
        draw.ellipse([(29, 10), (39, 20)], fill=(234, 179, 8, 255))   # Yellow
        draw.ellipse([(44, 10), (54, 20)], fill=(16, 185, 129, 255))  # Green
        
        # Window Title
        draw.text((62, 9), "badbunny.gif", fill=(148, 163, 184, 255), font=font)
        
        # Paste video
        canvas.paste(im_video, (0, header_h))
        
        # Rounded border
        draw.rounded_rectangle([(0, 0), (W - 1, H - 1)], radius=radius, outline=(30, 41, 59, 255), width=1)
        
        canvas.putalpha(mask)
        
        # Composite to TokyoNight RGB
        rgb_frame = Image.new("RGB", (W, H), (11, 15, 25))
        rgb_frame.paste(canvas, mask=canvas.split()[3])
        frames.append(rgb_frame)
        
    return frames

# Let's inspect the first 4.5 seconds (frames 0 to 135 with step 2 = ~45 frames at 15 FPS)
frames = build_gif_from_range(0.0, 4.0, step=2, crop_y=40)
print(f"Rendered {len(frames)} frames")

# Save as optimized GIF
duration_ms = int(1000 / (fps / 2)) # ~66ms per frame = 15 FPS
frames[0].save(
    out_gif,
    save_all=True,
    append_images=frames[1:],
    duration=duration_ms,
    loop=0,
    optimize=True
)

print(f"Generated {out_gif}, size: {os.path.getsize(out_gif)} bytes")
