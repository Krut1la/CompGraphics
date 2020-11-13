"""
Prog:   graphics3d.py

Auth:   Oleksii Krutko, IO-z91

Desc:   Computer graphics Labs. 2020

Linear algebra and basic 3d objects

"""

from math import sqrt, cos, sin

import numpy as np


class Transformable(object):
    """
    Interface for geometry objects that can be transformed.
    """

    def transform(self, matrix):
        """
        Uses matrix operations to transform.
        :param matrix: transformation matrix
        :return:
        """
        pass

    def get_transformed(self, matrix):
        """
        Uses matrix operations to transform.
        :param matrix: transformation matrix
        :return:
        """
        pass


class Vector3(Transformable):
    """
    Represents 3-vector with standard operations on it.
    """

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    @staticmethod
    def unit_x():
        return Vector3(1.0, 0.0, 0.0)

    @staticmethod
    def unit_y():
        return Vector3(0.0, 1.0, 0.0)

    @staticmethod
    def unit_z():
        return Vector3(0.0, 0.0, 1.0)

    @staticmethod
    def zero():
        return Vector3(0.0, 0.0, 0.0)

    def dist(self, other):
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2)

    def length(self):
        return sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def normalize(self):
        length = self.length()
        if length == 0.0:
            raise
        return self * (1 / length)

    def cross(self, vector):
        return Vector3(self.y * vector.z - self.z * vector.y,
                       self.z * vector.x - self.x * vector.z,
                       self.x * vector.y - self.y * vector.x)

    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        if isinstance(other, float):
            return Vector3(self.x * other, self.y * other, self.z * other)

    def neg(self):
        return Vector3(-self.x, -self.y, -self.z)

    def transform(self, matrix):
        vector4 = np.array([self.x, self.y, self.z, 1.0])
        vector4.dot(matrix.data, vector4)
        self.x = vector4[0] / vector4[3]
        self.y = vector4[1] / vector4[3]
        self.z = vector4[2] / vector4[3]

    def get_transformed(self, matrix):
        vector4 = np.array([self.x, self.y, self.z, 1.0])
        vector4.dot(matrix.data, vector4)
        return Vector3(vector4[0] / vector4[3], vector4[1] / vector4[3], vector4[2] / vector4[3])


class MatrixAffine4x4(object):
    """
    Represents affine matrix with standard operations.
    """

    def __init__(self):
        self.data = np.array([[1.0, 0.0, 0.0, 0.0],
                              [0.0, 1.0, 0.0, 0.0],
                              [0.0, 0.0, 1.0, 0.0],
                              [0.0, 0.0, 0.0, 1.0]])

    def __mul__(self, other):
        new_matrix = MatrixAffine4x4()
        new_matrix.data = self.data.dot(other.data)
        return new_matrix

    @staticmethod
    def build_identity():
        m = MatrixAffine4x4()
        m.data = np.array([[1.0, 0.0, 0.0, 0.0],
                           [0.0, 1.0, 0.0, 0.0],
                           [0.0, 0.0, 1.0, 0.0],
                           [0.0, 0.0, 0.0, 1.0]])
        return m

    @staticmethod
    def build_xz_reflection():
        m = MatrixAffine4x4()
        m.data = np.array([[1.0, 0.0, 0.0, 0.0],
                           [0.0, -1.0, 0.0, 0.0],
                           [0.0, 0.0, 1.0, 0.0],
                           [0.0, 0.0, 0.0, 1.0]])
        return m

    @staticmethod
    def build_xy_reflection():
        m = MatrixAffine4x4()
        m.data = np.array([[1.0, 0.0, 0.0, 0.0],
                           [0.0, 1.0, 0.0, 0.0],
                           [0.0, 0.0, -1.0, 0.0],
                           [0.0, 0.0, 0.0, 1.0]])
        return m

    @staticmethod
    def build_xy_perspective_proj(p, q, r):
        m = MatrixAffine4x4()
        m.data = np.array([[1.0, 0.0, 0.0, p],
                           [0.0, 1.0, 0.0, q],
                           [0.0, 0.0, 0.0, r],
                           [0.0, 0.0, 0.0, 1.0]])
        return m

    @staticmethod
    def build_orthogonal_proj():
        m = MatrixAffine4x4()
        m.data = np.array([[1.0, 0.0, 0.0, 0.0],
                           [0.0, 1.0, 0.0, 0.0],
                           [0.0, 0.0, 0.0, 0.0],
                           [0.0, 0.0, 0.0, 1.0]])
        return m

    @staticmethod
    def build_axonometric_proj(phi, eta):
        m = MatrixAffine4x4()
        m1 = np.array([[cos(phi), 0.0, -sin(phi), 0.0],
                       [0.0, 1.0, 0.0, 0.0],
                       [sin(phi), 0.0, cos(phi), 0.0],
                       [0.0, 0.0, 0.0, 1.0]])

        m2 = np.array([[1.0, 0.0, 0.0, 0.0],
                       [0.0, cos(eta), sin(eta), 0.0],
                       [0.0, -sin(eta), cos(eta), 0.0],
                       [0.0, 0.0, 0.0, 1.0]])

        m.data = m1.dot(m2).dot(MatrixAffine4x4.build_orthogonal_proj().data)

        return m

    @staticmethod
    def build_xy_orthograph_proj():
        m = MatrixAffine4x4()
        m.data = np.array([[1.0, 0.0, 0.0, 0.0],
                           [0.0, 0.0, 0.0, 0.0],
                           [0.0, -1.0, 0.0, 0.0],
                           [0.0, 0.0, 0.0, 1.0]])
        return m

    @staticmethod
    def build_rotation(angle, axis):
        s = axis.x ** 2 + axis.y ** 2 + axis.z ** 2
        sq = sqrt(s)
        n1 = axis.x / sq
        n2 = axis.y / sq
        n3 = axis.z / sq

        m = MatrixAffine4x4()
        m.data = np.array(
            [[n1 * n1 + (1 - n1 * n1) * cos(angle), n1 * n2 * (1 - cos(angle)) - n3 * sin(angle),
              n1 * n3 * (1 - cos(angle)) + n2 * sin(angle), 0.0],
             [n1 * n2 * (1 - cos(angle)) + n3 * sin(angle), n2 * n2 + (1 - n2 * n2) * cos(angle),
              n2 * n3 * (1 - cos(angle)) - n1 * sin(angle), 0.0],
             [n1 * n3 * (1 - cos(angle)) - n2 * sin(angle), n2 * n3 * (1 - cos(angle)) + n1 * sin(angle),
              n3 * n3 + (1 - n3 * n3) * cos(angle), 0.0],
             [0.0, 0.0, 0.0, 1.0]])

        return m

    @staticmethod
    def build_scale(sx, sy, sz):
        m = MatrixAffine4x4()
        m.data = np.array([[sx, 0.0, 0.0, 0.0],
                           [0.0, sy, 0.0, 0.0],
                           [0.0, 0.0, sz, 0.0],
                           [0.0, 0.0, 1.0, 0.0]])
        return m

    @staticmethod
    def build_translation(point):
        m = MatrixAffine4x4()
        m.data = np.array([[1.0, 0.0, 0.0, 0.0],
                           [0.0, 1.0, 0.0, 0.0],
                           [0.0, 0.0, 1.0, 0.0],
                           [point.x, point.y, point.z, 1.0]])
        return m


class BoundingBox(Transformable):
    """
    Represents bounding box.
    """

    def __init__(self, point_min, point_max):
        self.point_min = point_min
        self.point_max = point_max

    def is_point_in(self, point):
        return (self.point_min.x <= point.x) and \
               (self.point_max.x >= point.x) and \
               (self.point_min.y <= point.y) and \
               (self.point_max.y >= point.y) and \
               (self.point_min.z <= point.z) and \
               (self.point_max.z >= point.z)

    def get_model(self):
        model = Model()
        vid_1 = model.add_vertex(Vertex3d(Vector3(self.point_min.x, self.point_min.y, self.point_min.z)))
        vid_2 = model.add_vertex(Vertex3d(Vector3(self.point_min.x, self.point_min.y, self.point_max.z)))
        vid_3 = model.add_vertex(Vertex3d(Vector3(self.point_min.x, self.point_max.y, self.point_min.z)))
        vid_4 = model.add_vertex(Vertex3d(Vector3(self.point_min.x, self.point_max.y, self.point_max.z)))
        vid_5 = model.add_vertex(Vertex3d(Vector3(self.point_max.x, self.point_min.y, self.point_min.z)))
        vid_6 = model.add_vertex(Vertex3d(Vector3(self.point_max.x, self.point_min.y, self.point_max.z)))
        vid_7 = model.add_vertex(Vertex3d(Vector3(self.point_max.x, self.point_max.y, self.point_min.z)))
        vid_8 = model.add_vertex(Vertex3d(Vector3(self.point_max.x, self.point_max.y, self.point_max.z)))

        model.add_edge(Edge(vid_1, vid_2))
        model.add_edge(Edge(vid_2, vid_4))
        model.add_edge(Edge(vid_3, vid_4))
        model.add_edge(Edge(vid_3, vid_1))
        model.add_edge(Edge(vid_5, vid_6))
        model.add_edge(Edge(vid_6, vid_8))
        model.add_edge(Edge(vid_7, vid_8))
        model.add_edge(Edge(vid_7, vid_5))
        model.add_edge(Edge(vid_1, vid_5))
        model.add_edge(Edge(vid_2, vid_6))
        model.add_edge(Edge(vid_3, vid_7))
        model.add_edge(Edge(vid_4, vid_8))

        return model

    def transform(self, matrix):
        self.point_min.transform(matrix)
        self.point_max.transform(matrix)

    def get_transformed(self, matrix):
        point_min = self.point_min.get_transformed(matrix)
        point_max = self.point_max.get_transformed(matrix)
        return BoundingBox(point_min, point_max)


class Vertex3d(Transformable):
    """
    Represents a single 3d vertex.
    """

    def __init__(self, point, color=(0, 0, 0)):
        self.point = point
        self.color = color

    def transform(self, matrix):
        self.point.transform(matrix)

    def get_transformed(self, matrix):
        point = self.point.get_transformed(matrix)
        return Vertex3d(point, self.color)


class Edge(object):
    """
    Represents an edge between two vertices.
    """

    def __init__(self, vid_from, vid_to):
        self.vid_from = vid_from
        self.vid_to = vid_to


class Facet(object):
    """
    Represents a facet based on three vertices.
    """

    def __init__(self, vid_1, vid_2, vid_3, color=(0, 0, 0)):
        self.vid_1 = vid_1
        self.vid_2 = vid_2
        self.vid_3 = vid_3
        self.color = color


class Model(Transformable):
    """
    Represents 3d geometry objects.
    """

    def __init__(self):
        self._vertices = []
        self._edges = []
        self._facets = []

    def transform(self, matrix):
        for vertex in self._vertices:
            vertex.transform(matrix)

    def add_vertex(self, vertex):
        self._vertices.append(vertex)
        return len(self._vertices) - 1

    def add_edge(self, edge):
        self._edges.append(edge)
        return len(self._edges) - 1

    def add_facet(self, facet):
        self._facets.append(facet)
        return len(self._facets) - 1

    def get_vertices(self):
        return self._vertices

    def get_edges(self):
        return self._edges

    def get_facets(self):
        return self._facets

    def clear(self):
        self._vertices.clear()
        self._edges.clear()
        self._facets.clear()
