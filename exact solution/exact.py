#!/usr/bin/env python3
import sys, time, itertools

def clause_sat(clause, assignment):
    a, b, c = clause
    return (
        (a > 0 and assignment[a-1]) or (a < 0 and not assignment[-a-1]) or
        (b > 0 and assignment[b-1]) or (b < 0 and not assignment[-b-1]) or
        (c > 0 and assignment[c-1]) or (c < 0 and not assignment[-c-1])
    )

def main():
    path = sys.argv[1]
    with open(path) as f:
        n, m = map(int, f.readline().split())
        clauses = [tuple(map(int, f.readline().split())) for _ in range(m)]

    start = time.time()

    best_val = -1
    best_assignment = None
    
    for a in itertools.product([False, True], repeat=n):
        val = sum(clause_sat(c, a) for c in clauses)
        if val > best_val:
            best_val = val
            best_assignment = a
            
    runtime = time.time() - start

    print(best_val)
    for i, val in enumerate(best_assignment, start=1):
        print(f"{i} {'T' if val else 'F'}")

if __name__ == "__main__":
    main()
