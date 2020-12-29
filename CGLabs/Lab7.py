"""
Prog:   Lab7.py

Auth:   Oleksii Krutko, IO-z91

Desc:   Computer graphics Lab 7. 2020

"""

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
import math

rot_angle = 0.0


def drawBox(x1, x2, y1, y2, z1, z2):
    """
    Draws a box with diagonal  (x1, y1, z1) - (x2, y2, z2)
    :param x1:
    :param x2:
    :param y1:
    :param y2:
    :param z1:
    :param z2:
    :return:
    """
    glBegin(GL_POLYGON)
    glNormal3f(0.0, 0.0, 1.0)
    glVertex3f(x1, y1, z2)
    glVertex3f(x2, y1, z2)
    glVertex3f(x2, y2, z2)
    glVertex3f(x1, y2, z2)
    glEnd()

    glBegin(GL_POLYGON)
    glNormal3f(0.0, 0.0, -1.0)
    glVertex3f(x2, y1, z1)
    glVertex3f(x1, y1, z1)
    glVertex3f(x1, y2, z1)
    glVertex3f(x2, y2, z1)
    glEnd()

    glBegin(GL_POLYGON)
    glNormal3f(-1.0, 0.0, 0.0)
    glVertex3f(x1, y1, z1)
    glVertex3f(x1, y1, z2)
    glVertex3f(x1, y2, z2)
    glVertex3f(x1, y2, z1)
    glEnd()

    glBegin(GL_POLYGON)
    glNormal3f(1.0, 0.0, 0.0)
    glVertex3f(x2, y1, z2)
    glVertex3f(x2, y1, z1)
    glVertex3f(x2, y2, z1)
    glVertex3f(x2, y2, z2)
    glEnd()

    glBegin(GL_POLYGON)
    glNormal3f(0.0, 1.0, 0.0)
    glVertex3f(x1, y2, z2)
    glVertex3f(x2, y2, z2)
    glVertex3f(x2, y2, z1)
    glVertex3f(x1, y2, z1)
    glEnd()

    glBegin(GL_POLYGON)
    glNormal3f(0.0, -1.0, 0.0)
    glVertex3f(x2, y1, z2)
    glVertex3f(x1, y1, z2)
    glVertex3f(x1, y1, z1)
    glVertex3f(x2, y1, z1)
    glEnd()


def draw_cylinder(radius, height, num_slices):
    """
    Draws cylinder
    :param radius:
    :param height:
    :param num_slices:
    :return:
    """
    r = radius
    h = height
    n = float(num_slices)

    circle_pts = []
    for i in range(int(n) + 1):
        angle = 2 * math.pi * (i / n)
        x = r * math.cos(angle)
        y = r * math.sin(angle)
        pt = (x, y)
        circle_pts.append(pt)

    glBegin(GL_TRIANGLE_FAN)
    glNormal3f(0.0, 0.0, 1.0)
    glColor(1, 0, 0)
    glVertex(0, 0, h / 2.0)
    for (x, y) in circle_pts:
        z = h / 2.0
        glNormal3f(0.0, 0.0, 1.0)
        glVertex(x, y, z)
    glEnd()

    glBegin(GL_TRIANGLE_FAN)
    glNormal3f(0.0, 0.0, -1.0)
    glColor(0, 0, 1)
    glVertex(0, 0, h / 2.0)
    for (x, y) in circle_pts:
        z = -h / 2.0
        glNormal3f(0.0, 0.0, -1.0)
        glVertex(x, y, z)
    glEnd()

    glBegin(GL_TRIANGLE_STRIP)
    glColor(0, 1, 0)
    for (x, y) in circle_pts:
        z = h / 2.0
        glNormal3f(x, y, 0.0)
        glVertex(x, y, z)
        glVertex(x, y, -z)
    glEnd()


def init():
    """
    Initializes glut
    :return:
    """
    glClearColor(0.6, 0.6, 0.6, 0.0)
    glClearDepth(1.0)
    glDepthFunc(GL_LEQUAL)
    glEnable(GL_DEPTH_TEST)
    glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    light_pos = [0.5, 1.0, 1.0, 0.0]
    glLightfv(GL_LIGHT0, GL_POSITION, light_pos)

    cyan = [0.0, 0.8, 0.8, 1.0]
    glMaterialfv(GL_FRONT, GL_DIFFUSE, cyan)


def reshape(width, height):
    """
    Re-sets up when window size is changed
    :param width:
    :param height:
    :return:
    """
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(60.0, float(width) / float(height), 1.0, 60.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def display():
    """
    Renders scene
    :return:
    """
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(6, 5, 5, 0, 0, 0, 0, 0, 1)

    glRotatef(rot_angle, 1, -1, 0)

    drawBox(-1, 1, -3, -1, -1, 1)
    draw_cylinder(1, 2, 20)

    glutSwapBuffers()


def keyPressed(*args):
    """
    Finish when ESC is pressed
    :param args:
    :return:
    """
    if args[0] == '\033':
        sys.exit()


def animate():
    """
    Changes the global rot_angle to be used in display method
    :return:
    """
    global rot_angle

    rot_angle = 0.04 * glutGet(GLUT_ELAPSED_TIME)

    glutPostRedisplay()


def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(640, 480)
    glutInitWindowPosition(0, 0)

    glutCreateWindow("Lab 7. Variant 10.")
    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyPressed)
    init()

    glutMainLoop()


main()
