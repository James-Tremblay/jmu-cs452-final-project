#!/usr/bin/env python3
import os, time, subprocess, csv

TEST_DIR = "test_cases"
SOLVER = "solver.py"
OUT_CSV = "benchmark_results.csv"

def main():
    test_files = sorted(f for f in os.listdir(TEST_DIR) if f.startswith("test_case"))
    rows = []

    for tf in test_files:
        path = os.path.join(TEST_DIR, tf)
        print(f"Running {tf}...")

        start = time.time()
        result = subprocess.run(
            ["python3", SOLVER, path, "-p", "4"],
            capture_output=True,
            text=True
        )
        end = time.time()
        runtime = end - start

        # parse input size
        with open(path) as f:
            first = f.readline().strip().split()
            n = int(first[0])
            m = int(first[1])

        # parse output (first line = clauses satisfied)
        output_lines = result.stdout.strip().splitlines()
        satisfied = output_lines[0] if output_lines else "ERR"

        rows.append([tf, n, m, runtime, satisfied])

    # write CSV
    with open(OUT_CSV, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["file", "n", "m", "runtime_seconds", "clauses_satisfied"])
        w.writerows(rows)

    print(f"\nBenchmark complete. Results saved to {OUT_CSV}")

if __name__ == "__main__":
    main()
