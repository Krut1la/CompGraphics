"""
Prog:   Lab3.py

Auth:   Oleksii Krutko, IO-z91

Desc:   Computer graphics Lab 3. 2020

"""

from GraphicsEngine3dBase import GraphicsEngine3dBase, color_rgb
from ScreenSaver import ScreenSaver, build_animation
from graphics3d import Vector3, BoundingBox


class GraphicsEngine3dCanvas(GraphicsEngine3dBase):
    """
    Simple 3d graphics based on Tk.
    """

    def __init__(self, width, height, title):
        super(GraphicsEngine3dCanvas, self).__init__(width, height, title)

    def _init_ui(self):
        super(GraphicsEngine3dCanvas, self)._init_ui()

    def _draw_line(self, x_from, y_from, x_to, y_to, z_from, z_to, line_width, color_from, color_to, transparency):
        # this engine does not support color gradients, so we pick color from
        color_str = color_rgb(min(round(color_from[0] + 255 * transparency), 255),
                              min(round(color_from[1] + 255 * transparency), 255),
                              min(round(color_from[2] + 255 * transparency), 255))

        self._canvas.create_line(x_from,
                                 y_from,
                                 x_to,
                                 y_to,
                                 width=line_width,
                                 fill=color_str)

    def _draw_text(self, x, y, text):
        self._canvas.create_text(x, y,
                                 text=text,
                                 font=("Helvetica", 7))


def main():
    engine2d = GraphicsEngine3dCanvas(1024, 768, "Lab 3. Variant 10.")

    model = BoundingBox(Vector3(-150.0, -100.0, -50.0), Vector3(150.0, 100.0, 50.0))\
        .get_model()

    boundary_box = BoundingBox(Vector3(-250.0, -200.0, -150.0), Vector3(250.0, 200.0, 150.0))
    animation = build_animation(boundary_box)

    screen_saver = ScreenSaver(engine2d, model, animation, boundary_box)

    screen_saver.start()


main()
