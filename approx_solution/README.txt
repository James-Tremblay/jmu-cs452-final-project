 n = number of variables
m = number of clauses
The cost per flip is O(m/n). 
Since this runs for a constant number for flips, 
the runtime for a single restart is O(m/n). 
Since most of time m>>n, it is closer to O(m).


====================================
Example Run:
====================================
PS C:\Users\charl\OneDrive\Documents\Fall2025\CS452\np_project> python approx_solution\approx.py approx_solution\test_cases\hard01.txt
565
1 F
2 F
3 T
4 F
5 T
6 T
7 F
8 T
9 F
10 F
11 F
12 F
13 T
14 T
15 F
16 F
17 F
18 T
19 F
20 F
21 T
22 T
23 T
24 T
25 T
26 T
27 F
28 T
29 T
30 F
31 T
32 T
33 F
34 F
35 T
36 T
37 F
38 F
39 T
40 T
41 T
42 F
43 F
44 T
45 F
46 F
47 F
48 T
49 F
50 T
51 T
52 F
53 T
54 F
55 F
56 F
57 T
58 T
59 T
60 T
61 F
62 T
63 F
64 F
65 T
66 T
67 T
68 T
69 F
70 T
71 F
72 T
73 F
74 T
75 T
76 F
77 T
78 F
79 F
80 T
81 T
82 T
83 F
84 T
85 F
86 T
87 F
88 F
89 T
90 T
91 F
92 T
93 F
94 F
95 F
96 F