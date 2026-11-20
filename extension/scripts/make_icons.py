#!/usr/bin/env python3
"""
High-Fidelity Multi-Resolution PNG Icon Renderer for OmniSnap
Renders squircle chassis, viewfinder reticle brackets, lens bezel, and 6-blade aperture iris.
Generates: 16x16, 32x32, 48x48, 128x128, and 512x512 PNG assets.
"""

import struct
import zlib
import os
import math

def create_png(width, height, pixels):
    raw_data = bytearray()
    for row in pixels:
        raw_data.append(0) # Filter byte: None
        for r, g, b, a in row:
            raw_data.extend((r, g, b, a))
            
    compressed = zlib.compress(bytes(raw_data), 9)
    
    png = bytearray(b"\x89PNG\r\n\x1a\n")
    
    # IHDR
    ihdr_data = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)
    ihdr_crc = zlib.crc32(b"IHDR" + ihdr_data)
    png.extend(struct.pack(">I", len(ihdr_data)))
    png.extend(b"IHDR")
    png.extend(ihdr_data)
    png.extend(struct.pack(">I", ihdr_crc))
    
    # IDAT
    idat_crc = zlib.crc32(b"IDAT" + compressed)
    png.extend(struct.pack(">I", len(compressed)))
    png.extend(b"IDAT")
    png.extend(compressed)
    png.extend(struct.pack(">I", idat_crc))
    
    # IEND
    iend_crc = zlib.crc32(b"IEND")
    png.extend(struct.pack(">I", 0))
    png.extend(b"IEND")
    png.extend(struct.pack(">I", iend_crc))
    
    return bytes(png)

def render_omni_icon(size):
    pixels = []
    center = size / 2.0
    
    # Dimensions proportional to size
    corner_radius = size * 0.22
    max_d = center - corner_radius
    bezel_radius = size * 0.34
    inner_bezel = size * 0.31
    aperture_radius = size * 0.27
    pupil_radius = size * 0.10
    spark_radius = size * 0.04
    reticle_inset = size * 0.12
    reticle_len = size * 0.08
    reticle_w = max(1.0, size * 0.02)
    
    for y in range(size):
        row = []
        for x in range(size):
            dx = abs(x - center + 0.5)
            dy = abs(y - center + 0.5)
            
            # Squircle bounds
            in_box = True
            if dx > max_d and dy > max_d:
                cdist = math.hypot(dx - max_d, dy - max_d)
                if cdist > corner_radius:
                    in_box = False
            elif dx > center or dy > center:
                in_box = False
                
            if not in_box:
                row.append((0, 0, 0, 0))
                continue
                
            # Base Gradient: Electric Indigo (#4F46E5) -> Violet (#7C3AED) -> Cyan (#06B6D4)
            diag = (x + y) / (2.0 * size)
            if diag < 0.5:
                # Indigo to Violet
                t = diag * 2.0
                r = int(79 + t * (124 - 79))
                g = int(70 + t * (58 - 70))
                b = int(229 + t * (237 - 229))
            else:
                # Violet to Cyan
                t = (diag - 0.5) * 2.0
                r = int(124 + t * (6 - 124))
                g = int(58 + t * (182 - 58))
                b = int(237 + t * (212 - 237))
            a = 255

            dist = math.hypot(x - center + 0.5, y - center + 0.5)

            # Viewfinder Reticles (Corners)
            px = x if x < center else (size - 1 - x)
            py = y if y < center else (size - 1 - y)
            is_reticle = False
            if (px >= reticle_inset and px <= reticle_inset + reticle_len and abs(py - reticle_inset) <= reticle_w) or \
               (py >= reticle_inset and py <= reticle_inset + reticle_len and abs(px - reticle_inset) <= reticle_w):
                is_reticle = True

            if is_reticle:
                r, g, b = 224, 242, 254 # Pale Ice Blue

            # Camera Outer Bezel
            if dist <= bezel_radius and dist > inner_bezel:
                r, g, b = 15, 23, 42 # Dark Slate 900
            elif dist <= inner_bezel and dist > aperture_radius:
                r, g, b = 30, 41, 59 # Slate 800

            # Aperture Iris area
            elif dist <= aperture_radius and dist > pupil_radius:
                # 6-blade rotational gradient effect
                angle = (math.atan2(y - center + 0.5, x - center + 0.5) + math.pi) % (math.pi / 3.0)
                blade_t = angle / (math.pi / 3.0)
                # Alternating vibrant blades
                sector = int(((math.atan2(y - center + 0.5, x - center + 0.5) + math.pi) / (math.pi / 3.0))) % 2
                if sector == 0:
                    r = int(56 + blade_t * (255 - 56))
                    g = int(189 + blade_t * (255 - 189))
                    b = 255
                else:
                    r = int(79 + blade_t * (6 - 79))
                    g = int(70 + blade_t * (182 - 70))
                    b = int(229 + blade_t * (212 - 229))

            # Center Pupil
            elif dist <= pupil_radius:
                if dist <= spark_radius:
                    r, g, b = 255, 255, 255 # Lens reflection gleam
                else:
                    # Glowing Cyan Pupil
                    t_pupil = dist / pupil_radius
                    r = int(34 + t_pupil * (6 - 34))
                    g = int(211 + t_pupil * (182 - 211))
                    b = int(238 + t_pupil * (212 - 238))

            row.append((r, g, b, a))
        pixels.append(row)
        
    return create_png(size, size, pixels)

def main():
    icons_dir = "extension/icons"
    store_dir = "store"
    os.makedirs(icons_dir, exist_ok=True)
    os.makedirs(store_dir, exist_ok=True)
    
    # Extension icons
    for s in [16, 32, 48, 128]:
        data = render_omni_icon(s)
        path = os.path.join(icons_dir, f"icon{s}.png")
        with open(path, "wb") as f:
            f.write(data)
        print(f"Rendered {path} ({s}x{s}) - {len(data)} bytes")
        
    # High-resolution 512x512 Store Master
    store_512 = render_omni_icon(512)
    path_512 = os.path.join(store_dir, "icon512.png")
    with open(path_512, "wb") as f:
        f.write(store_512)
    print(f"Rendered {path_512} (512x512) - {len(store_512)} bytes")

if __name__ == "__main__":
    main()
