import csv
import matplotlib.pyplot as plt
import sys

def main():
    results_file = "results.csv"
    
    sizes = []
    optimals = []
    bounds = []
    approxs = []
    times = []
    
    try:
        with open(results_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                sizes.append(int(row["Input Size (m)"]))
                optimals.append(int(row["Optimal"]))
                bounds.append(int(row["Bound"]))
                approxs.append(int(row["Approx"]))
                times.append(float(row["Reduction Time"]))
    except FileNotFoundError:
        print("results.csv not found. Run driver.py first.")
        return

    # Sort by size for better plotting
    data = sorted(zip(sizes, optimals, bounds, approxs, times))
    sizes, optimals, bounds, approxs, times = zip(*data)

    # Plot 1: Reduction Time vs Input Size
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, times, 'bo-', label='Reduction Time')
    plt.xlabel('Input Size (Number of Clauses m)')
    plt.ylabel('Time (seconds)')
    plt.title('Reduction Wall Clock Time vs Input Size')
    plt.grid(True)
    plt.legend()
    plt.savefig('reduction_time.png')
    print("Saved reduction_time.png")
    
    # Plot 2: Optimal vs Bound vs Approx
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, bounds, 'r--', label='Upper Bound')
    plt.plot(sizes, optimals, 'g*-', label='Optimal Value')
    plt.plot(sizes, approxs, 'b.-', label='Approx Value')
    
    plt.xlabel('Input Size (Number of Clauses m)')
    plt.ylabel('Number of Satisfied Clauses')
    plt.title('Solution Quality Comparison')
    plt.grid(True)
    plt.legend()
    plt.savefig('solution_quality.png')
    print("Saved solution_quality.png")

if __name__ == "__main__":
    main()

