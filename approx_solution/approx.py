"""
Approximation solution for Max 3-SAT using an anytime random-assignment algorithm.

This program reads a Max-3-SAT instance, repeatedly generates random assignments,
evaluates the number of satisfied clauses, and keeps the best assignment found 
within a fixed time limit.

** Input Format **
The first line contains two integers:
    n  m
where n is the number of boolean variables and m is the number of clauses.
Variables are numbered 1 through n.

Each of the next m lines contains three integers representing a clause.
A positive integer k represents the literal x_k, and a negative integer -k
represents the negated literal ¬x_k. Each clause has exactly three literals.

Example:
    4 3
    1 -2 3
    -1 2 -4
    3 4 -2

** Output Format **
The first line prints the maximum number of clauses satisfied by the best 
assignment found by the algorithm.

This is followed by n lines, one per variable, in this format:
    variable_number  T/F
where T means the variable is assigned True and F means False.

Example:
    2
    1 T
    2 F
    3 T
    4 F

This algorithm is anytime: it can be stopped at any moment and always has a 
valid best-so-far assignment.

Use dimacs format for testing.
"""

import random
import sys
import time
import threading
import matplotlib.pyplot as plt
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="My program description")

    # Add integer flags -t and -p
    parser.add_argument("-t", type=int, required=True,
                        help="Amount of time for program to run (in seconds)")

    parser.add_argument("-p", type=int, required=True,
                        help="The number of parrallel processes to use")

    # Positional filename argument
    parser.add_argument("filename", type=str,
                        help="Input file name")

    return parser.parse_args()

def read_input():
    """Reads n, m, then m clauses of 3 literals each."""
    n, m = map(int, sys.stdin.readline().strip().split())
    clauses = []
    for _ in range(m):
        a, b, c = map(int, sys.stdin.readline().strip().split())
        clauses.append((a, b, c))
    return n, m, clauses

def read_file(filename):
    """Reads n, m, then m clauses of 3 literals each from a file."""
    with open(filename, 'r') as f:
        n, m = map(int, f.readline().strip().split())
        clauses = []
        for _ in range(m):
            a, b, c = map(int, f.readline().strip().split())
            clauses.append((a, b, c))
    return n, m, clauses


def evaluate(clauses, assignment):
    """Count satisfied clauses under assignment."""
    sat = 0
    for (a, b, c) in clauses:
        if ((a > 0 and assignment[a]) or (a < 0 and not assignment[-a]) or
            (b > 0 and assignment[b]) or (b < 0 and not assignment[-b]) or
            (c > 0 and assignment[c]) or (c < 0 and not assignment[-c])):
            sat += 1
    return sat


def random_assignment(n):
    """Generate a random True/False assignment for n variables."""
    return {i: bool(random.getrandbits(1)) for i in range(1, n+1)}


def anytime_max3sat(n, m, clauses, time_limit=1.0):
    """
    Anytime Max-3-SAT approximation algorithm.

    Randomly generates complete assignments to all n variables and evaluates
    how many of the m clauses are satisfied. Continues generating random
    assignments until the time_limit (in seconds) is reached.

    Returns:
        (best_score, best_assignment, history)
        history: list of (elapsed_seconds, best_score) when a new best was found
    """
    start = time.time()
    best_assign = None
    best_score = -1
    history = []

    while time.time() - start < time_limit:
        if best_score == m:
            break  # Optimal solution found
        assign = random_assignment(n)
        score = evaluate(clauses, assign)
        if score > best_score:
            best_score = score
            best_assign = assign
            elapsed = time.time() - start
            history.append((elapsed, best_score))

    return best_score, best_assign, history


def main():
    """Main function to read input, run the algorithm, and print output."""
    args = parse_args()
    filename = args.filename
    n, m, clauses = read_file(filename)
    time_limit = args.t  # Use -t argument as time limit in seconds
    
    print("Running anytime Max-3-SAT approximation...")
    best_score, best_assign, history = anytime_max3sat(n, m, clauses, time_limit=time_limit)

    # Output format
    print(best_score)
    for i in range(1, n+1):
        print(i, "T" if best_assign[i] else "F")

    # Plot best score over time and save figure
    if history:
        times, scores = zip(*history)
        times = list(times)
        scores = list(scores)
        
        # Add final point at time_limit to show flat line
        if times[-1] < time_limit:
            times.append(time_limit)
            scores.append(scores[-1])
        
        plt.figure()
        plt.axhline(y=m, color='r', linestyle='--', label='Number of Clauses (m)')
        plt.plot(times, scores, marker='o', label='Best score over time')
        plt.legend()
        plt.xlabel('Time (s)')
        plt.ylabel('Best score (satisfied clauses)')
        plt.title('Max-3-SAT: best score over time')
        plt.grid(True)
        plt.tight_layout()
        plt.savefig('best_score_over_time.png')
        plt.show()
        plt.close()


if __name__ == "__main__":
    main()