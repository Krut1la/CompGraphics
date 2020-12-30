"""
Prog:   Lab8.py

Auth:   Oleksii Krutko, IO-z91

Desc:   Computer graphics Lab 8. 2020

"""

import cv2
import numpy as np


def main():
    # Create initial gray image
    image = cv2.imread("venv/Lab8Results/test_sea.jpeg")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("venv/Lab8Results/gray_sea.jpeg", gray)

    # Make some noise
    gaussian_noise = np.zeros((image.shape[0], image.shape[1]), dtype=np.uint8)
    cv2.randn(gaussian_noise, 128, 5)

    gray_noise = gray + gaussian_noise

    cv2.imwrite("venv/Lab8Results/noise.jpeg", gaussian_noise)
    cv2.imwrite("venv/Lab8Results/noise_gray_sea.jpeg", gray_noise)

    # Change brighness
    gray_noise_bgr = cv2.cvtColor(gray_noise, cv2.COLOR_GRAY2BGR)
    gray_noise_hsv = cv2.cvtColor(gray_noise_bgr, cv2.COLOR_BGR2HSV)
    gray_noise_hsv[:, :, 2] += 50
    gray_noise_brightness = cv2.cvtColor(gray_noise_hsv, cv2.COLOR_HSV2BGR)

    cv2.imwrite("venv/Lab8Results/noise_gray_brightness_sea.jpeg", gray_noise_brightness)

    # Apply gray level threshold for better edge detection
    gray_noise_brightness_improved_edged = cv2.Canny(gray_noise_brightness, 40, 200)
    cv2.imwrite("venv/Lab8Results/noise_grey_brightness_edged_sea.jpeg", gray_noise_brightness_improved_edged)

    # Detect edges
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    closed = cv2.morphologyEx(gray_noise_brightness_improved_edged, cv2.MORPH_CLOSE, kernel)
    cv2.imwrite("venv/Lab8Results/noise_gray_brightness_edged_closed_sea.jpeg", closed)

    # Get contours
    contours, hierarchy = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find stars. Supposed to have 5*2 points
    for contour in contours:
        c_len = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.03 * c_len, True)
        x, y, w, h = cv2.boundingRect(contour)

        if len(approx) == 10:
            cv2.drawContours(image, [approx], -1, (0, 0, 255), 1)
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            break

    # Store final results on color image
    cv2.imwrite("venv/Lab8Results/noise_gray_brightness_improved_contours_test_fruits.jpeg", image)


main()
