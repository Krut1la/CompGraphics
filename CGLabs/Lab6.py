"""
Prog:   Lab6.py

Auth:   Oleksii Krutko, IO-z91

Desc:   Computer graphics Lab 6. 2020

"""

from graphics3d import Vector3, BoundingBox
from GraphicsEngine3dBase import GraphicsEngine3dImageVectorFractal
from ScreenSaver import ScreenSaver, build_animation


def main():
    engine2d = GraphicsEngine3dImageVectorFractal(1024, 768, "Lab 6. Variant 10.")

    model = BoundingBox(Vector3(-150.0, -100.0, -50.0), Vector3(150.0, 100.0, 50.0)) \
        .get_model()

    boundary_box = BoundingBox(Vector3(-250.0, -200.0, -150.0), Vector3(250.0, 200.0, 150.0))
    animation = build_animation(boundary_box)

    screen_saver = ScreenSaver(engine2d, model, animation, boundary_box)

    screen_saver.start()


main()
