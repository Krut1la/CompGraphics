import numpy as np


def get_bezier_coefficients(points):
    """
    Find the a & b points
    :param points:
    :return:
    """
    n = len(points) - 1

    # build coefficients matrix
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


def get_cubic(a, b, c, d):
    """
    Gets the general Bezier cubic formula given 4 control points
    :param a:
    :param b:
    :param c:
    :param d:
    :return:
    """
    return lambda t: np.power(1 - t, 3) * a + 3 * np.power(1 - t, 2) \
                     * t * b + 3 * (1 - t) * np.power(t, 2) * c + np.power(t, 3) * d


def get_bezier_cubic(points):
    """
    Gets one cubic curve for each consecutive points
    :param points:
    :return:
    """
    A, B = get_bezier_coefficients(points)
    return [get_cubic(points[i], A[i], B[i], points[i + 1]) for i in range(len(points) - 1)]


def evaluate_bezier(points, n):
    """
    Evaluates each cubic curve on the range [0, 1] sliced in n points
    :param points:
    :param n:
    :return:
    """
    curves = get_bezier_cubic(points)
    return np.array([func(t) for func in curves for t in np.linspace(0, 1, n)])
