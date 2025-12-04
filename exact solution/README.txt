The O runtime of the exact solution is... 

O(m * 2^n)

As there are 2^n total possible assignments for my program to make, and for each assignment
it evaluates all m clauses and counts how many it satisfies. Thus m * 2^n

Example command line usage:
python3 exact.py test_cases/test_case1.txt

which produces
10
1 F
2 F
3 F
4 F
5 F
6 F
7 F
8 F
