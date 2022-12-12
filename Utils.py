import math
import numpy as np


def Euclidean_dist(p1, p2):
    # Computes Euclidean distance between two 2D points
    x1, y1 = p1
    x2, y2 = p2
    x_d, y_d = x1 - x2, y1 - y2

    return math.sqrt(x_d**2 + y_d**2)


def BoundingBox(lmList):
    if len(lmList) == 0:
        return 0, None
    lmList_ = np.array(lmList)
    x_min, x_max = np.min(lmList_[:, 1]), np.max(lmList_[:, 1])
    y_min, y_max = np.min(lmList_[:, 2]), np.max(lmList_[:, 2])
    # resize bounding box
    x_min, x_max = int(x_min) - 20, int(x_max) + 20
    y_min, y_max = int(y_min) - 20, int(y_max) + 20

    width, height = x_max - x_min, y_max - y_min
    area = width * height // 100
    return area, [(x_min, y_min), (x_max, y_max)]
