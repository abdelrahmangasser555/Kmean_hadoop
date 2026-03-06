import subprocess
import shutil
import os
import pandas as pd
import numpy as np
from sklearn.datasets import load_iris
from sklearn.metrics import adjusted_rand_score

HADOOP_STREAMING = "/usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar"

INPUT = "/projects/kmeans/input/iris.csv"
OUTPUT = "/projects/kmeans/output"

RESULT_DIR = "results"

iris = load_iris()
true_labels = iris.target
points = iris.data[:, [0,2]]


def run_cmd(cmd):
    print("Running:", cmd)
    subprocess.run(cmd, shell=True, check=True)


def convert_centroids():

    with open("data/new_centroids.txt") as f, open("data/centroids.txt","w") as out:

        for line in f:
            line = line.strip()

            if not line:
                continue

            cid,x,y = line.split(",")

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

    run_cmd("hdfs dfs -rm -r /projects/kmeans/output || true")

    run_cmd(cmd)

    run_cmd("hdfs dfs -cat /projects/kmeans/output/part-00000 > data/new_centroids.txt")

    convert_centroids()


def run_kmeans(k):

    print(f"\nRunning K={k}")

    indices = np.random.choice(len(points), k, replace=False)

    with open("data/centroids.txt","w") as f:
        for i, idx in enumerate(indices):
            x, y = points[idx]
            f.write(f"{i},{x},{y}\n")

    for i in range(5):
        print("Iteration", i+1)
        run_iteration()

    shutil.copy("data/centroids.txt", f"{RESULT_DIR}/k{k}_centroids.txt")


def load_centroids(file):

    centroids = []

    with open(file) as f:
        for line in f:
            line=line.strip()

            if not line:
                continue

            cid,x,y=line.split(",")

            centroids.append([float(x),float(y)])

    return np.array(centroids)


def assign_clusters(centroids):

    preds=[]

    for p in points:

        d=np.linalg.norm(centroids-p,axis=1)

        preds.append(np.argmin(d))

    return preds


def compute_ari():

    rows=[]

    for k in range(1,6):

        centroids=load_centroids(f"{RESULT_DIR}/k{k}_centroids.txt")

        preds=assign_clusters(centroids)

        ari=adjusted_rand_score(true_labels,preds)

        rows.append([k,ari])

    df=pd.DataFrame(rows,columns=["K","ARI"])

    df.to_csv(f"{RESULT_DIR}/ari_scores.csv",index=False)

    best=df.loc[df["ARI"].idxmax()]

    with open(f"{RESULT_DIR}/best_k.txt","w") as f:
        f.write(f"Best K = {int(best['K'])}\nARI = {best['ARI']}\n")

    print("\nARI RESULTS")
    print(df)
    print("\nBest K =",int(best["K"]))


def main():

    os.makedirs(RESULT_DIR,exist_ok=True)

    for k in range(1,6):
        run_kmeans(k)

    compute_ari()


if __name__=="__main__":
    main()