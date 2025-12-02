import re
from typing import List, Dict, Tuple

# --- INPUT FORMAT SPECIFICATION ---
# Max 3-SAT Input: A list of clauses, where each clause is a tuple of 3 literals.
# A literal is represented as a string: 'xN' for variable X_N, or '~xN' for NOT X_N.
# Example: (x1 OR ~x2 OR x3) AND (~x1 OR x2 OR ~x3)
# Input is parsed into: [('x1', '~x2', 'x3'), ('~x1', 'x2', '~x3')]

# --- OUTPUT FORMAT SPECIFICATION ---
# Max Clique Output: A graph G = (V, E) represented by an adjacency list.
# The graph is represented by a dictionary where keys are vertex IDs (integers)
# and values are lists of connected vertex IDs. The problem statement on Canvas
# specifies the exact output format for Max Clique (usually an adjacency matrix
# or list). We will use a simple adjacency list (dictionary) for demonstration,
# which can be easily adapted to the required output format.

def parse_literal(literal_str: str) -> Tuple[str, bool]:
    """
    Parses a literal string into its variable name and its negation status.
    e.g., 'x5' -> ('x5', False); '~x3' -> ('x3', True)
    """
    if literal_str.startswith('~'):
        return literal_str[1:], True  # (Variable name, is_negated=True)
    return literal_str, False # (Variable name, is_negated=False)

def check_contradiction(lit1: str, lit2: str) -> bool:
    """
    Checks if two literals are mutually contradictory (e.g., x1 and ~x1).
    This function is the heart of the reduction's edge rule.
    """
    var1, neg1 = parse_literal(lit1)
    var2, neg2 = parse_literal(lit2)

    # Contradiction occurs if:
    # 1. They are the same variable (var1 == var2)
    # 2. They have opposite polarities (neg1 != neg2)
    return var1 == var2 and neg1 != neg2

def max3sat_to_maxclique(clauses: List[Tuple[str, str, str]]) -> Dict[int, List[int]]:
    """
    Reduces a Max 3-SAT instance to a Max Clique instance (Adjacency List).
    The size of the maximum clique in the resulting graph is equal to the
    maximum number of satisfiable clauses in the Max 3-SAT instance.

    Args:
        clauses: A list of 3-literal clauses.

    Returns:
        An adjacency list representation of the resulting graph (Max Clique input).
    """
    V = [] # List to store all vertices (literal, clause_index, vertex_id)
    adj_list = {} # The adjacency list for the resulting graph

    # 1. Create the Vertices (V)
    vertex_id = 0
    for clause_index, clause in enumerate(clauses):
        for literal in clause:
            # Each vertex is uniquely identified by an ID and stores its
            # literal and the index of the clause it came from.
            V.append({'id': vertex_id, 'literal': literal, 'clause_idx': clause_index})
            adj_list[vertex_id] = []
            vertex_id += 1

    M = len(clauses)
    N = len(V) # Total number of vertices (3 * M)

    # 2. Create the Edges (E)
    # This loop runs in O((3M)^2) = O(M^2), which is polynomial time.
    for i in range(N):
        for j in range(i + 1, N):
            u = V[i]
            v = V[j]

            # Rule 1: Edges only between literals from DIFFERENT clauses
            if u['clause_idx'] != v['clause_idx']:
                # Rule 2: Edges only between literals that are NOT contradictory
                if not check_contradiction(u['literal'], v['literal']):
                    # Add bidirectional edge
                    adj_list[u['id']].append(v['id'])
                    adj_list[v['id']].append(u['id'])

    return adj_list

# ====================================================================
# EXAMPLE USAGE
# ====================================================================

# Max 3-SAT instance (2 variables, 3 clauses)
# C1: (x1 OR x2 OR x2)
# C2: (~x1 OR ~x2 OR x1)
# C3: (~x1 OR x2 OR x1)

max3sat_input = [
    ('x1', 'x2', 'x2'),      # C0
    ('~x1', '~x2', 'x1'),    # C1
    ('~x1', 'x2', 'x1')      # C2
]

# The reduction algorithm call
maxclique_output = max3sat_to_maxclique(max3sat_input)

# --- Output generation for Max Clique ---
print("--- MAX 3-SAT TO MAX CLIQUE REDUCTION OUTPUT ---")
print(f"Input: {len(max3sat_input)} clauses")
print(f"Output: Graph with {len(maxclique_output)} vertices (Nodes: 0 to {len(maxclique_output) - 1})")
print("\nAdjacency List (Vertex ID: [Neighbors])")

# Print the resulting adjacency list
for vertex_id, neighbors in maxclique_output.items():
    print(f"{vertex_id}: {sorted(neighbors)}")

# Example of how the problem sizes relate:
M = len(max3sat_input)
N_vertices = 3 * M
print(f"\nReduction Time Complexity: O(M^2) where M is the number of clauses.")
print(f"This is polynomial time (O(N^2) on the resulting graph size, N=3M).")

# The optimal solution to this Max 3-SAT is 3 (all clauses can be satisfied, e.g., x1=True, x2=True).
# Thus, the Max Clique size in this graph should be 3.
# The Max Clique problem is NP-Hard, so we don't solve it here, only output the instance.