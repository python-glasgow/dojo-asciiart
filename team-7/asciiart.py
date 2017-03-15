""" ASCII art generator.
"""


def load_img(filepath):
    import scipy.misc
    return scipy.misc.imread(filepath)


def rgb_to_char(rgb):
    """ Convert an (R, G, B) iterable to a single ASCII character.

    Args:
        rgb = A tuple/list (R, G, B) values.  Each in range 0-255.

    Returns:
        A single character representing this value.
    """
    # chars = list('8ZI_,  ')
    # chars = list('$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^\'.  ')
    chars = list('@%#*+=-:.  ')

    average = int(sum(rgb) // len(rgb))
    ix = int(average // 25.5)  # 255 / 10.

    return chars[ix]


def convert_to_ascii(img):
    """ Converts an image (array of RGB values) to ASCII art.

    Args:
        img = Array of RGB values representing the image.  The shape is
              [Height, Width, RGB].  Must be a Numpy array.

    Returns:
        Array of characters, shape [Height, Width].
    """
    import numpy as np

    H, W, RGB_SIZE = img.shape

    step = 10

    scaledH = H // step + 1
    scaledW = W // step + 1

    art = np.zeros((scaledH, scaledW * 2), dtype=str)
    art[:] = ' '

    for x in range(0, W, step):
        for y in range(0, H, step):
            rgb = img[y:y+step, x:x+step]
            rgb_average = np.average(np.average(rgb, axis=0), axis=0)

            chary = y // step
            charx = 2 * x // step
            art[chary, charx:charx+2] = rgb_to_char(rgb_average)
    return art


if __name__ == '__main__':
    import sys
    import os.path

    args = sys.argv
    print(args)

    if len(args) < 2 or not os.path.exists(args[1]):
        file_path = '/home/matthew/Documents/PyGla/duke.jpg'
    else:
        file_path = args[1]

    if len(args) < 3:
        output_path = 'art.txt'
    else:
        output_path = args[2]

    img = load_img(file_path)
    art = convert_to_ascii(img)

    with open(output_path, 'w') as fout:
        for row in art:
            line = ''.join(row) + '\n'
            fout.write(line)
