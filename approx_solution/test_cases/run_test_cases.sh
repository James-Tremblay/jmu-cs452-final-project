SOLVER="./approx.py"
TESTDIR="./test_cases"

echo "Running all test cases..."

for f in $TESTDIR/*.txt; do
    echo "======================================="
    echo "Running: $f"
    echo "---------------------------------------"
    START=$(date +%s%N)
    
    $SOLVER < "$f" > "${f%.txt}_output.txt"
    
    END=$(date +%s%N)
    RUNTIME=$(( (END - START)/1000000 ))
    
    echo "Completed in ${RUNTIME} ms"
done

echo "======================================="
echo "Done running all test cases."