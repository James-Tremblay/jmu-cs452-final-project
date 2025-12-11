import csv
import matplotlib

# Force a non-interactive backend so plotting works in headless environments
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def to_float(value, default=0.0):
    try:
        return float(value)
    except Exception:
        return default


def main():
    results_file = "results.csv"
    
    sizes = []
    bounds = []
    approx_scores = []
    mis_scores = []
    reduction_times = []
    exact_scores = []
    exact_sizes = []
    exact_bounds = []
    
    try:
        with open(results_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                size = int(row["Clauses (m)"])
                bound = int(row["Bound"])
                approx_score = int(row["Approx MaxSAT"])
                mis_score = int(row["MIS Independent Set"])
                
                reduction_times.append(to_float(row.get("Reduction Time (s)")))
                
                sizes.append(size)
                bounds.append(bound)
                approx_scores.append(approx_score)
                mis_scores.append(mis_score)
                
                exact_val = row.get("Exact Optimal")
                if exact_val not in (None, ""):
                    try:
                        exact_score = int(exact_val)
                        exact_scores.append(exact_score)
                        exact_sizes.append(size)
                        exact_bounds.append(bound)
                    except Exception:
                        pass
    except FileNotFoundError:
        print("results.csv not found. Run driver.py first.")
        return
    
    if not sizes:
        print("results.csv is empty.")
        return
    
    runtime_data = sorted(zip(sizes, reduction_times))
    sizes_runtime, reduction_times = zip(*runtime_data)
    
    bound_vs_exact = sorted(zip(exact_sizes, exact_bounds, exact_scores))
    approx_data = sorted(zip(sizes, bounds, approx_scores))
    
    # Plot 1: Reduction runtime vs input size
    plt.figure(figsize=(10, 6))
    plt.plot(sizes_runtime, reduction_times, 'bo-', label='Reduction Time')
    plt.xlabel('Input Size (Number of Clauses m)')
    plt.ylabel('Time (seconds)')
    plt.title('Reduction Runtime vs Input Size')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig('pictures/runtime_vs_size.png')
    print("Saved runtime_vs_size.png")
    
    # Plot 2: Approximation and (when available) Optimal vs bound on one plot
    sizes_sorted, bounds_sorted, approx_sorted = zip(*approx_data)
    plt.figure(figsize=(10, 6))
    plt.plot(sizes_sorted, bounds_sorted, 'k--', label='Upper Bound (m)')
    plt.plot(sizes_sorted, approx_sorted, 'r.-', label='Approx Max-3-SAT')
    if bound_vs_exact:
        x_sizes, x_bounds, x_exact = zip(*bound_vs_exact)
        plt.plot(x_sizes, x_exact, 'm*:', label='Exact Optimal')
    plt.xlabel('Input Size (Number of Clauses m)')
    plt.ylabel('Satisfied Clauses')
    plt.title('Optimal and Approximation vs Bound')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig('pictures/approx_vs_bound.png')
    print("Saved approx_vs_bound.png")


if __name__ == "__main__":
    main()
