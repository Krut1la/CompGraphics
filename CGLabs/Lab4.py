"""
Prog:   Lab4.py

Auth:   Oleksii Krutko, IO-z91

Desc:   Computer graphics Lab 4. 2020

"""

import numpy as np
from PIL import Image, ImageTk
from graphics3d import Vector3, BoundingBox
from GraphicsEngine3dBase import GraphicsEngine3dBase
from ScreenSaver import ScreenSaver, build_animation


class GraphicsEngine3dImage(GraphicsEngine3dBase):
    """
    Simple 3d graphics based on Tk.
    """

    def __init__(self, width, height, title):
        super(GraphicsEngine3dImage, self).__init__(width, height, title)

        self._canvas.update()
        self._image_width = self._canvas.winfo_width()
        self._image_height = self._canvas.winfo_height()
        # self._background = Image.open("background.png")
        self._background = Image.new("RGB", (self._image_width, self._image_height), "white")
        self._pixels = np.array(self._background)

        self._image = ImageTk.PhotoImage(image=self._background)

        self._image_on_canvas = self._canvas.create_image((self._image_width / 2, self._image_height / 2),
                                                          image=self._image)

    def _init_ui(self):
        super(GraphicsEngine3dImage, self)._init_ui()

    def update(self):
        self._background = Image.fromarray(self._pixels, mode="RGB")
        self._image = ImageTk.PhotoImage(self._background)
        self._canvas.itemconfig(self._image_on_canvas, image=self._image)

        super(GraphicsEngine3dImage, self).update()

    def clear(self):
        self._canvas.delete("labels")

        self._pixels.fill(255)

    def _draw_line(self, x_from, y_from, x_to, y_to, line_width, color_from, color_to):
        x1, y1 = x_from, y_from
        x2, y2 = x_to, y_to
        dx = x2 - x1
        dy = y2 - y1

        is_steep = abs(dy) > abs(dx)

        if is_steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2

        swapped = False
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
            swapped = True

        dx = x2 - x1
        dy = y2 - y1

        error = int(dx / 2.0)
        ystep = 1 if y1 < y2 else -1

        y = y1
        points = []
        for x in range(round(x1), round(x2) + 1):
            coord = (y, x) if is_steep else (x, y)
            points.append(coord)
            error -= abs(dy)
            if error < 0:
                y += ystep
                error += dx

        if swapped:
            points.reverse()

        for point in points:
            # TODO: interpolate color
            interpolated_pixel_color = color_from

            x = round(point[0])
            y = round(point[1])
            if 0 <= x < self._image.width() and 0 <= y < self._image.height():
                self._pixels[y, x] = interpolated_pixel_color

    def _fill_facet(self, x_1, y_1, x_2, y_2, x_3, y_3, color):
        # TODO: fill pixels
        pass

    def _draw_text(self, x, y, text):
        self._canvas.create_text(x, y,
                                 tag="labels",
                                 text=text,
                                 font=("Helvetica", 7))


def main():
    engine2d = GraphicsEngine3dImage(1024, 768, "Lab 4. Variant 10.")

    model = BoundingBox(Vector3(-150.0, -100.0, -50.0), Vector3(150.0, 100.0, 50.0)) \
        .get_model()

    boundary_box = BoundingBox(Vector3(-250.0, -200.0, -150.0), Vector3(250.0, 200.0, 150.0))
    animation = build_animation(boundary_box)

    screen_saver = ScreenSaver(engine2d, model, animation, boundary_box)

    screen_saver.start()


main()
