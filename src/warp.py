import cv2
import numpy as np

def warp(img, points):
    points = points.reshape(4, 2).astype(np.float32)

    center = points.mean(axis=0)
    angles = np.arctan2(
        points[:, 1] - center[1],
        points[:, 0] - center[0]
    )
    points = points[np.argsort(angles)]

    start  = np.argmin(points.sum(axis=1))
    points = np.roll(points, -start, axis=0)
    tl, tr, br, bl = points

    width  = max(np.linalg.norm(tr - tl), np.linalg.norm(br - bl))
    height = max(np.linalg.norm(bl - tl), np.linalg.norm(br - tr))
    width  = int(round(width))  + 1
    height = int(round(height)) + 1

    if width < 3 or height < 3: raise ValueError("Document is too small")

    target = np.array([
        [0, 0],
        [width - 1, 0],
        [width - 1, height - 1],
        [0, height - 1]
    ], dtype=np.float32)

    matrix = cv2.getPerspectiveTransform(points, target)
    return cv2.warpPerspective(img, matrix, (width, height))