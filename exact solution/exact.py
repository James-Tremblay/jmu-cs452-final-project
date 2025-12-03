#!/usr/bin/env python3
import sys, time, itertools

def clause_sat(clause, a):
    return any((lit > 0 and a[lit-1]) or (lit < 0 and not a[-lit-1]) for lit in clause)

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
