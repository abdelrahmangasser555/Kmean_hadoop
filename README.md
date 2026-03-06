# 🚀 Hadoop K-Means Clustering (MapReduce)

This project implements the **K-Means clustering algorithm using Hadoop MapReduce** with Python streaming scripts.
It demonstrates how a machine learning algorithm can be executed in a **distributed computing environment**.

The system clusters data points using **iterative MapReduce jobs** and uses **K-Means++ initialization** to improve centroid selection.

---

# 📊 Project Overview

K-Means is an unsupervised machine learning algorithm used to group similar data points into clusters.

In this project:

- 📥 Data is stored in **HDFS**
- 🧠 The **Mapper** assigns points to the nearest centroid
- 🔄 The **Reducer** recomputes new centroids
- 🔁 The process repeats for multiple iterations
- 🎯 The algorithm is tested with **K = 1..5**

The goal is to identify the **best number of clusters** for the dataset.

---

# 🏗️ Architecture

The clustering pipeline follows the standard MapReduce workflow.

```
Dataset (HDFS)
      │
      ▼
   Mapper
(assign nearest centroid)
      │
      ▼
 Shuffle & Sort
      │
      ▼
   Reducer
(recompute centroid)
      │
      ▼
 Updated Centroids
      │
      ▼
 Next Iteration
```

Each iteration updates cluster centers until convergence.

---

# ⚙️ Technologies Used

- 🐍 **Python**
- 🐘 **Hadoop MapReduce**
- 📂 **HDFS**
- 🐳 **Docker**
- 📊 **NumPy**

---

# 📁 Project Structure

```
kmean/
│
├── src/
│   ├── mapper.py
│   ├── reducer.py
│   ├── driver.py
│   └── kmeans_utils.py
│
├── data/
│   └── iris.csv
│
├── results/
│   ├── k1_centroids.txt
│   ├── k2_centroids.txt
│   ├── k3_centroids.txt
│   ├── k4_centroids.txt
│   ├── k5_centroids.txt
│   └── scores.txt
│
├── docker/
│   └── Dockerfile
│
└── README.md
```

---

# 📥 Dataset

The project uses a simplified **Iris dataset** containing two features per sample:

```
sepal_length, petal_length
```

Example:

```
5.1,1.4
4.9,1.4
4.7,1.3
```

---

# 🧠 K-Means Algorithm

The clustering process follows these steps:

1️⃣ Initialize centroids using **K-Means++**
2️⃣ Assign each data point to the nearest centroid
3️⃣ Compute new centroids by averaging cluster points
4️⃣ Repeat for several iterations
5️⃣ Evaluate results for different values of **K**

---

# ✨ K-Means++ Initialization

Instead of random initialization, **K-Means++** is used.

This improves clustering by choosing centroids that are **far apart**, which leads to:

- faster convergence
- better cluster quality
- more stable results

---

# ▶️ Running the Project

### 1️⃣ Upload dataset to HDFS

```bash
hdfs dfs -mkdir -p /projects/kmeans/input
hdfs dfs -put data/iris.csv /projects/kmeans/input/
```

---

### 2️⃣ Run clustering

```
python src/driver.py
```

This will run clustering for:

```
K = 1,2,3,4,5
```

---

### 3️⃣ View results

```
ls results
```

Example output:

```
k1_centroids.txt
k2_centroids.txt
k3_centroids.txt
k4_centroids.txt
k5_centroids.txt
scores.txt
```

---

# 📈 Example Results

```
K=1 SCORE=120.3
K=2 SCORE=80.2
K=3 SCORE=45.1
K=4 SCORE=43.9
K=5 SCORE=43.0

BEST_K=3
```

This matches the **true number of clusters in the Iris dataset**.

---

# 🐳 Running with Docker

Build the container:

```
docker build -t hadoop-kmeans .
```

Run the container:

```
docker run -it hadoop-kmeans
```

The container will automatically run the clustering pipeline.

---

# 🎯 Learning Outcomes

This project demonstrates:

- implementing ML algorithms with **MapReduce**
- working with **distributed datasets in HDFS**
- using **Hadoop streaming with Python**
- applying **K-Means++ for better clustering**
- containerizing data pipelines with **Docker**

---

# 📚 References

- Hadoop MapReduce Documentation
- K-Means Clustering Algorithm
- K-Means++ Initialization Paper

---

# 👨‍💻 Author

Developed as part of a **distributed data processing assignment** exploring scalable machine learning algorithms with Hadoop.
