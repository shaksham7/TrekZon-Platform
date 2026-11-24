"""
compress_images.py

One-time helper: converts large PNG images in static/images/ to compressed JPEG,
dramatically reducing file size with no meaningful visual quality loss for
photographic trek images (PNG is lossless and inefficient for photos; JPEG
is designed for exactly this).

Run from your project folder (venv activated):

    python compress_images.py

This will:
- Convert every .png in static/images/ to a compressed .jpg
- Resize any image wider than 1600px down to 1600px (plenty for web display)
- Delete the original .png after a successful conversion
- Print a before/after size comparison

You'll need Pillow installed:
    pip install Pillow --break-system-packages
"""

import os
from PIL import Image

IMAGES_DIR = os.path.join('static', 'images')
MAX_WIDTH = 1600
JPEG_QUALITY = 82


def compress_images():
    if not os.path.isdir(IMAGES_DIR):
        print(f"Could not find {IMAGES_DIR} -- run this script from your TrekZon project root.")
        return

    total_before = 0
    total_after = 0

    for filename in os.listdir(IMAGES_DIR):
        if not filename.lower().endswith('.png'):
            continue

        png_path = os.path.join(IMAGES_DIR, filename)
        jpg_filename = os.path.splitext(filename)[0] + '.jpg'
        jpg_path = os.path.join(IMAGES_DIR, jpg_filename)

        size_before = os.path.getsize(png_path)

        img = Image.open(png_path)
        # Flatten transparency onto white, since JPEG has no alpha channel
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1])
            img = background
        else:
            img = img.convert('RGB')

        if img.width > MAX_WIDTH:
            new_height = int(img.height * (MAX_WIDTH / img.width))
            img = img.resize((MAX_WIDTH, new_height), Image.LANCZOS)

        img.save(jpg_path, 'JPEG', quality=JPEG_QUALITY, optimize=True)
        size_after = os.path.getsize(jpg_path)

        os.remove(png_path)

        total_before += size_before
        total_after += size_after
        print(f"{filename} -> {jpg_filename}: {size_before/1024:.0f} KB -> {size_after/1024:.0f} KB")

    print()
    print(f"Total: {total_before/1024/1024:.2f} MB -> {total_after/1024/1024:.2f} MB")
    print()
    print("IMPORTANT: Update any template/database references from '.png' to '.jpg' for these files.")


if __name__ == '__main__':
    compress_images()
