import subprocess
import shutil
import os
import numpy as np

HADOOP_STREAMING = "/usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar"

INPUT = "/projects/kmeans/input/iris.csv"
OUTPUT = "/projects/kmeans/output"

RESULT_DIR = "results"

# load local dataset
points = []
with open("data/iris.csv") as f:
    for line in f:
        x, y = map(float, line.strip().split(","))
        points.append([x, y])

points = np.array(points)


def run_cmd(cmd):
    print("Running:", cmd)
    subprocess.run(cmd, shell=True, check=True)


# -----------------------------
# KMEANS++ INITIALIZATION
# -----------------------------
def kmeans_plus_plus(points, k):

    centroids = []

    centroids.append(points[np.random.randint(len(points))])

    for _ in range(1, k):

        distances = []

        for p in points:
            d = min(np.linalg.norm(p - c) for c in centroids)
            distances.append(d ** 2)

        probs = np.array(distances) / sum(distances)

        idx = np.random.choice(len(points), p=probs)

        centroids.append(points[idx])

    return np.array(centroids)


def convert_centroids():

    with open("data/new_centroids.txt") as f, open("data/centroids.txt", "w") as out:

        for line in f:
            line = line.strip()

            if not line:
                continue

            cid, x, y = line.split(",")

            out.write(f"{cid},{x},{y}\n")


def run_iteration():

    cmd = f"""
    hadoop jar {HADOOP_STREAMING} \
    -input {INPUT} \
    -output {OUTPUT} \
    -mapper src/mapper.py \
    -reducer src/reducer.py \
    -file src/mapper.py \
    -file src/reducer.py \
    -file src/kmeans_utils.py \
    -file data/centroids.txt
    """

    run_cmd("hdfs dfs -rm -r -f /projects/kmeans/output")

    run_cmd(cmd)

    run_cmd(
        "hdfs dfs -cat /projects/kmeans/output/part-00000 > data/new_centroids.txt"
    )

    convert_centroids()


def run_kmeans(k):

    print(f"\n===== Running K={k} =====")

    centroids = kmeans_plus_plus(points, k)

    with open("data/centroids.txt", "w") as f:
        for i, (x, y) in enumerate(centroids):
            f.write(f"{i},{x},{y}\n")

    for i in range(5):
        print("Iteration", i + 1)
        run_iteration()

    shutil.copy("data/centroids.txt", f"{RESULT_DIR}/k{k}_centroids.txt")


def simple_score(centroids):

    score = 0

    for p in points:
        d = np.linalg.norm(centroids - p, axis=1)
        score += np.min(d)

    return score


def evaluate():

    results = []

    for k in range(1, 6):

        centroids = []

        with open(f"{RESULT_DIR}/k{k}_centroids.txt") as f:
            for line in f:
                _, x, y = line.strip().split(",")
                centroids.append([float(x), float(y)])

        centroids = np.array(centroids)

        score = simple_score(centroids)

        results.append((k, score))

    with open(f"{RESULT_DIR}/scores.txt", "w") as f:

        for k, s in results:
            f.write(f"K={k} SCORE={s}\n")

        best = min(results, key=lambda x: x[1])

        f.write(f"\nBEST_K={best[0]}\n")

    print("\nResults:")
    for r in results:
        print(r)

    print("\nBest K =", best[0])


def main():

    os.makedirs(RESULT_DIR, exist_ok=True)

    for k in range(1, 6):
        run_kmeans(k)

    evaluate()


if __name__ == "__main__":
    main()