#!/usr/bin/env python3
import sys

current_cluster = None
sum_x = 0.0
sum_y = 0.0
count = 0


def emit(cluster, sx, sy, c):
    if c == 0:
        return

    cx = sx / c
    cy = sy / c

    print(f"{cluster},{cx},{cy}")


for line in sys.stdin:

    line = line.strip()

    if not line:
        continue

    cluster, point = line.split("\t")
    x, y = map(float, point.split(","))

    if current_cluster is None:
        current_cluster = cluster

    if cluster != current_cluster:

        emit(current_cluster, sum_x, sum_y, count)

        current_cluster = cluster
        sum_x = 0
        sum_y = 0
        count = 0

    sum_x += x
    sum_y += y
    count += 1

emit(current_cluster, sum_x, sum_y, count)