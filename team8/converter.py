#!/usr/bin/python

import sys
import subprocess
import urllib.request
from PIL import Image

greyscale = [ ' ', '\u2591', '\u2592', '\u2593', '\u2588' ]

(tty_h, tty_w) = subprocess.check_output(['stty', 'size']).decode("utf-8").strip().split(' ')

def convert(path):
    image = Image.open(path)

    (w, h) = image.size

    resized = image.resize((w, int(h/2)))

    resized.thumbnail((int(tty_w), int(tty_h)-1))
    (h_small, w_small) = resized.size


    bw = resized.convert('L')

    px = bw.load()

    for x in range(0, w_small):
        for y in range(0, h_small):
            pix = px[y,x]
            sys.stdout.write(greyscale[min(int(pix/51),len(greyscale)-1)])
        print()

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Usage: {} (file|http://address)".format(sys.argv[0]))
        sys.exit()

    if sys.argv[1].startswith("http://") or sys.argv[1].startswith("https://"):
        request = urllib.request.Request(sys.argv[1], headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0"})
        response = urllib.request.urlopen(request)
        with open("tmp.file", "bw") as f:
            f.write(response.read())
        convert("tmp.file")
    else:
        convert(sys.argv[1])
