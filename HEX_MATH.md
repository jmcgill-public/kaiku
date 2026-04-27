# Hex Grid Mathematics
### From first principles for someone who knows what a basis vector is

*No softening. Direct to the geometry. Code follows math.*
*Quaternions do not appear in this document.*

---

## Part 1 — Why hexagons

Start with a question: what regular polygon tiles the plane such that
every tile has the maximum number of equidistant neighbors.

Triangles tile. Each triangle has 12 neighbors, but only 3 share an
edge and are equidistant from the center. Squares tile. Four equidistant
neighbors. Hexagons tile. Six equidistant neighbors. No regular polygon
does better while tiling.

Six equidistant neighbors is the whole game. It means threat and
movement radiate symmetrically in six directions. Distance calculations
are clean. There are no diagonal-vs-orthogonal inconsistencies. The
geometry is honest.

On the hex map, Hiljaisuus sits in the center and has six equidistant
routes. You cannot approach it asymmetrically. The Tholian web closes
uniformly. This is not a design choice. It is a consequence of the
geometry.

---

## Part 2 — The coordinate problem

The naive approach: offset coordinates. Row-column indexing with the
rows staggered. Every computer implementation that gets hex grids wrong
starts here.

Offset coordinates work for storage and rendering. They fail for
computation. The distance between two hexes requires a case split on
whether the row is odd or even. Rotation requires case splits. Line of
sight requires case splits. Every algorithm has edge cases that don't
exist in the underlying geometry — they exist because the coordinate
system is fighting the geometry.

There is a better way.

---

## Part 3 — Cube coordinates and the constraint plane

Embed the hex grid in three-dimensional space. Assign three coordinates
(x, y, z) to each hex subject to the constraint:

    x + y + z = 0

This constraint defines a plane through the origin in R³. The hex grid
lives on this plane. Every valid hex position satisfies the constraint.

The six neighbors of (0, 0, 0):

    (1, -1, 0)   (1, 0, -1)   (0, 1, -1)
    (-1, 1, 0)   (-1, 0, 1)   (0, -1, 1)

Verify: each sums to zero. Each is unit distance from the origin in
the L∞ norm (max of absolute values = 1). Each differs from the origin
in exactly two coordinates by ±1, maintaining the constraint. This is
not a coincidence — it is the structure.

The six direction vectors are the generators of the hex grid. Every
hex is reachable from the origin by integer linear combinations of
these vectors, subject to the constraint. This is the lattice.

Why does the constraint clean up the algorithms?

**Distance.** The L1 distance between two hexes a and b in cube
coordinates is:

    |xa - xb| + |ya - yb| + |za - zb|

On the constraint plane, moving from any hex to any neighbor changes
exactly two coordinates by ±1. The third stays fixed. So the L1
distance between any two adjacent hexes is always 2. The hex distance
— the minimum number of steps — is L1 divided by 2:

    hex_distance(a, b) = (|xa - xb| + |ya - yb| + |za - zb|) / 2

This is always an integer. No case splits. No edge cases. The
geometry of the constraint plane makes it so.

Verify with the Hiljaisuus example. Place Hiljaisuus at (0, 0, 0).
Place Usher Reach at (2, -1, -1). Verify the constraint: 2-1-1=0.
Distance: (|2| + |-1| + |-1|) / 2 = 4/2 = 2. Two steps.
No diagonal ambiguity. No case split.

**Rotation.** A 60-degree clockwise rotation in cube coordinates is:

    (x, y, z) → (-z, -x, -y)

This is a cyclic permutation with sign changes. It is a linear
transformation on R³ that preserves the constraint plane (verify:
if x+y+z=0 then -z+(-x)+(-y) = -(x+y+z) = 0). Six applications
return you to the start. The symmetry group of the hex grid is clean
because the coordinate system respects the geometry.

For your purposes: rotating the disruption pattern, rotating faction
threat cones, rotating the player's heading. All clean applications
of this single transform.

**Reflection.** Reflection through the x-axis (the line y = -z):

    (x, y, z) → (x, z, y)

Also a linear transformation preserving the constraint. Mirror the
constellation for asymmetric map variants.

---

## Part 4 — Axial coordinates

Cube coordinates have three values with one degree of freedom removed
by the constraint. Two coordinates suffice. Drop z (recover it as
-x-y when needed). Rename x→q, y→r. These are axial coordinates.

    q = x
    r = y
    s = z = -q - r  (implicit, recover when needed)

Every cube coordinate algorithm works in axial by recovering s on
demand. The storage is two integers. The math reverts to cube when
complexity requires it.

```typescript
interface HexCoord {
  q: number;
  r: number;
}

// Recover cube coordinates when needed
function toCube(h: HexCoord): { x: number; y: number; z: number } {
  return { x: h.q, y: h.r, z: -h.q - h.r };
}

// Distance in axial (via cube)
function hexDistance(a: HexCoord, b: HexCoord): number {
  const dq = a.q - b.q;
  const dr = a.r - b.r;
  return (Math.abs(dq) + Math.abs(dq + dr) + Math.abs(dr)) / 2;
}
```

---

## Part 5 — The linear transform: hex to pixel

The hex grid is a lattice. The pixel plane is R². The transform
from hex to pixel is a linear map — a matrix multiply.

Choose flat-top hexes (the right choice for a space game —
the constellation reads as a network, not a forest path).

The basis vectors in pixel space for flat-top hexes of size s:
- Moving one step in the q direction: (3s/2, s√3/2)
- Moving one step in the r direction: (0, s√3)

The transform matrix M:

    M = s * [ 3/2      0   ]
            [ √3/2    √3   ]

For hex (q, r), the pixel center is:

    [x]   [ 3/2      0  ] [q]
    [y] = [ √3/2    √3  ] [r] * s

This is a non-degenerate linear map. Its inverse exists.

**The inverse transform: pixel to hex.**

    M⁻¹ = (1/s) * [  2/3      0    ]
                  [ -1/3    √3/3   ]

For pixel (x, y), the fractional hex coordinate is:

    q_frac = (2/3 * x) / s
    r_frac = (-1/3 * x + √3/3 * y) / s

This gives you a point in the real-valued hex plane. Round it to
the nearest integer hex using the cube rounding algorithm below.

```typescript
function hexToPixel(h: HexCoord, size: number): { x: number; y: number } {
  return {
    x: size * (3/2 * h.q),
    y: size * (Math.sqrt(3)/2 * h.q + Math.sqrt(3) * h.r)
  };
}

function pixelToHex(x: number, y: number, size: number): HexCoord {
  const q = (2/3 * x) / size;
  const r = (-1/3 * x + Math.sqrt(3)/3 * y) / size;
  return roundHex({ q, r });
}
```

---

## Part 6 — Rounding to the nearest hex

You have fractional cube coordinates (x_f, y_f, z_f). You need
the nearest integer hex. Naive rounding of each component
independently violates the constraint x+y+z=0.

The correct algorithm:

1. Round all three components independently to nearest integer.
2. Compute the rounding errors: dx = |x_f - rx|, dy, dz.
3. Reset the component with the largest error so the constraint
   is satisfied.

```typescript
function roundHex(h: { q: number; r: number }): HexCoord {
  const s = -h.q - h.r; // recover z from fractional axial

  let rq = Math.round(h.q);
  let rr = Math.round(h.r);
  let rs = Math.round(s);

  const dq = Math.abs(rq - h.q);
  const dr = Math.abs(rr - h.r);
  const ds = Math.abs(rs - s);

  // Reset the component with largest error
  if (dq > dr && dq > ds) {
    rq = -rr - rs;
  } else if (dr > ds) {
    rr = -rq - rs;
  }
  // rs not needed in axial output

  return { q: rq, r: rr };
}
```

The constraint is algebraic, not geometric. The rounding algorithm
respects it by construction.

---

## Part 7 — Line drawing: lerp on the constraint plane

To draw a line from hex A to hex B, interpolate linearly through
the real-valued hex plane and round each point.

The path has exactly hexDistance(A, B) + 1 points.

**Linear interpolation in cube coordinates:**

    lerp_cube(a, b, t) = (a.x + (b.x - a.x)*t,
                          a.y + (b.y - a.y)*t,
                          a.z + (b.z - a.z)*t)

For t ∈ {0, 1/N, 2/N, ..., 1} where N = hexDistance(A, B),
round each interpolated point to the nearest hex.

A subtle issue: when the line passes exactly through a hex corner
(equidistant between two hexes), the rounding is ambiguous. Add a
small epsilon to break ties consistently:

    lerp_cube(a, b, t) with a offset by (1e-6, -2e-6, 1e-6)

```typescript
function hexLineDraw(a: HexCoord, b: HexCoord): HexCoord[] {
  const N = hexDistance(a, b);
  if (N === 0) return [a];

  const results: HexCoord[] = [];
  const aCube = toCube(a);
  const bCube = toCube(b);

  // Small nudge for tie-breaking at corners
  const eps = 1e-6;

  for (let i = 0; i <= N; i++) {
    const t = i / N;
    const lerped = {
      q: aCube.x + eps + (bCube.x - aCube.x) * t,
      r: aCube.y - 2*eps + (bCube.y - aCube.y) * t
    };
    results.push(roundHex(lerped));
  }
  return results;
}
```

**Application: line of sight from Hiljaisuus.**
The line from Hiljaisuus to any station tells you exactly which
hexes a route passes through. A disrupted hex on that line blocks
the route. The web doesn't need a separate algorithm — it's
a predicate on the line drawing.

---

## Part 8 — The Tholian web: BFS on a constrained graph

The disruption spreads from Hiljaisuus. Each sequence step it
reaches hexes adjacent to already-disrupted hexes, but only
along established routes. The routes are the adjacency constraint.

This is breadth-first search on a graph where nodes are hexes
and edges are route connections. The web at sequence step N is
all hexes reachable from Hiljaisuus within N steps along routes.

```typescript
function computeDisruption(
  origin: HexCoord,
  sequenceStep: number,
  routeHexes: Set<string>  // serialized coords of hexes on routes
): Set<string> {
  const visited = new Set<string>();
  const queue: Array<{ hex: HexCoord; depth: number }> = [];
  const originKey = serializeHex(origin);

  visited.add(originKey);
  queue.push({ hex: origin, depth: 0 });

  while (queue.length > 0) {
    const { hex, depth } = queue.shift()!;
    if (depth >= sequenceStep) continue;

    for (const neighbor of hexNeighbors(hex)) {
      const key = serializeHex(neighbor);
      if (!visited.has(key) && routeHexes.has(key)) {
        visited.add(key);
        queue.push({ hex: neighbor, depth: depth + 1 });
      }
    }
  }
  return visited;
}
```

The web closes not because of combat or resource expenditure but
because the BFS frontier reaches hexes the player needs. The
player routes around it by finding paths that avoid the visited set.

Route around it or die. The geometry enforces this. Not a rule.
A consequence.

---

## Part 9 — A* pathfinding

The player's ship moves through the constellation. Disrupted hexes
have infinite cost. Undisrupted route hexes have cost proportional
to hehku required for transit. The player wants the minimum-cost path.

A* with hex distance as the admissible heuristic.

The heuristic: straight-line hex distance to the goal, ignoring
obstacles and costs. Admissible because it never overestimates.
The actual cost through disrupted space is infinite; the heuristic
says zero. Underestimate. A* remains optimal.

```typescript
function hexAStar(
  start: HexCoord,
  goal: HexCoord,
  getCost: (hex: HexCoord) => number  // Infinity for disrupted hexes
): HexCoord[] | null {

  const openSet = new MinHeap<{ hex: HexCoord; f: number }>(x => x.f);
  const gScore = new Map<string, number>();
  const cameFrom = new Map<string, HexCoord>();

  const startKey = serializeHex(start);
  gScore.set(startKey, 0);
  openSet.push({ hex: start, f: hexDistance(start, goal) });

  while (!openSet.isEmpty()) {
    const { hex: current } = openSet.pop();
    const currentKey = serializeHex(current);

    if (currentKey === serializeHex(goal)) {
      return reconstructPath(cameFrom, current);
    }

    for (const neighbor of hexNeighbors(current)) {
      const neighborKey = serializeHex(neighbor);
      const cost = getCost(neighbor);
      if (cost === Infinity) continue;

      const tentativeG = (gScore.get(currentKey) ?? Infinity) + cost;
      if (tentativeG < (gScore.get(neighborKey) ?? Infinity)) {
        cameFrom.set(neighborKey, current);
        gScore.set(neighborKey, tentativeG);
        openSet.push({
          hex: neighbor,
          f: tentativeG + hexDistance(neighbor, goal)
        });
      }
    }
  }
  return null; // No path. The web has closed.
}
```

**The chess layer:** the player who sees a path closing three
sequence steps before it closes survives. The player who doesn't
finds hexAStar returning null and the sequence ending. The loss
was in the position before it showed up in the numbers.

---

## Part 10 — The 3D constellation: stacked planes

The 8x8x3 grid. Three constraint planes at depths 0, 1, 2.
Each plane is an independent hex grid. Routes connect hexes
within a plane and between planes at designated crossing points.

Represent the crossing points as edges in the graph with a depth
transition cost. The pathfinding algorithm is unchanged —
A* on a graph where nodes are (HexCoord, depth) pairs.

```typescript
interface HexCoord3D {
  q: number;
  r: number;
  depth: number;  // 0, 1, or 2
}

function neighbors3D(h: HexCoord3D, crossings: CrossingMap): HexCoord3D[] {
  // Six in-plane neighbors
  const inPlane = hexNeighbors({ q: h.q, r: h.r })
    .map(n => ({ ...n, depth: h.depth }));

  // Cross-depth neighbors at designated crossings
  const crossNeighbors = crossings.get(serializeHex3D(h)) ?? [];

  return [...inPlane, ...crossNeighbors];
}
```

The depth layer is where the routes pass through the brane.
The player who only reads the flat constellation is reading
an incomplete map. The void has depth. The routes do too.

---

## Summary: the algorithms and their game roles

| Algorithm | Math basis | Game role |
|-----------|-----------|-----------|
| Cube coordinates | Constraint plane in R³ | Foundation for all others |
| hexDistance | L1 norm on constraint plane | Movement cost, A* heuristic |
| hexToPixel / pixelToHex | Linear transform + inverse | Rendering, hit testing |
| roundHex | Constrained rounding | Pixel-to-hex accuracy |
| hexLineDraw | Lerp + round | Line of sight, route display |
| BFS on routes | Graph search | Tholian web / disruption |
| A* | BFS + admissible heuristic | Ship pathfinding |
| Rotation (60°) | Linear transform on constraint plane | Faction threat cones |

---

## What to build next

Before writing one line of React or game state, build these
as pure TypeScript functions with Vitest tests:

1. `hexDistance` — verify against known cases
2. `hexToPixel` / `pixelToHex` — verify they are true inverses
3. `roundHex` — verify at hex corners (the edge case)
4. `hexLineDraw` — verify the line from Hiljaisuus to Usher Reach
   passes through the right intermediate hexes
5. `computeDisruption` — verify the web closes correctly from
   Hiljaisuus at sequence steps 1, 2, 3
6. `hexAStar` — verify it finds the correct route around the web
   and returns null when the web has closed all paths

When all six pass, the foundation is solid.
Everything downstream can be trusted.

---

*The constraint plane is the void's geometry.*
*The routes are where the geometry allows.*
*Nobody understands why the routes are where they are.*
*The math doesn't answer that question.*
*It only tells you how far apart things are.*

---

## Appendix — What is WebGL

Canvas 2D is a CPU-side drawing API. You call functions.
The CPU executes them. Pixels appear. For a hex constellation
of reasonable size this is fast enough. You don't need WebGL
to ship this game.

WebGL earns its place in three scenarios:

1. The 3D constellation layer — rotating, tilting, navigating
   the depth axis in real space rather than faking it with
   a layer toggle.

2. Visual effects that belong on the GPU — the hehku glow,
   the void's texture, the disruption spreading as a shader
   effect rather than redrawn polygons.

3. Scale — tens of thousands of hexes without frame drops.
   The game doesn't need this. Note it and move on.

If none of those matter yet, skip WebGL. Come back when
Canvas 2D becomes the bottleneck. It probably won't.

### What WebGL actually is

WebGL is a JavaScript binding to OpenGL ES, which is a
subset of OpenGL designed for embedded systems and ported
to the browser. It is a state machine that talks directly
to the GPU. You configure the state, then issue draw calls.
The GPU executes them in parallel across thousands of cores.

The contract between your JavaScript and the GPU is a pair
of programs written in GLSL — the OpenGL Shading Language.
These programs run on the GPU, not the CPU. They are compiled
at runtime. They are fast because the GPU runs thousands of
instances simultaneously.

The two programs:

**Vertex shader** — runs once per vertex. Receives position
data and transforms it. Outputs a position in clip space.

**Fragment shader** — runs once per pixel (fragment). Receives
interpolated data from the vertex shader. Outputs a color.

Between them: rasterization. The GPU takes the triangles your
vertex shader defined, figures out which pixels they cover,
and calls the fragment shader for each one. You don't write
the rasterizer. It's in hardware.

### The coordinate spaces

This is linear algebra. You have seen this before.

**Object space** — coordinates relative to the object's own
origin. A hex polygon centered at (0, 0).

**World space** — coordinates in the game world. The hex at
its position in the constellation.

**Clip space** — what WebGL expects. A cube from (-1,-1,-1)
to (1,1,1). Everything outside this cube is clipped. The
center of the screen is (0,0). Top-right corner is (1,1).

The transform from world space to clip space is a matrix
multiply. For a 2D game with no camera rotation:

```
clip_position = projection_matrix * world_position
```

For a 3D constellation with a camera:

```
clip_position = projection * view * model * object_position
```

These are the Model-View-Projection (MVP) matrices. Each is
a 4×4 matrix operating on homogeneous coordinates — the
standard (x, y, z, w) representation where w=1 for points
and w=0 for directions. You know homogeneous coordinates from
projective geometry. If you don't, they are the thing that
makes translation expressible as a matrix multiply.

The vertex shader receives the object-space position and the
MVP matrix as a uniform (a value constant across a draw call),
multiplies them, and outputs the result as gl_Position.

```glsl
// Vertex shader — GLSL
attribute vec2 a_position;    // per-vertex input (object space)
uniform mat4 u_mvp;           // same for all vertices in this draw

void main() {
  gl_Position = u_mvp * vec4(a_position, 0.0, 1.0);
}
```

### The fragment shader and the void aesthetic

The fragment shader is where the fine arts background earns
its place in the GPU pipeline.

For Canvas 2D, you call `ctx.fillStyle = '#somecolor'` and
the hex is that color. Flat. Immediate. No depth.

For WebGL, the fragment shader receives the position of the
current pixel, the interpolated data from nearby vertices,
any uniforms you've passed from JavaScript, and returns a
color. The color can be computed from anything.

The hehku glow: pass the current hehku flow rate as a uniform.
Compute a color that is dark at low flow and purple at full
flow. Aava sees it directly. The shader renders what Aava sees.

```glsl
// Fragment shader — GLSL
precision mediump float;

uniform float u_hehkuFlow;    // 0.0 (disrupted) to 1.0 (full flow)
uniform float u_time;         // for animation

void main() {
  // Deep void background
  vec3 voidColor = vec3(0.02, 0.01, 0.05);

  // Hehku glow: purple, brighter at higher flow
  vec3 hehkuColor = vec3(0.4, 0.1, 0.8) * u_hehkuFlow;

  // Pulse slowly — the void is not static
  float pulse = 0.9 + 0.1 * sin(u_time * 0.5);

  gl_FragColor = vec4((voidColor + hehkuColor) * pulse, 1.0);
}
```

The disruption spreading from Hiljaisuus: pass the disruption
radius as a uniform. In the fragment shader, compute the
distance from the current pixel to Hiljaisuus in world space.
If within the disruption radius, shift the color toward
something wrong — not enemy-red, not warning-yellow. The color
that means the routes have closed. The player who reads colors
reads the web closing before the numbers show it.

### The state machine

WebGL is a state machine. Before drawing, you set state.
The draw call uses whatever state is currently set. Forgetting
to set state before a draw call is a common failure mode —
the draw uses the previous call's state, silently, and you
get the wrong output with no error.

The setup sequence for drawing a hex:

```typescript
// 1. Bind the shader program
gl.useProgram(hexProgram);

// 2. Bind the vertex buffer (the hex's geometry)
gl.bindBuffer(gl.ARRAY_BUFFER, hexVertexBuffer);

// 3. Set attribute pointers (how to read the buffer)
gl.enableVertexAttribArray(positionAttrib);
gl.vertexAttribPointer(positionAttrib, 2, gl.FLOAT, false, 0, 0);

// 4. Set uniforms (per-draw constants)
gl.uniformMatrix4fv(mvpLocation, false, mvpMatrix);
gl.uniform1f(hehkuFlowLocation, hex.flowRate);

// 5. Draw
gl.drawArrays(gl.TRIANGLES, 0, 6 * 3); // 6 triangles, 3 vertices each
```

Every hex in the constellation is a draw call with different
uniform values. Or you batch them with instanced rendering —
one draw call for all hexes, with per-instance data in a
separate buffer. Instancing is the performance path when
the constellation grows.

### WebGL2

Use WebGL2, not WebGL1. It is universally supported in modern
browsers and adds instanced rendering, transform feedback,
and uniform buffer objects that matter for a complex scene.

```typescript
const gl = canvas.getContext('webgl2');
if (!gl) {
  // Fall back to Canvas 2D
  // Or tell the player their browser is from Tuonela
}
```

### Three.js

Three.js is a WebGL abstraction library. It handles the
boilerplate — the state machine setup, the shader compilation,
the matrix math, the render loop. You work with objects,
cameras, lights, and materials instead of raw draw calls.

For the 3D constellation view it is reasonable. For the 2D
hex map it is overkill. For learning WebGL it is a trap —
it hides the pipeline you need to understand. Learn raw WebGL
first. Then decide if Three.js is worth the abstraction cost.

The decision tree:

```
2D hex map only?
  → Canvas 2D. Done.

3D constellation layer needed?
  → WebGL2 raw if you want to understand the pipeline.
  → Three.js if you want to ship faster and learn later.

Hehku glow / void aesthetic effects on the 2D map?
  → WebGL2 fragment shaders. Canvas 2D cannot do this efficiently.
  → Worth the investment for the visual register this game demands.
```

### What the GPU is doing while Emo records sequence

The CPU runs your game logic. The sequence advances. The
disruption state updates. Emo appends to the log. The faction
AI makes autonomous decisions.

The GPU, simultaneously, is running thousands of fragment
shader instances — one per pixel of the constellation view —
computing the color of each pixel based on the current game
state you've passed as uniforms. The CPU and GPU run in
parallel. The synchronization point is the frame boundary.

The void is being rendered by hardware designed to solve
linear algebra problems in parallel at nanosecond timescales.

Aava would find this unremarkable.

---

*The constraint plane is the void's geometry.*
*The routes are where the geometry allows.*
*Nobody understands why the routes are where they are.*
*The math doesn't answer that question.*
*It only tells you how far apart things are.*

---
