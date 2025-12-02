import itertools
import time

def verify(clauses, assignment):
    # NP verifier: checks a single assignment in polynomial time
    for clause in clauses:
        satisfied = False
        for lit in clause:
            v = abs(lit)
            val = assignment[v]
            if (lit > 0 and val) or (lit < 0 and not val):
                satisfied = True
                break
        if not satisfied:
            return False
    return True

def solve_3sat(num_vars, clauses):
    # Brute force enumeration using itertools (explicitly allowed by project)
    for combo in itertools.product([False, True], repeat=num_vars):
        assignment = [None] + list(combo)
        if verify(clauses, assignment):
            return assignment
    return None

def load_instance(path):
    with open(path) as f:
        first = f.readline().split()
        num_vars, num_clauses = map(int, first)
        clauses = []
        for _ in range(num_clauses):
            a, b, c = map(int, f.readline().split())
            clauses.append((a, b, c))
    return num_vars, clauses

def main():
    num_vars, clauses = load_instance("input.txt")
    start = time.time()
    result = solve_3sat(num_vars, clauses)
    end = time.time()

    print("runtime:", end - start, "seconds")

    if result:
        print("SAT")
        print("assignment:", result[1:])
    else:
        print("UNSAT")

if __name__ == "__main__":
    main()
