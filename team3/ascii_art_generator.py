from PIL import Image
import numpy as np


def to_ascii_char(value):
    """
    Assigns a symbol to a value
    :param value: int
    :return: string, the assigned symbol
    """
    if value < 64:
        return '*'
    elif value < 128:
        return '.'
    else:
        return ' '


def writer(value, file_path):
    """
    Writes the value to a text file in file_path
    :param value: string to be written
    :param file_path: string, the file_path where the value is written
    :return:
    """
    with open(file_path, 'w') as file:
        file.write(value)


def generate_art(file_path):
    """
    Generates art for an input file from file_path
    :param file_path: string
    :return:
    """
    # Read the image and convert to greyscale
    img = Image.open(file_path).convert('L')
    # Assign each image's pixel to an ascii char
    ascii_chars = [to_ascii_char(pixel) for pixel in img.getdata()]
    # Get the image matrix
    img_matrix = np.array(ascii_chars).reshape((img.size[1], img.size[0]))
    # Return string representation of the matrix
    return '\n'.join(' '.join(char for char in row) for row in img_matrix) + '\n'


def write_art(input_file, output_file):
    """
    Calls the art generator and writes the output to a file
    :param input_file: file path to be processed
    :param output_file: file path to write the output
    :return:
    """
    art = generate_art(input_file)
    writer(art, output_file)

if __name__ == '__main__':
    write_art('C:\\ascii\\team3\\tests\\python-logo.png', 'C:\\ascii\\team3\\tests\\python-logo-ascii.txt')