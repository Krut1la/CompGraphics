"""
Prog:   Lab5.py

Auth:   Oleksii Krutko, IO-z91

Desc:   Computer graphics Lab 5. 2020

"""
import copy
import math
from graphics3d import MatrixAffine4x4
from graphics3d import Vector3, BoundingBox
from GraphicsEngine3dBase import GraphicsEngine3dImageVector
from ScreenSaver import ScreenSaver, build_animation


def main():
    engine2d = GraphicsEngine3dImageVector(1024, 768, "Lab 5. Variant 10.")

    model = BoundingBox(Vector3(-150.0, -100.0, -50.0), Vector3(150.0, 100.0, 50.0)) \
        .get_model()

    rot = MatrixAffine4x4.build_rotation(math.pi/10, Vector3.unit_y())

    model_transformed = copy.deepcopy(model)
    model_transformed.transform(rot)

    model.append(model_transformed)

    boundary_box = BoundingBox(Vector3(-250.0, -200.0, -150.0), Vector3(250.0, 200.0, 150.0))
    animation = build_animation(boundary_box)

    screen_saver = ScreenSaver(engine2d, model, animation, boundary_box)

    screen_saver.start()


main()
