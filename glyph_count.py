from collections import deque
from itertools import permutations

# Hex grid cube coordinates
DIRECTIONS = [(1,-1,0),(1,0,-1),(0,1,-1),(-1,1,0),(-1,0,1),(0,-1,1)]

def hex_key(h): return (h[0],h[1],h[2])

def neighbors(h):
    return [(h[0]+d[0], h[1]+d[1], h[2]+d[2]) for d in DIRECTIONS]

# Build radius-2 hex grid
all_hexes = set()
for q in range(-2,3):
    for r in range(-2,3):
        s = -q-r
        if abs(s) <= 2:
            all_hexes.add((q,r,s))

HILJ = (0,0,0)

STATIONS = [
    (2,-1,-1),(1,-2,1),(-1,-1,2),(-2,1,1),(-1,2,-1),(1,1,-2),(2,-2,0),(0,-2,2),(-2,0,2)
]

# BFS shortest path between two hexes
def bfs_path(start, end):
    if start == end: return [start]
    queue = deque([[start]])
    visited = {start}
    while queue:
        path = queue.popleft()
        cur = path[-1]
        for nb in neighbors(cur):
            if nb not in all_hexes: continue
            if nb == end: return path + [nb]
            if nb not in visited:
                visited.add(nb)
                queue.append(path + [nb])
    return [start, end]

# Convert path to frozenset of edges
def path_to_edges(path):
    edges = set()
    for i in range(len(path)-1):
        a, b = path[i], path[i+1]
        edges.add((min(a,b), max(a,b)))
    return frozenset(edges)

# Precompute BFS paths between all station pairs and HILJ->station
path_cache = {}
nodes = [HILJ] + STATIONS
for i, a in enumerate(nodes):
    for j, b in enumerate(nodes):
        if i != j:
            path_cache[(a,b)] = bfs_path(a,b)

print(f"Grid: {len(all_hexes)} hexes")
print(f"Stations: {len(STATIONS)}")
print()

# Generate all glyphs from sequences of length 1..8
# A sequence visits N stations (no immediate repeat)
# Glyph = frozenset of edges from HILJ->s[0]->s[1]->...->s[N-1]

base_glyphs = set()
sequence_count = 0

def walk_sequences(current_pos, remaining_stations, current_edges, depth, max_depth):
    global sequence_count
    if depth > 0:
        sequence_count += 1
        base_glyphs.add(frozenset(current_edges))
    if depth == max_depth or not remaining_stations:
        return
    for i, s in enumerate(remaining_stations):
        path = path_cache[(current_pos, s)]
        new_edges = current_edges | path_to_edges(path)
        new_remaining = remaining_stations[:i] + remaining_stations[i+1:]
        walk_sequences(s, new_remaining, new_edges, depth+1, max_depth)

# Use 8 stations (drop one — use first 8)
stations_8 = STATIONS[:8]
walk_sequences(HILJ, stations_8, set(), 0, 8)

print(f"Sequences enumerated: {sequence_count:,}")
print(f"Distinct base glyphs: {len(base_glyphs):,}")
print()

# Glyph size distribution
from collections import Counter
size_dist = Counter(len(g) for g in base_glyphs)
print("Glyph edge-count distribution:")
for k in sorted(size_dist):
    print(f"  {k} edges: {size_dist[k]} glyphs")

# Varied glyphs: each edge can be unidirectional or bidirectional
# A varied glyph is a base glyph + a subset of its edges marked as bidirectional
# Upper bound: sum over all base glyphs of 2^|edges|
varied_upper = sum(2**len(g) for g in base_glyphs)
print(f"\nVaried glyph upper bound (base × 2^edges): {varied_upper:,}")
print("(Many of these will be identical subgraphs — actual count lower)")
