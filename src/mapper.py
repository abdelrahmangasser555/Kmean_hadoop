#!/usr/bin/env python3
import sys
from kmeans_utils import load_centroids, closest_centroid

centroids = load_centroids()

for line in sys.stdin:

    line = line.strip()

    if not line:
        continue

    parts = line.split(",")

    # dataset has exactly 2 columns
    if len(parts) != 2:
        continue

    try:
        x = float(parts[0])
        y = float(parts[1])
    except:
        continue

    cluster = closest_centroid(x, y, centroids)

    print(f"{cluster}\t{x},{y}")