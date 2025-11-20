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

def read_input():
    """Reads n, m, then m clauses of 3 literals each."""
    n, m = map(int, sys.stdin.readline().strip().split())
    clauses = []
    for _ in range(m):
        a, b, c = map(int, sys.stdin.readline().strip().split())
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
        (best_score, best_assignment)
        best_score      : maximum number of satisfied clauses found
        best_assignment : dictionary mapping variable → True/False
    """
    start = time.time()
    best_assign = None
    best_score = -1

    while time.time() - start < time_limit:
        assign = random_assignment(n)
        score = evaluate(clauses, assign)
        if score > best_score:
            best_score = score
            best_assign = assign

    return best_score, best_assign


def main():
    """Main function to read input, run the algorithm, and print output."""
    n, m, clauses = read_input()

    # you can adjust how long the algorithm runs (in seconds)
    best_score, best_assign = anytime_max3sat(n, m, clauses, time_limit=1.0)

    # Output format
    print(best_score)
    for i in range(1, n+1):
        print(i, "T" if best_assign[i] else "F")


if __name__ == "__main__":
    main()