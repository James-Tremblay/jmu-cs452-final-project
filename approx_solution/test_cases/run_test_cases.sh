#!/bin/bash

SOLVER="../approx.py"
TESTDIR="."
TVAL=5  # your -t flag

echo "Running all test cases..."
shopt -s nullglob   # avoids literal *.txt error

FILES=($TESTDIR/*.txt)

if [ ${#FILES[@]} -eq 0 ]; then
    echo "ERROR: No .txt test files found in $TESTDIR"
    exit 1
fi

# Clear previous results
echo "" > results.txt

for f in "${FILES[@]}"; do
    if [[ "$(basename "$f")" == "results2.txt" ]] || [[ "$(basename "$f")" == "results.txt" ]]; then
        continue
    fi
    
    echo "======================================="  >> results.txt
    echo "Running: $f" >> results.txt
    echo "---------------------------------------" >> results.txt

    START=$(date +%s%N)

    python "$SOLVER" "$f" >> results.txt
    echo "" >> results.txt

    END=$(date +%s%N)
    RUNTIME=$(( (END - START)/1000000 ))

    echo "Completed in ${RUNTIME} ms" >> results.txt
done

echo "======================================="
echo "Done running all test cases."
