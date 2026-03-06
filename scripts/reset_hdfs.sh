#!/bin/bash

echo "Resetting project directories..."

hdfs dfs -rm -r /projects/kmeans/output 2>/dev/null

hdfs dfs -mkdir -p /projects/kmeans/input
hdfs dfs -mkdir -p /projects/kmeans/output

echo "Done."