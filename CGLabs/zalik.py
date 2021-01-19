"""
Prog:   zalik.py

Auth:   Oleksii Krutko, IO-z91

Desc:   Computer graphics. Zalik. 2020

"""

import cv2
import numpy as np
import math
import ntpath


def process_image(impage_path, serpia_depth, add_noise):
    # Load image
    image = cv2.imread(impage_path)

    # Make some noise
    gaussian_noise = np.zeros((image.shape[0], image.shape[1]), dtype=np.uint8)
    cv2.randn(gaussian_noise, 128, serpia_depth)

    # Make serpia
    for y in range(0, image.shape[0]):
        for x in range(0, image.shape[1]):
            b = image[y, x][0]
            g = image[y, x][1]
            r = image[y, x][2]
            avrg = (int(b) + int(g) + int(r)) / 3

            if add_noise:
                b = min(avrg, 255)
                g = min(avrg + gaussian_noise[y, x], 255)
                r = min(avrg + gaussian_noise[y, x] * 2, 255)
            else:
                b = min(avrg, 255)
                g = min(avrg + serpia_depth, 255)
                r = min(avrg + serpia_depth * 2, 255)
            image[y, x] = (b, g, r)

    head, tail = ntpath.split(impage_path)
    cv2.imwrite(head + "/" + "{0}_{1}_".format(serpia_depth, add_noise) + tail, image)


def main():
    process_image("venv/ZalikResults/test_sea.jpeg", 10, False)
    process_image("venv/ZalikResults/test_sea.jpeg", 50, False)

    process_image("venv/ZalikResults/test_sea.jpeg", 50, True)



main()
