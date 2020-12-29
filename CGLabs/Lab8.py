"""
Prog:   Lab8.py

Auth:   Oleksii Krutko, IO-z91

Desc:   Computer graphics Lab 8. 2020

"""

import cv2
import numpy as np


def main():

    image = cv2.imread("venv/Lab8Results/test_fruits.jpeg")
    grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("venv/Lab8Results/grey_test_fruits.jpeg", grey)

    gaussian_noise = np.zeros((image.shape[0], image.shape[1]), dtype=np.uint8)
    cv2.randn(gaussian_noise, 128, 0)
    # grey_noise = grey + gaussian_noise
    grey_noise = grey

    cv2.imwrite("venv/Lab8Results/noise.jpeg", gaussian_noise)
    cv2.imwrite("venv/Lab8Results/noise_grey_test_fruits.jpeg", grey_noise)

    grey_noise_bgr = cv2.cvtColor(grey_noise, cv2.COLOR_GRAY2BGR)
    grey_noise_hsv = cv2.cvtColor(grey_noise_bgr, cv2.COLOR_BGR2HSV)
    grey_noise_hsv[:, :, 2] += 0
    grey_noise_brightness = cv2.cvtColor(grey_noise_hsv, cv2.COLOR_HSV2BGR)

    cv2.imwrite("venv/Lab8Results/noise_grey_brightness_test_fruits.jpeg", grey_noise_brightness)

    grey_noise_brightness_improved = cv2.detailEnhance(grey_noise_brightness, sigma_s=10, sigma_r=1.5)
    grey_noise_brightness_improved = cv2.cvtColor(grey_noise_brightness_improved, cv2.COLOR_BGR2GRAY)
    grey_noise_brightness_improved = cv2.adaptiveThreshold(grey_noise_brightness_improved, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    cv2.imwrite("venv/Lab8Results/noise_grey_brightness_improved_test_fruits.jpeg", grey_noise_brightness_improved)



    contours, hierarchy = cv2.findContours(grey_noise_brightness_improved.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    total = 0

    grey_noise_brightness_improved.fill(255)
    for contour in contours:
        c_len = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * c_len, True)
        cv2.drawContours(image, [approx], -1, (0, 255, 0), 4)
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 1)

    cv2.imwrite("venv/Lab8Results/noise_grey_brightness_improved_contours_test_fruits.jpeg", image)




main()
