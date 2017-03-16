from bisect import bisect_left
from functools import partial
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import string


# Trim off non space invisibles
ACCEPTABLE_CHARS = string.printable[:-5]
GRID_X = 8
GRID_Y = 8


def classify_chars():
    char_dict = {}
    for c in ACCEPTABLE_CHARS:
        img = Image.new('L', (GRID_X, GRID_Y), (255))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("FreeMono.ttf", 8)
        draw.text((0, 0), c, (0), font=font)
        char_dict[luminescence(img)] = c
    normalised_keys = [(char_dict[k], n * (255/len(char_dict))) for n, k in enumerate(sorted(char_dict))]
    normalised_char_dict = {nk[1]: nk[0] for nk in normalised_keys}
    return normalised_char_dict


def nearest_match(iterable, f):
    """ Returns the key for the character closest to the given float `f`'s luminescence """
    pos = bisect_left(iterable, f)
    if pos == 0:
        return iterable[0]
    if pos == len(iterable):
        return iterable[-1]
    before = iterable[pos - 1]
    after = iterable[pos]
    if after - f < f - before:
        return after
    else:
        return before


def greyscale(file_path):
    """ Returns a greyscale version of the image at `file_path`

    Parameters
    ----------
    file_path: str
        path to the image file under operation

    Returns
    -------
    PIL.Image

    """
    return Image.open(file_path).convert('L')


def char_to_image(char):
    img = Image.new('L', (GRID_X, GRID_Y))
    d = ImageDraw.Draw(img)
    d.text((GRID_X, GRID_Y), char)
    return img


def image_to_tiles(i):
    """ Given a PIL.Image returns a list of tiles conforming to the global x, y values.
    
    THIS IS WHAT WE DID AT THE DOJO BUT IT DOESN'T WORK SO WELL!

    Parameters
    ----------
    PIL.Image
        The image we will break up.

    Returns
    -------
    list
        A list of PIL.Image objects interspersed with '\n' characters to indicate line breaks

    """
    width, height = i.size
    range_x = width // GRID_X
    range_y = width // GRID_Y
    values = []
    for y in range(range_y):
        for x in range(range_x):
            bounding = (x * GRID_X, y * GRID_Y, x *
                        GRID_X + GRID_X, y * GRID_Y + GRID_Y)
            tile = i.crop(bounding)
            values.append(tile)
        values.append('\n')
    return values


def luminescence(i):
    """ THIS IS WHAT WE DID AT THE DOJO BUT IT DOESN'T WORK SO WELL! """
    divisor = GRID_X * GRID_Y
    total = 0
    for x in range(GRID_X):
        for y in range(GRID_Y):
            total += i.getpixel((x, y))
    return total / divisor


def main(path_to_image, max_width):
    """ Added after dojo as we didn't finish. The numpy stuff is new after seeing that
    our approach didn't give great images """
    ### Assign the characters to greyscale values
    char_dict = classify_chars()
    char_keys = [key for key in char_dict]
    char_keys.sort()
    ### End assign the characters to greyscale values
    ### Manipulate the image
    gscale = greyscale(path_to_image)
    width_scale = (max_width/(float(gscale.size[0])))
    horizontal_scale = int((float(gscale.size[1])*float(width_scale)))
    gscale = gscale.resize((max_width, horizontal_scale), Image.ANTIALIAS)
    ### End manipulate the image
    ### Numpy it!
    image_array = np.array(gscale)
    to_float_keys = partial(nearest_match, char_keys)
    f = np.vectorize(to_float_keys)
    image_array = f(image_array)
    to_chars = lambda c: char_dict[c]
    g = np.vectorize(to_chars)
    image_array = g(image_array)
    ### End numpy it!
    print('\n'.join([''.join(row) for row in image_array]))
