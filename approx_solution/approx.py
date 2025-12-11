#!/usr/bin/env python3
"""
Faster Max-3-SAT anytime approximation using WalkSAT-style local search
Keeps input/output format identical to the original program.
"""
import random
import sys
import time
from multiprocessing import Process, Pipe
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Max-3-SAT WalkSAT-style anytime solver")
    parser.add_argument("-t", type=int, default=2,
                        help="Amount of time for program to run (in seconds)")
    parser.add_argument("-p", type=int, default=1,
                        help="The number of parallel processes to use")
    parser.add_argument("filename", type=str, nargs='?', default="-",
                        help="Input file name (default: read from stdin)")
    return parser.parse_args()

def read_input():
    n, m = map(int, sys.stdin.readline().strip().split())
    clauses = []
    for _ in range(m):
        a, b, c = map(int, sys.stdin.readline().strip().split())
        clauses.append((a, b, c))
    return n, m, clauses

def read_file(filename):
    with open(filename, 'r') as f:
        n, m = map(int, f.readline().strip().split())
        clauses = []
        for _ in range(m):
            a, b, c = map(int, f.readline().strip().split())
            clauses.append((a, b, c))
    return n, m, clauses

# helper: literal satisfied given assignment list (1..n)
def literal_satisfied(lit, assign):
    if lit > 0:
        return assign[lit]
    else:
        return not assign[-lit]

def initial_assignment(n):
    # list indexed 0..n, ignore index 0 for simplicity
    return [False] + [bool(random.getrandbits(1)) for _ in range(n)]

def build_occurrences(n, clauses):
    """Build pos_occ and neg_occ: for each var, list of clause indices where it appears"""
    m = len(clauses)
    pos_occ = [[] for _ in range(n+1)]
    neg_occ = [[] for _ in range(n+1)]
    for i, cl in enumerate(clauses):
        a,b,c = cl
        for lit in (a,b,c):
            v = abs(lit)
            if lit > 0:
                pos_occ[v].append(i)
            else:
                neg_occ[v].append(i)
    return pos_occ, neg_occ

def evaluate_initial_true_counts(clauses, assign):
    """Return true_count list and initial satisfied count"""
    m = len(clauses)
    true_count = [0]*m
    sat = 0
    for i, cl in enumerate(clauses):
        a,b,c = cl
        cnt = 0
        if literal_satisfied(a, assign): cnt += 1
        if literal_satisfied(b, assign): cnt += 1
        if literal_satisfied(c, assign): cnt += 1
        true_count[i] = cnt
        if cnt > 0: sat += 1
    return true_count, sat

def compute_flip_gain(var, clauses, assign, true_count, pos_occ, neg_occ):
    """
    Compute change in number of satisfied clauses (delta) when flipping var.
    Only iterates clauses where var occurs.
    """
    delta = 0
    # if var is True now, flipping will make it False, and vice versa
    cur_val = assign[var]
    # positive occurrences: literal is var
    for ci in pos_occ[var]:
        cur_cnt = true_count[ci]
        # contribution before flip: var contributes if cur_val True
        contrib_before = 1 if cur_val else 0
        contrib_after = 1 if (not cur_val) else 0
        new_cnt = cur_cnt - contrib_before + contrib_after
        # clause satisfaction change: was satisfied? will be?
        if (cur_cnt > 0) and (new_cnt == 0):
            delta -= 1
        elif (cur_cnt == 0) and (new_cnt > 0):
            delta += 1
    # negative occurrences: literal is ¬var
    for ci in neg_occ[var]:
        cur_cnt = true_count[ci]
        # contribution before flip: ¬var contributes if cur_val is False
        contrib_before = 1 if (not cur_val) else 0
        contrib_after = 1 if (not (not cur_val)) else 0  # after flip, var becomes not cur_val
        # but simpler: contrib_after = 1 if cur_val else 0
        contrib_after = 1 if cur_val else 0
        new_cnt = cur_cnt - contrib_before + contrib_after
        if (cur_cnt > 0) and (new_cnt == 0):
            delta -= 1
        elif (cur_cnt == 0) and (new_cnt > 0):
            delta += 1
    return delta

def do_flip(var, assign, true_count, clauses, pos_occ, neg_occ):
    """Flip var and update true_count. Return new satisfied count change (delta)."""
    cur_val = assign[var]
    delta = 0
    # positive occurrences
    for ci in pos_occ[var]:
        # compute contribution delta for this clause
        # contribution before flip
        contrib_before = 1 if cur_val else 0
        contrib_after = 1 if (not cur_val) else 0
        prev_cnt = true_count[ci]
        new_cnt = prev_cnt - contrib_before + contrib_after
        # update true_count
        true_count[ci] = new_cnt
        if prev_cnt == 0 and new_cnt > 0:
            delta += 1
        elif prev_cnt > 0 and new_cnt == 0:
            delta -= 1
    # negative occurrences
    for ci in neg_occ[var]:
        contrib_before = 1 if (not cur_val) else 0
        contrib_after = 1 if cur_val else 0
        prev_cnt = true_count[ci]
        new_cnt = prev_cnt - contrib_before + contrib_after
        true_count[ci] = new_cnt
        if prev_cnt == 0 and new_cnt > 0:
            delta += 1
        elif prev_cnt > 0 and new_cnt == 0:
            delta -= 1
    # perform flip
    assign[var] = not cur_val
    return delta

def walk_sat_anytime(n, m, clauses, time_limit=1.0, p_random_walk=0.4, max_flips_per_try=1000):
    """
    WalkSAT-style local search with restarts.
    - p_random_walk: probability to flip a random variable in an unsatisfied clause
    - max_flips_per_try: flips before a random restart
    """
    start = time.time()
    pos_occ, neg_occ = build_occurrences(n, clauses)

    best_assign = None
    best_score = -1
    history = []

    # keep running until time limit
    while time.time() - start < time_limit:
        # random restart
        assign = initial_assignment(n)
        true_count, sat = evaluate_initial_true_counts(clauses, assign)
        if sat > best_score:
            best_score = sat
            best_assign = assign.copy()
            history.append((time.time()-start, best_score))
            if best_score == m:
                break

        flips = 0
        # central loop for this restart
        while flips < max_flips_per_try and (time.time() - start < time_limit):
            if sat == m:
                # perfect assignment
                if sat > best_score:
                    best_score = sat
                    best_assign = assign.copy()
                    history.append((time.time()-start, best_score))
                return best_score, best_assign, history

            # pick unsatisfied clause uniformly
            # we can sample by scanning for a random unsatisfied clause; since clauses are small,
            # this is acceptable. To avoid O(m) scan every time, we do one cheap sample attempt:
            # pick a random clause and check if unsatisfied; try up to 5 times, else scan collect unsat list once.
            chosen_clause_index = None
            for _ in range(5):
                ci = random.randrange(m)
                if true_count[ci] == 0:
                    chosen_clause_index = ci
                    break
            if chosen_clause_index is None:
                # fallback: scan to build unsatisfied list
                unsat = [i for i in range(m) if true_count[i] == 0]
                if not unsat:
                    # all satisfied
                    if sat > best_score:
                        best_score = sat
                        best_assign = assign.copy()
                        history.append((time.time()-start, best_score))
                    break
                chosen_clause_index = random.choice(unsat)

            a,b,c = clauses[chosen_clause_index]
            lits = (a,b,c)
            # with prob p_random_walk flip a random var from clause
            if random.random() < p_random_walk:
                lit = random.choice(lits)
                var = abs(lit)
                delta = do_flip(var, assign, true_count, clauses, pos_occ, neg_occ)
                sat += delta
            else:
                # choose variable in clause that gives best gain (max increase in satisfied clauses)
                best_var = None
                best_gain = -10**9
                for lit in lits:
                    var = abs(lit)
                    gain = compute_flip_gain(var, clauses, assign, true_count, pos_occ, neg_occ)
                    if gain > best_gain:
                        best_gain = gain
                        best_var = var
                # tie-breaker randomness
                if best_var is None:
                    best_var = abs(random.choice(lits))
                    best_gain = compute_flip_gain(best_var, clauses, assign, true_count, pos_occ, neg_occ)
                delta = do_flip(best_var, assign, true_count, clauses, pos_occ, neg_occ)
                sat += delta

            flips += 1

            # record best
            if sat > best_score:
                best_score = sat
                best_assign = assign.copy()
                history.append((time.time()-start, best_score))
                if best_score == m:
                    return best_score, best_assign, history

        # end of restart, continue if time remains
    return best_score, best_assign, history

def worker(n, m, clauses, time_limit, conn):
    score, assign, _ = walk_sat_anytime(n, m, clauses, time_limit=time_limit)
    conn.send((score, assign))
    conn.close()

def main():
    args = parse_args()
    filename = args.filename
    # If not file specified, read from stdin
    if filename == "-":
        n, m, clauses = read_input()
    else:
        n, m, clauses = read_file(filename)

    # Ensure parameters are valid
    time_limit = max(1, args.t)
    threads = max(1, args.p)

    if threads == 1:
        best_score, best_assign, _ = walk_sat_anytime(n, m, clauses, time_limit=time_limit)
    else:
        processes = []
        conns = []
        for i in range(threads):
            parent_conn, child_conn = Pipe()
            p = Process(target=worker, args=(n, m, clauses, time_limit, child_conn))
            p.start()
            processes.append(p)
            conns.append(parent_conn)

        for p in processes:
            p.join()

        best_score = -1
        best_assign = None
        for conn in conns:
            score, assign = conn.recv()
            if score > best_score:
                best_score = score
                best_assign = assign

    # ensure we have an assignment (if none found, create a random one)
    if best_assign is None:
        best_assign = initial_assignment(n)

    print(best_score)
    for i in range(1, n+1):
        print(i, "T" if best_assign[i] else "F")

if __name__ == "__main__":
    main()
