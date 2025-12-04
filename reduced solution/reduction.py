import sys
import time

def parse_input():
    """
    Reads Max 3-SAT input from stdin.
    Expected format:
    n m
    l1 l2 l3
    ...
    """
    try:
        input_data = sys.stdin.read().strip().split()
        if not input_data:
            return None
        
        iterator = iter(input_data)
        try:
            n = int(next(iterator))
            m = int(next(iterator))
        except StopIteration:
            return None

        clauses = []
        for _ in range(m):
            try:
                l1 = int(next(iterator))
                l2 = int(next(iterator))
                l3 = int(next(iterator))
                clauses.append((l1, l2, l3))
            except StopIteration:
                break
        
        return n, m, clauses
    except Exception as e:
        sys.stderr.write(f"Error parsing input: {e}\n")
        return None

def is_consistent(l1, l2):
    """
    Check if two literals are consistent (i.e., not negations of each other).
    """
    return l1 != -l2


def reduce_to_independent_set(n, c, clauses):
    """
    Reduces Max 3-SAT to Maximum Independent Set (MIS).
    
    From the problem description:
    The graph G contains exactly 3k vertices (where k=c is the number of clauses).
    Two vertices in G are connected by an edge if:
    1. They correspond to literals in the SAME clause (forming a triangle per clause).
    2. They correspond to a variable and its inverse (contradictory literals).
    
    Runtime: O(c^2) where c is the number of clauses.
    Returns (num_vertices, edges)
    """
    edges = []
    num_vertices = 3 * c
    
    # List of literals with their clause index (clause_idx, literal_value)
    flat_literals = []
    for i, clause in enumerate(clauses):
        for lit in clause:
            flat_literals.append((i, lit))
            
    #  Build edges: Iterate over all pairs of vertices
    for i in range(len(flat_literals)):
        for j in range(i + 1, len(flat_literals)):
            c1_idx, l1 = flat_literals[i]
            c2_idx, l2 = flat_literals[j]
            
            is_connected = False
            
            # Condition 1: Literals in the SAME clause
            if c1_idx == c2_idx:
                is_connected = True
            
            # Condition 2: Variable and its inverse (Contradictory)
            elif l1 == -l2:
                is_connected = True
            
            if is_connected:
                # Add edge (1-based indices)
                u = i + 1
                v = j + 1
                edges.append((u, v))
                
    return num_vertices, edges

def compute_bound(n, c, clauses):
    """
    Computes an upper bound on the max number of satisfied clauses.
    Returns: c (total clauses).
    """
    return c

def main():
    """
    Main function to handle command line arguments and input parsing.
    """
    compute_bound_only = len(sys.argv) > 1 and sys.argv[1] == "--bound"
    
    data = parse_input()
    if not data:
        sys.stderr.write("Failed to read input\n")
        sys.exit(1)
        
    n, m, clauses = data
    
    if compute_bound_only:
        print(compute_bound(n, m, clauses))
        return
    
    num_vertices, edges = reduce_to_independent_set(n, m, clauses)
    
    # Output format for Maximum Independent Set (MIS)
    print(len(edges))
    for u, v in edges:
        print(f"{u} {v}")

if __name__ == "__main__":
    main()
