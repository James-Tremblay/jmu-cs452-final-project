Reduction Solution - Max 3-SAT to Max Clique
============================================

This folder contains the reduction from Max 3-SAT to Max Clique.

Files:
------
- reduction.py: Performs the reduction and computes the upper bound.
- exact_max.py: Exact solver for Max 3-SAT (finds max satisfied clauses) used for comparison.
- driver.py: Runs the reduction and solvers on all test cases.
- plot_results.py: Generates plots from the results.
- results.csv: Output of driver.py.
- test_cases/: Directory containing test inputs.

Reduction Description:
----------------------
The reduction transforms a Max 3-SAT instance into a Max Clique instance (Graph).
For a 3-SAT instance with m clauses, we construct a graph G=(V, E) such that:
- V has 3m vertices (one for each literal in each clause).
- E connects two vertices if and only if:
  1. They correspond to literals in DIFFERENT clauses.
  2. They are CONSISTENT (i.e., not negations of each other, x and -x).

The size of the Maximum Clique in G is equal to the maximum number of simultaneously satisfiable clauses in the 3-SAT instance.

Running Time Analysis:
----------------------
Let m be the number of clauses in the Max 3-SAT instance.
The reduction algorithm proceeds as follows:
1. Create Vertices: We iterate through all m clauses, creating 3 vertices for each. This takes O(m) time.
2. Create Edges: We iterate through all pairs of vertices to determine if an edge exists.
   - Number of vertices N = 3m.
   - Number of pairs is N(N-1)/2 = O(N^2) = O(m^2).
   - Checking consistency takes O(1).

Total Running Time: O(m^2).
Since the input size is proportional to m, this is a polynomial-time reduction.

Bound Calculation:
------------------
The Upper Bound for the maximum number of satisfied clauses is simply m (the total number of clauses).
This calculation takes O(1) time (after reading input).

Usage:
------
1. To run the reduction on a single input (reads from stdin):
   
   python3 reduction.py < input.txt

   Output: DIMACS format graph (to stdout).

2. To compute the upper bound only:

   python3 reduction.py --bound < input.txt

   Output: Integer upper bound.

3. To run the full test suite and generate results:

   cd "reduced solution"
   python3 driver.py

   This will generate 'results.csv'.

4. To generate plots:

   python3 plot_results.py

   This will generate 'reduction_time.png' and 'solution_quality.png'.

Example Command Line:
---------------------
python3 reduction.py < test_cases/test_case1.txt

