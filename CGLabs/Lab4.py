"""
Prog:   Lab4.py

Auth:   Oleksii Krutko, IO-z91

Desc:   Computer graphics Lab 4. 2020

"""

import random
import copy
import tkinter as tk
import numpy as np
from graphics3d import Vector3, BoundingBox
from GraphicsEngine3dBase import GraphicsEngine3dBase
from ScreenSaver import ScreenSaver, build_animation


class GraphicsEngine2dImage(GraphicsEngine3dBase):
    """
    Simple 3d graphics based on Tk.
    """

    def __init__(self, width, height, title):
        super(GraphicsEngine2dImage, self).__init__(width, height, title)

    def _init_ui(self):
        super(GraphicsEngine2dImage, self)._init_ui()

    def _draw_line(self, x_from, y_from, x_to, y_to, line_width, color):
        self._canvas.create_line(x_from,
                                 y_from,
                                 x_to,
                                 y_to,
                                 width=line_width,
                                 fill=color)

    def _draw_text(self, x, y, text):
        self._canvas.create_text(x, y,
                                 text=text,
                                 font=("Helvetica", 7))


def main():
    engine2d = GraphicsEngine2dImage(1024, 768, "Lab 4. Variant 10.")

    model = BoundingBox(Vector3(-150.0, -100.0, -50.0), Vector3(150.0, 100.0, 50.0))\
        .get_model()

    boundary_box = BoundingBox(Vector3(-250.0, -200.0, -150.0), Vector3(250.0, 200.0, 150.0))
    animation = build_animation(boundary_box)

    screen_saver = ScreenSaver(engine2d, model, animation, boundary_box)

    screen_saver.start()


main()
