Reduction Solution - Max 3-SAT to MIS
=====================================

Running Time Analysis:
----------------------
Let c be the number of clauses in the Max 3-SAT instance. The reduction
performs the following work:

1. Create Vertices: iterate through every clause (O(c)) and append three
   vertices.
2. Create Edges: iterate through all pairs of literals (there are 3c literals),
   which is O((3c)^2) = O(c^2) pairs. Checking whether an edge should be added
   is O(1).

Total Running Time: O(c^2). Because the reduction only depends on c (the number
of clauses), the transformation is polynomial.

Bound Calculation:
------------------
The trivial upper bound on the number of simultaneously satisfied clauses is
m (one per clause). `reduction.py --bound` prints this in O(1) time after
parsing n and m.

Usage:
------
1. Reduction only:

   python3 reduction.py < test_cases/test_case1.txt

2. Bound only:

   python3 reduction.py --bound < test_cases/test_case1.txt

3. Full pipeline (runs MIS solver and SAT approximation across all 150 cases):

   cd "reduced solution"
   python3 driver.py

4. Plot runtime and correctness evidence:

   python3 plot_results.py
