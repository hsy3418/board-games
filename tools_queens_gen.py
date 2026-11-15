"""Generate 'Bunny Formation' (Star Battle 1★ / Queens-style) puzzles with a unique solution.
N x N grid, N regions; one rabbit per row, column and region; no two rabbits touch (incl. diagonally)."""
import random, json, sys

def solutions(N, reg, limit=2):
    """count solutions (up to limit), plus number of search nodes as a rough difficulty signal"""
    cols, regs = [False]*N, [False]*N
    sol, cnt, nodes = [], [0], [0]
    def rec(r, prevc):
        if cnt[0] >= limit: return
        if r == N: cnt[0] += 1; return
        for c in range(N):
            nodes[0] += 1
            if cols[c] or regs[reg[r][c]] or (prevc is not None and abs(c - prevc) <= 1): continue
            cols[c] = regs[reg[r][c]] = True; sol.append(c)
            rec(r + 1, c)
            cols[c] = regs[reg[r][c]] = False; sol.pop()
    rec(0, None)
    return cnt[0], nodes[0]

def queens(N):
    while True:
        p = list(range(N)); random.shuffle(p)
        if all(abs(p[i] - p[i+1]) > 1 for i in range(N - 1)): return p

def grow(N, q):
    reg = [[-1]*N for _ in range(N)]
    frontier = []
    for r, c in enumerate(q): reg[r][c] = r; frontier.append((r, c))
    left = N*N - N
    while left:
        r, c = random.choice(frontier)
        nb = [(r+dr, c+dc) for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)) if 0 <= r+dr < N and 0 <= c+dc < N and reg[r+dr][c+dc] < 0]
        if not nb: frontier.remove((r, c)); continue
        rr, cc = random.choice(nb); reg[rr][cc] = reg[r][c]; frontier.append((rr, cc)); left -= 1
    return reg

def connected(N, reg, k):
    cells = [(r, c) for r in range(N) for c in range(N) if reg[r][c] == k]
    if not cells: return False
    seen, st = {cells[0]}, [cells[0]]
    while st:
        r, c = st.pop()
        for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
            n = (r+dr, c+dc)
            if 0 <= n[0] < N and 0 <= n[1] < N and n not in seen and reg[n[0]][n[1]] == k: seen.add(n); st.append(n)
    return len(seen) == len(cells)

def make(N, tries=4000):
    q = queens(N); reg = grow(N, q)
    qcells = {(r, c) for r, c in enumerate(q)}
    best = solutions(N, reg)[0]
    for _ in range(tries):
        if best == 1: break
        # move a random boundary cell (never a queen cell) into a neighbouring region, keep regions connected
        r, c = random.randrange(N), random.randrange(N)
        if (r, c) in qcells: continue
        nbs = {reg[r+dr][c+dc] for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)) if 0 <= r+dr < N and 0 <= c+dc < N} - {reg[r][c]}
        if not nbs: continue
        old = reg[r][c]; reg[r][c] = random.choice(list(nbs))
        if not connected(N, reg, old): reg[r][c] = old; continue
        n = solutions(N, reg)[0]
        if n >= 1 and n <= best: best = n
        else: reg[r][c] = old
    if best != 1: return None
    return {'n': N, 'r': [''.join('abcdefghij'[x] for x in row) for row in reg], 's': q, 'd': solutions(N, reg)[1]}

random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 20261115)
plan = json.loads(sys.argv[3]) if len(sys.argv) > 3 else {6: 30, 7: 30, 8: 30, 9: 25, 10: 15}
plan = {int(k): v for k, v in plan.items()}
out = []
for N, k in plan.items():
    got = 0
    while got < k:
        p = make(N)
        if p: out.append(p); got += 1
    print(N, 'done', file=sys.stderr)
json.dump(out, open(sys.argv[2] if len(sys.argv) > 2 else 'puzzles.json', 'w'), separators=(',', ':'))
print(len(out), 'puzzles', file=sys.stderr)
