#!/bin/bash

echo "🚀 Starting Hadoop services..."

start-dfs.sh
start-yarn.sh

echo "⏳ Waiting for Hadoop to initialize..."
sleep 5

echo "🧹 Cleaning old results..."

rm -rf results
rm -f data/centroids.txt
rm -f data/new_centroids.txt

mkdir -p results

echo "🗑 Removing old HDFS directories..."

hdfs dfs -rm -r -f /projects/kmeans/input
hdfs dfs -rm -r -f /projects/kmeans/output

echo "📤 Uploading dataset to HDFS..."

hdfs dfs -mkdir -p /projects/kmeans/input
hdfs dfs -put -f data/iris.csv /projects/kmeans/input/

echo "📊 Verifying dataset..."

hdfs dfs -ls /projects/kmeans/input

echo "🏃 Running K-Means pipeline..."

python src/driver.py

echo "✅ Finished!"

echo "📂 Results:"
ls results