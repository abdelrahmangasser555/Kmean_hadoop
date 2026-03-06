#!/bin/bash

echo "Starting Hadoop..."

start-dfs.sh

echo ""
echo "Running processes:"
jps

echo ""
echo "HDFS root:"
hdfs dfs -ls /