#!/bin/bash

APPROX="../approx.py"
EXACT="../exact.py"
TESTDIR="."
TVAL=5  # your -t flag

echo "Running all test cases..."
shopt -s nullglob   # avoids literal *.txt error

FILES=($TESTDIR/test_case*.txt)

if [ ${#FILES[@]} -eq 0 ]; then
    echo "ERROR: No test_case*.txt files found in $TESTDIR"
    exit 1
fi

# Clear previous results2
echo "" > results2.txt

for f in "${FILES[@]}"; do
    if [[ "$(basename "$f")" == "results2.txt" ]] || [[ "$(basename "$f")" == "results.txt" ]]; then
        continue
    fi
    
    echo "======================================="  >> results2.txt
    echo "Running: $f" >> results2.txt
    echo "---------------------------------------" >> results2.txt

    START=$(date +%s%N)

    echo "Approximate Solution:" >> results2.txt
    python "$APPROX" "$f" | head -n 1 >> results2.txt
    echo "" >> results2.txt

    END=$(date +%s%N)
    RUNTIME=$(( (END - START)/1000000 ))

    echo "Completed in ${RUNTIME} ms" >> results2.txt


    START=$(date +%s%N)
    
    echo "Exact Solution:" >> results2.txt
    python "$EXACT" "$f" | head -n 1 >> results2.txt
    echo "" >> results2.txt

    END=$(date +%s%N)
    RUNTIME=$(( (END - START)/1000000 ))

    echo "Completed in ${RUNTIME} ms" >> results2.txt
done

echo "======================================="
echo "Done running all test cases."
