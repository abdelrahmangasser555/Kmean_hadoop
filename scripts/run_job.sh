#!/bin/bash

STREAMING_JAR=/usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar

INPUT=/projects/kmeans/input/dataset.csv
OUTPUT=/projects/kmeans/output

echo "Uploading dataset..."

hdfs dfs -put -f ../data/dataset.csv /projects/kmeans/input/

echo "Removing old output..."

hdfs dfs -rm -r $OUTPUT 2>/dev/null

echo "Running Hadoop job..."

hadoop jar $STREAMING_JAR \
-input $INPUT \
-output $OUTPUT \
-mapper ../src/mapper.py \
-reducer ../src/reducer.py \
-file ../src/mapper.py \
-file ../src/reducer.py

echo ""
echo "Job finished."
echo "Results:"

hdfs dfs -cat /projects/kmeans/output/part-00000