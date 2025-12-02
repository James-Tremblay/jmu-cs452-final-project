import os
import sys
import time
import subprocess
import glob
import csv

def run_command(command, input_file):
    """Runs a command with input from a file and returns stdout."""
    with open(input_file, 'r') as f:
        start = time.time()
        result = subprocess.run(command, stdin=f, capture_output=True, text=True)
        end = time.time()
        return result.stdout.strip(), end - start

def get_input_size(file_path):
    with open(file_path, 'r') as f:
        line = f.readline()
        if not line: return 0
        parts = line.split()
        if len(parts) >= 2:
            return int(parts[1]) # m is the second number
    return 0

def main():
    test_cases_dir = "test_cases"
    results_file = "results.csv"
    
    # Find all test cases
    test_files = sorted(glob.glob(os.path.join(test_cases_dir, "test_case*.txt")))
    
    results = []
    
    print(f"Found {len(test_files)} test cases.")
    
    # Paths to scripts
    # Assuming we run from 'reduced solution' directory
    path_exact = "exact_max.py"
    path_reduction = "reduction.py"
    path_approx = "../approx_solution/approx.py"
    
    for test_file in test_files:
        case_name = os.path.basename(test_file)
        print(f"Processing {case_name}...")
        
        m = get_input_size(test_file)
        
        # 1. Get Optimal Value
        out_exact, _ = run_command(["python3", path_exact], test_file)
        try:
            optimal = int(out_exact.split('\n')[0]) # First line is score
        except:
            optimal = -1
            
        # 2. Get Bound
        out_bound, _ = run_command(["python3", path_reduction, "--bound"], test_file)
        try:
            bound = int(out_bound.split('\n')[0])
        except:
            bound = -1
            
        # 3. Measure Reduction Time
        # We discard output but measure time
        _, red_time = run_command(["python3", path_reduction], test_file)
        
        # 4. Get Approx Value
        # approx.py prints score on first line
        out_approx, _ = run_command(["python3", path_approx], test_file)
        try:
            lines = out_approx.split('\n')
            approx = int(lines[0])
        except:
            approx = -1
            
        results.append({
            "Test Case": case_name,
            "Input Size (m)": m,
            "Optimal": optimal,
            "Bound": bound,
            "Approx": approx,
            "Reduction Time": red_time
        })
        
    # Write to CSV
    with open(results_file, 'w', newline='') as csvfile:
        fieldnames = ["Test Case", "Input Size (m)", "Optimal", "Bound", "Approx", "Reduction Time"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow(row)
            
    print(f"Results saved to {results_file}")

if __name__ == "__main__":
    main()

