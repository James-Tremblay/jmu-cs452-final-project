import argparse
import ast
import csv
import glob
import os
import subprocess
import sys
import time

APPROX_TIME_LIMIT = 1  # seconds per Max-3-SAT approximation run
MIS_TIME_LIMIT = 1     # seconds per MIS heuristic run


def run_process(command, *, input_data=None):
    """
    Execute command, optionally providing stdin input_data. Returns tuple of
    (stdout, stderr, returncode, elapsed_seconds).
    """
    start = time.time()
    result = subprocess.run(
        command,
        input=input_data,
        capture_output=True,
        text=True,
    )
    elapsed = time.time() - start
    if result.returncode != 0:
        sys.stderr.write(
            f"[driver] Command {' '.join(command)} failed ({result.returncode}):\n"
            f"{result.stderr}\n"
        )
    return result.stdout.strip(), result.stderr.strip(), result.returncode, elapsed


def parse_input_size(test_data):
    """
    Return m (number of clauses) from the test case contents.
    """
    first_line = test_data.strip().splitlines()
    if not first_line:
        return 0
    tokens = first_line[0].split()
    if len(tokens) < 2:
        return 0
    return int(tokens[1])


def parse_mis_size(raw_output):
    """
    max_ind_set.py prints the final independent set on the last line.
    Convert that textual Python-set representation into its numeric size.
    """
    if not raw_output:
        return -1
    last_line = raw_output.strip().splitlines()[-1].strip()
    if last_line == "set()":
        return 0
    try:
        parsed = ast.literal_eval(last_line)
        if isinstance(parsed, (set, list, tuple)):
            return len(parsed)
    except Exception:
        pass
    if last_line.startswith("{") and last_line.endswith("}"):
        inner = last_line[1:-1].strip()
        if not inner:
            return 0
        return len([item for item in inner.split(",") if item.strip()])
    return -1

def main():
    parser = argparse.ArgumentParser(description="Run Max 3-SAT reduction and approximation tests")
    parser.add_argument(
        "-n", "--num-tests",
        type=int,
        default=None,
        help="Number of test cases to run (default: run all tests)"
    )
    args = parser.parse_args()
    
    test_cases_dir = "test_cases"
    results_file = "results.csv"
    approx_time = APPROX_TIME_LIMIT
    
    # Find all test cases
    test_files = sorted(
        glob.glob(os.path.join(test_cases_dir, "test_case*.txt")),
        key=lambda path: int(''.join(filter(str.isdigit, os.path.basename(path)))),
    )
    
    # Limit to specified number of tests if provided
    if args.num_tests is not None:
        test_files = test_files[:args.num_tests]
    
    results = []
    
    total_tests = len(glob.glob(os.path.join(test_cases_dir, "test_case*.txt")))
    print(f"Found {total_tests} total test cases. Running {len(test_files)} test case(s).")
    
    # Paths to scripts
    # Assuming we run from 'reduced solution' directory
    path_reduction = "reduction.py"
    path_max_ind_set = "max_ind_set.py"
    path_approx = os.path.join("..", "approx_solution", "approx.py")
    
    for test_file in test_files:
        case_name = os.path.basename(test_file)
        print(f"Processing {case_name}...")
        with open(test_file, "r") as f:
            test_data = f.read()
        
        m = parse_input_size(test_data)
        
        # 1. Compute bound (trivial m)
        bound_stdout, _, _, _ = run_process(
            ["python3", path_reduction, "--bound"],
            input_data=test_data,
        )
        try:
            bound = int(bound_stdout.splitlines()[0])
        except Exception:
            bound = m if m else -1
        
        # 2. Run reduction to build MIS instance
        reduction_stdout, _, _, red_time = run_process(
            ["python3", path_reduction],
            input_data=test_data,
        )
        
        # 3. Run Max Independent Set heuristic on reduced graph
        mis_stdout, _, _, mis_time = run_process(
            ["python3", path_max_ind_set, "--t", str(MIS_TIME_LIMIT)],
            input_data=reduction_stdout + ("\n" if not reduction_stdout.endswith("\n") else ""),
        )
        mis_size = parse_mis_size(mis_stdout)
        
        # 4. Get approximation result directly on Max-3-SAT
        approx_stdout, _, _, _ = run_process(
            ["python3", path_approx, "-t", str(approx_time), test_file],
        )
        try:
            approx_score = int(approx_stdout.splitlines()[0])
        except Exception:
            approx_score = -1
            
        results.append({
            "Test Case": case_name,
            "Clauses (m)": m,
            "Bound": bound,
            "Approx MaxSAT": approx_score,
            "MIS Independent Set": mis_size,
            "Reduction Time (s)": red_time,
            "MIS Solve Time (s)": mis_time,
        })
        
    # Write to CSV
    with open(results_file, 'w', newline='') as csvfile:
        fieldnames = [
            "Test Case",
            "Clauses (m)",
            "Bound",
            "Approx MaxSAT",
            "MIS Independent Set",
            "Reduction Time (s)",
            "MIS Solve Time (s)",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow(row)
            
    print(f"Results saved to {results_file}")

if __name__ == "__main__":
    main()

