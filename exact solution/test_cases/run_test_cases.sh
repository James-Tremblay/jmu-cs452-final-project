#!/bin/bash
for f in test_case*.txt
do
    python3 ../exact.py "$f" >> results.txt
    echo "" >> results.txt
done
