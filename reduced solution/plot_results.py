import csv
import matplotlib

# Force a non-interactive backend so plotting works in headless environments
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def main():
    results_file = "results.csv"
    
    sizes = []
    bounds = []
    approx_scores = []
    mis_scores = []
    reduction_times = []
    mis_times = []
    
    try:
        with open(results_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                sizes.append(int(row["Clauses (m)"]))
                bounds.append(int(row["Bound"]))
                approx_scores.append(int(row["Approx MaxSAT"]))
                mis_scores.append(int(row["MIS Independent Set"]))
                reduction_times.append(float(row["Reduction Time (s)"]))
                mis_times.append(float(row["MIS Solve Time (s)"]))
    except FileNotFoundError:
        print("results.csv not found. Run driver.py first.")
        return
    
    if not sizes:
        print("results.csv is empty.")
        return
    
    data = sorted(zip(sizes, bounds, approx_scores, mis_scores, reduction_times, mis_times))
    sizes, bounds, approx_scores, mis_scores, reduction_times, mis_times = zip(*data)
    
    # Plot 1: Reduction and MIS time vs input size
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, reduction_times, 'bo-', label='Reduction Time')
    plt.plot(sizes, mis_times, 'gs-', label='MIS Solve Time')
    plt.xlabel('Input Size (Number of Clauses m)')
    plt.ylabel('Time (seconds)')
    plt.title('Runtime vs Input Size')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig('pictures/runtime_vs_size.png')
    print("Saved runtime_vs_size.png")
    
    # Plot 2: Compare bound, SAT approximation, and MIS result
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, bounds, 'k--', label='Upper Bound (m)')
    plt.plot(sizes, approx_scores, 'r.-', label='Approx Max-3-SAT')
    plt.plot(sizes, mis_scores, 'b*:', label='MIS after Reduction')
    plt.xlabel('Input Size (Number of Clauses m)')
    plt.ylabel('Satisfied Clauses / Independent Set Size')
    plt.title('Solution Quality Comparison')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig('pictures/solution_quality.png')
    print("Saved solution_quality.png")
    
    # Plot 3: Scatter to show reduction correctness
    plt.figure(figsize=(6, 6))
    plt.scatter(approx_scores, mis_scores, c=sizes, cmap='viridis', edgecolor='black')
    max_val = max(max(approx_scores), max(mis_scores), max(bounds))
    plt.plot([0, max_val], [0, max_val], 'k--', label='y = x')
    plt.xlabel('Approx Max-3-SAT score')
    plt.ylabel('MIS size after reduction')
    plt.title('Approximation vs Reduced MIS (should match)')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig('pictures/approx_vs_mis.png')
    print("Saved approx_vs_mis.png")


if __name__ == "__main__":
    main()
