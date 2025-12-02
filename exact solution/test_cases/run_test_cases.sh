#!/bin/bash
for f in test_case*.txt
do
    python3 ../exact.py "$f" -p 4 >> results.txt
    echo "" >> results.txt
done
