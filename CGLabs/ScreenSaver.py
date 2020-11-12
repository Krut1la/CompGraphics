import copy
import random
from math import pi, sin

from GraphicsEngine3dBase import color_rgb
from graphics3d import Model, Vector3, Vertex3d, Edge, MatrixAffine4x4


class AnimationFrame(object):
    """
    Represents a single frame in an animation sequence.
    """
    def __init__(self, time_delay, color, transformation):
        self.time_delay = time_delay
        self.color = color
        self.transformation = transformation


class Animation(object):
    """
    Represents animation as a sequence of frames.
    """
    def __init__(self, cyclic, frames):
        self._cyclic = cyclic
        self._frames = frames
        self.position = 0

    def get_model(self):
        model = Model()
        prev_vid = -1
        prev_point = None
        for frame in self._frames:

            point = Vector3.zero()
            point.transform(frame.transformation)

            if prev_vid == -1:
                vid = model.add_vertex(Vertex3d(point))
                prev_point = copy.deepcopy(point)
                prev_vid = vid
            else:
                segment_dist = prev_point.dist(point)
                if segment_dist > 50.0:
                    vid = model.add_vertex(Vertex3d(point))
                    model.add_edge(Edge(prev_vid, vid))
                    prev_point = copy.deepcopy(point)
                    prev_vid = vid

        return model

    def get_frame(self):
        frame = self._frames[self.position]
        self.position = self.position + 1

        if self.position == len(self._frames):
            if self._cyclic:
                self.position = 0
            else:
                self.position = self.position - 1

        return frame


class ScreenSaver(object):
    """
    Represents a simple screen saver according to Lab 3. Variant 10.
    """
    def __init__(self, engine, model, animation, boundary_box):
        self._engine = engine
        self._model = copy.deepcopy(model)
        self._boundary_box_model = boundary_box.get_model()
        self._trajectory_model = animation.get_model()
        self._animation = animation

        self._engine.update()
        self._draw_frame(self._animation.get_frame())

    def _animate(self):
        if self._engine.is_animating.get():
            self._draw_frame(self._animation.get_frame())

        self._engine.after(20, self._animate)

    def _draw_frame(self, frame):
        if self._model is not None:
            self._engine.clear()

            if self._engine.show_axes.get():
                self._engine.draw_axes()

            if self._engine.show_debug.get():
                self._engine.draw_model(self._boundary_box_model, 1, "gray", True)
                self._engine.draw_model(self._trajectory_model, 5, "red", True)

            model = copy.deepcopy(self._model)
            model.transform(frame.transformation)

            self._engine.draw_model(model, 3, frame.color,  self._engine.show_debug.get())
            self._engine.update()

    def start(self):
        self._engine.after(1, self._animate)
        self._engine.show()

    def stop(self):
        pass


def build_animation(boundary_box):
    """

    :param boundary_box:
    :return:
    """
    frames = []

    start_point = Vector3(0.0, 0.0, 0.0)
    direction = Vector3(1.0, 1.0, 1.0)
    direction_inc = 1.0

    current_position = copy.deepcopy(start_point)

    for i in range(0, 2000):
        while True:
            new_position = current_position + direction * direction_inc

            if not boundary_box.is_point_in(new_position):
                ort_dir = Vector3(random.random(), random.random(), random.random())
                ort_dir = ort_dir.normalize()
                direction.transform(MatrixAffine4x4.build_rotation(random.random() * pi / 3 + pi, ort_dir))
            else:
                current_position = new_position
                break

        trans = MatrixAffine4x4.build_translation(current_position)
        rot = MatrixAffine4x4.build_rotation(2 * i * pi / 300, Vector3.unit_z())
        color = color_rgb(round(abs(sin(i / 100)) * 255), round(abs(sin(i / 100)) * 255), 255)
        time_delay = 100
        frame = AnimationFrame(time_delay, color, rot * trans)
        frames.append(frame)

    return Animation(True, frames)