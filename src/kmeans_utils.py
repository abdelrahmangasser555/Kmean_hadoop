import numpy as np


def load_centroids():

    centroids = []

    with open("centroids.txt") as f:
        for line in f:

            line = line.strip()

            if not line:
                continue

            cid, x, y = line.split(",")

            centroids.append([float(x), float(y)])

    return np.array(centroids)


def closest_centroid(x, y, centroids):

    point = np.array([x, y])

    distances = np.linalg.norm(centroids - point, axis=1)

    return int(np.argmin(distances))