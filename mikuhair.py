#    mikuhair.py : Visualize Miku's hair color
#    Copyright (C) 2025  Andrew Potter
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

from PIL import Image, ImageDraw, ImageFont

def hex_to_rgb(hex_code):
    """Converts a hex color code to an RGB tuple."""
    hex_code = hex_code.lstrip('#')
    return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))

def blend_colors(c1, c2, c3, a, b, c):
    """Blends three RGB colors using barycentric coordinates."""
    r = int(a * c1[0] + b * c2[0] + c * c3[0])
    g = int(a * c1[1] + b * c2[1] + c * c3[1])
    b = int(a * c1[2] + b * c2[2] + c * c3[2])
    return (r, g, b)

def barycentric_coords(p, a, b, c):
    """Calculates barycentric coordinates of point p relative to triangle a, b, c."""
    denominator = (b[1] - c[1]) * (a[0] - c[0]) + (c[0] - b[0]) * (a[1] - c[1])
    alpha = ((b[1] - c[1]) * (p[0] - c[0]) + (c[0] - b[0]) * (p[1] - c[1])) / denominator
    beta = ((c[1] - a[1]) * (p[0] - c[0]) + (a[0] - c[0]) * (p[1] - c[1])) / denominator
    gamma = 1.0 - alpha - beta
    return alpha, beta, gamma

teal_hex = '#008080'
#cyan_hex = '#00FFFF'
turquoise_hex = '#40E0D0'
miku_hex = '#39C5BB'

teal_rgb = hex_to_rgb(teal_hex)
turquoise_rgb = hex_to_rgb(turquoise_hex)
miku_rgb = hex_to_rgb(miku_hex)

# Create an image and a drawing object
width, height = 1200, 1200
img = Image.new('RGBA', (width, height), (0,0,0,0))
pixels = img.load()
draw = ImageDraw.Draw(img) # Initialize ImageDraw for text and shapes

margin = 100
miku_v = (width // 2, margin)
turquoise_v = (margin, height - margin)
teal_v = (width - margin, height - margin)

# Loop through each pixel and color it if it's inside the triangle
for x in range(width):
    for y in range(height):
        alpha, beta, gamma = barycentric_coords((x, y), teal_v, turquoise_v, miku_v)

        # Check if the point is inside the triangle
        if 0 <= alpha <= 1 and 0 <= beta <= 1 and 0 <= gamma <= 1:
            # Blend the colors using the barycentric coordinates
            r = int(alpha * teal_rgb[0] + beta * turquoise_rgb[0] + gamma * miku_rgb[0])
            g = int(alpha * teal_rgb[1] + beta * turquoise_rgb[1] + gamma * miku_rgb[1])
            b = int(alpha * teal_rgb[2] + beta * turquoise_rgb[2] + gamma * miku_rgb[2])

            pixels[x, y] = (r, g, b)


# --- Add Labels ---

# Try to load a default font. If it fails, use Pillow's default font.
try:
    font = ImageFont.truetype("/usr/share/fonts/adwaita-sans-fonts/AdwaitaSans-Regular.ttf", 30) # You might need to change "arial.ttf"
except IOError:
    font = ImageFont.load_default()
    print("Could not load 'arial.ttf'. Using default font. Labels might look different.")

# Label data: (text, hex_color, vertex_position)
labels_data = [
    ("Teal\n" + teal_hex, teal_rgb, teal_v, "bottom_right"),
    ("Turquoise\n" + turquoise_hex, turquoise_rgb, turquoise_v, "bottom_left"),
    ("Hatsune Miku\n" + miku_hex, miku_rgb, miku_v, "top"),
]

for label_text, bg_color_rgb, vertex_pos, position_key in labels_data:
    # Get text size
    bbox = draw.textbbox((0,0), label_text, font=font)
    #bbox = font.getbbox(label_text)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1] + 15

    # Calculate label background rectangle position
    padding = 10
    if position_key == "top":
        rect_x1 = vertex_pos[0] - text_width // 2 - padding
        rect_y1 = vertex_pos[1] - text_height - 2 * padding # Above the vertex
        rect_x2 = vertex_pos[0] + text_width // 2 + padding
        rect_y2 = vertex_pos[1] - padding
    elif position_key == "bottom_left":
        rect_x1 = vertex_pos[0] - padding
        rect_y1 = vertex_pos[1] + padding
        rect_x2 = vertex_pos[0] + text_width + padding
        rect_y2 = vertex_pos[1] + text_height + 2 * padding
    elif position_key == "bottom_right":
        rect_x1 = vertex_pos[0] - text_width - padding
        rect_y1 = vertex_pos[1] + padding
        rect_x2 = vertex_pos[0] + padding
        rect_y2 = vertex_pos[1] + text_height + 2 * padding

    # Draw background rectangle
    draw.rectangle([rect_x1, rect_y1, rect_x2, rect_y2], fill=bg_color_rgb)

    # Calculate text position (centered within its background)
    text_x = rect_x1 + (rect_x2 - rect_x1 - text_width) // 2
    text_y = rect_y1 + (rect_y2 - rect_y1 - text_height) // 2

    # Draw text (white for contrast)
    draw.text((text_x, text_y), label_text, font=font, fill=(255, 0, 164), align="center")

# --- Add Color Key Rectangles ---
key_width = 30
key_height = 30
key_spacing = 0
key_y_miku = height - key_height - 700 - key_height
key_width_miku = key_width * 2 + key_spacing

key_y = height - key_height - 700
key_x_start = width - 3 * key_width - 3 * key_spacing - 200

# Draw Miku's hair color key
draw.rectangle([key_x_start, key_y_miku, key_x_start + key_width_miku, key_y_miku + key_height], fill=miku_rgb + (255,))

# Draw Turquoise key
draw.rectangle([key_x_start, key_y, key_x_start + key_width, key_y + key_height], fill=turquoise_rgb + (255,))

# Draw Teal key
draw.rectangle([key_x_start + key_width + key_spacing, key_y, key_x_start + 2*key_width + key_spacing, key_y + key_height], fill=teal_rgb + (255,))


# Save the image
img.save('miku_teal_turquoise.png')
print("Simplified color triangle gradient image saved as 'miku_teal_turquoise.png'")
