# -*- coding: utf-8 -*-

"""Python3.6 script to print an image as ascii art.

Remove f-string print statements for other Python versions.
"""

import sys

from PIL import Image

ASCII_CHARS = ['#', '?', '%', '@', 'S', '+', '-', '*', ':', ',', '.']
EMOJI = ['🎥', '🌑', '🦃', '👽', '🐦', '🐰', '🐭', '👻']

W_SCALE = 0.125
H_SCALE = 0.125


def main(image_file, characters, w_scale, h_scale):
    img = Image.open(image_file)
    print(f"Original image {img.size} {img.format} {img.mode}")

    gray = img.convert('L')
    print(f"Grayscale image {gray.size} {gray.format} {gray.mode}")

    width, height = gray.size
    resized = gray.resize((int(width * w_scale), int(height * h_scale)))
    print(f"Resized image {resized.size} {resized.format} {resized.mode}")

    width, height = resized.size

    num_colors = len(characters)

    for y in range(height):
        line = ''
        for x in range(width):
            v = resized.getpixel((x, y))
            line += characters[v * num_colors // 255] + ' '
        print(line)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit("Please specify an image file!")

    # Change this to EMOJI if you want :)
    main(sys.argv[1], ASCII_CHARS, W_SCALE, H_SCALE)
