"""
Prog:   Lab5.py

Auth:   Oleksii Krutko, IO-z91

Desc:   Computer graphics Lab 5. 2020

"""

import numpy as np
from PIL import Image, ImageTk
from graphics3d import Vector3, BoundingBox
from GraphicsEngine3dBase import GraphicsEngine3dBase
from ScreenSaver import ScreenSaver, build_animation


# find the a & b points
def get_bezier_coef(points):
    # since the formulas work given that we have n+1 points
    # then n must be this:
    n = len(points) - 1

    # build coefficents matrix
    C = 4 * np.identity(n)
    np.fill_diagonal(C[1:], 1)
    np.fill_diagonal(C[:, 1:], 1)
    C[0, 0] = 2
    C[n - 1, n - 1] = 7
    C[n - 1, n - 2] = 2

    # build points vector
    P = [2 * (2 * points[i] + points[i + 1]) for i in range(n)]
    P[0] = points[0] + 2 * points[1]
    P[n - 1] = 8 * points[n - 1] + points[n]

    # solve system, find a & b
    A = np.linalg.solve(C, P)
    B = [0] * n
    for i in range(n - 1):
        B[i] = 2 * points[i + 1] - A[i + 1]
    B[n - 1] = (A[n - 1] + points[n]) / 2

    return A, B


# returns the general Bezier cubic formula given 4 control points
def get_cubic(a, b, c, d):
    return lambda t: np.power(1 - t, 3) * a + 3 * np.power(1 - t, 2) * t * b + 3 * (1 - t) * np.power(t,
                                                                                                      2) * c + np.power(
        t, 3) * d


# return one cubic curve for each consecutive points
def get_bezier_cubic(points):
    A, B = get_bezier_coef(points)
    return [
        get_cubic(points[i], A[i], B[i], points[i + 1])
        for i in range(len(points) - 1)
    ]


# evaluate each cubic curve on the range [0, 1] sliced in n points
def evaluate_bezier(points, n):
    curves = get_bezier_cubic(points)
    return np.array([fun(t) for fun in curves for t in np.linspace(0, 1, n)])


class GraphicsEngine3dImageVector(GraphicsEngine3dBase):
    """
    Simple 3d graphics based on Tk.
    """

    def __init__(self, width, height, title):
        super(GraphicsEngine3dImageVector, self).__init__(width, height, title)

        self._canvas.update()
        self._image_width = self._canvas.winfo_width()
        self._image_height = self._canvas.winfo_height()

        self._background = Image.new("RGB", (self._image_width, self._image_height), "white")
        self._pixels = np.array(self._background)

        self._image = ImageTk.PhotoImage(image=self._background)

        self._image_on_canvas = self._canvas.create_image((self._image_width / 2, self._image_height / 2),
                                                          image=self._image)

    def _init_ui(self):
        super(GraphicsEngine3dImageVector, self)._init_ui()

    def update(self):
        self._background = Image.fromarray(self._pixels, mode="RGB")
        self._image = ImageTk.PhotoImage(self._background)
        self._canvas.itemconfig(self._image_on_canvas, image=self._image)

        super(GraphicsEngine3dImageVector, self).update()

    def clear(self):
        self._canvas.delete("labels")

        self._pixels.fill(255)

    def _draw_line(self, x_from, y_from, x_to, y_to, line_width, color_from, color_to, transparency):
        m = np.array([[x_from, y_from],
                       [(x_from + x_to)/2, (y_from + y_to)/2],
                         [x_to, y_to]])

        points = evaluate_bezier(m, 50)

        for point in points:
            x = round(point[0])
            y = round(point[1])
            if 0 <= x < self._image.width() and 0 <= y < self._image.height():
                self._pixels[y, x] = color_from

    def _fill_facet(self, x_1, y_1, x_2, y_2, x_3, y_3, color_1, color_2, color_3, transparency):
        # m = np.array([[(x_1 + x_2)/2, (y_1 + y_2)/2],
        #              [(x_2 + x_3)/2, (y_2 + y_3)/2],
        #              [(x_3 + x_1)/2, (y_3 + y_1)/2],
        #              [(x_1 + x_2)/2, (y_1 + y_2)/2],
        #              [(x_2 + x_3) / 2, (y_2 + y_3) / 2]
        #              ])

        m = np.array([[x_1, y_1],
                     [x_2, y_2],
                     [x_3, y_3]])

        points = evaluate_bezier(m, 50)

        for point in points:
            x = round(point[0])
            y = round(point[1])
            if 0 <= x < self._image.width() and 0 <= y < self._image.height():
                self._pixels[y, x] = color_1

    def _draw_text(self, x, y, text):
        self._canvas.create_text(x, y,
                                 tag="labels",
                                 text=text,
                                 font=("Helvetica", 7))


def main():
    engine2d = GraphicsEngine3dImageVector(1024, 768, "Lab 5. Variant 10.")

    model = BoundingBox(Vector3(-150.0, -100.0, -50.0), Vector3(150.0, 100.0, 50.0)) \
        .get_model()

    boundary_box = BoundingBox(Vector3(-250.0, -200.0, -150.0), Vector3(250.0, 200.0, 150.0))
    animation = build_animation(boundary_box)

    screen_saver = ScreenSaver(engine2d, model, animation, boundary_box)

    screen_saver.start()


main()
