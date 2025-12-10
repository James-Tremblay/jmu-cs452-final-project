Reduction Solution - Max 3-SAT to MIS
=====================================

This folder contains the reduction from Max 3-SAT to Maximum Independent Set
(MIS). A Max Clique reduction is still available via `reduction.py --clique`,
but the default output (and all automation) now targets MIS so that we can feed
the reduced instance directly into the provided `max_ind_set.py` heuristic.

Files:
------
- reduction.py: Performs the reduction to MIS or Max Clique and computes the upper bound.
- max_ind_set.py: Heuristic/anytime solver that approximates MIS on the reduced graph.
- driver.py: Automates the entire pipeline across every test case.
- plot_results.py: Generates the comparison plots from `results.csv`.
- results.csv: Output metrics produced by `driver.py`.
- test_cases/: Directory containing 50 Max 3-SAT instances.

Reduction Description:
----------------------
The reduction transforms a Max 3-SAT instance with m clauses into a graph
G = (V, E) that has exactly 3m vertices (one per literal per clause).

Two vertices are connected by an edge if and only if **one** of the following
holds:

1. The vertices come from the SAME clause (forming a triangle within every clause).
2. The literals correspond to a variable and its negation (they cannot both be
   chosen in a satisfying assignment).

Any independent set in G therefore contains at most one literal from each
clause and never includes contradictory literals. Consequently, the size of
the maximum independent set equals the number of clauses that can be satisfied
simultaneously in the original Max 3-SAT instance.

Running Time Analysis:
----------------------
Let m be the number of clauses in the Max 3-SAT instance. The reduction
performs the following work:

1. Create Vertices: iterate through every clause (O(m)) and append three
   vertices.
2. Create Edges: iterate through all pairs of literals (there are 3m literals),
   which is O((3m)^2) = O(m^2) pairs. Checking whether an edge should be added
   is O(1).

Total Running Time: O(m^2). Because the reduction only depends on m (the number
of clauses), the transformation is polynomial.

Bound Calculation:
------------------
The trivial upper bound on the number of simultaneously satisfied clauses is
m (one per clause). `reduction.py --bound` prints this in O(1) time after
parsing n and m.

Usage:
------
1. Reduction only (reads from stdin):

   python3 reduction.py < test_cases/test_case1.txt

2. Bound only:

   python3 reduction.py --bound < test_cases/test_case1.txt

3. Full pipeline (runs MIS solver and SAT approximation across all 50 cases):

   cd "reduced solution"
   python3 driver.py

   Produces `results.csv` with the following columns:
   - Clauses (m)
   - Bound (always m for this reduction)
   - Approx MaxSAT (score from approx_solution/approx.py with a 1s budget)
   - MIS Independent Set (size returned by max_ind_set.py on the reduced graph)
   - Reduction Time (s)
   - MIS Solve Time (s)

4. Plot runtime and correctness evidence:

   python3 plot_results.py

   Generates:
   - runtime_vs_size.png
   - solution_quality.png
   - approx_vs_mis.png

