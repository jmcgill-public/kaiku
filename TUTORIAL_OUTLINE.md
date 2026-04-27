# Kaamos — Technical Tutorial Outline
### Stack: TypeScript / React 18 / HTML5 Canvas / Vite

*Written for a veteran developer making a platform transition.
No softening. No installation walkthroughs. Direct to the concepts
that will cost you time if you don't understand them cold.*

---

## Strategic overview

The stack has four distinct layers. Each has a learning curve.
The curves don't compound if you understand where they're separate.

| Layer | Technology | Primary Concern |
|-------|------------|-----------------|
| Game math | TypeScript (pure) | Hex geometry, game state |
| Game rendering | Canvas 2D API | Pixel-accurate hex map |
| UI shell | React 18 | Merchant screen, Emo log, panels |
| Build / DX | Vite + Vitest | Fast iteration, no webpack hell |

The canonical mistake: letting React manage the canvas render loop.
Don't. React owns the UI. Canvas owns the map. They coexist.
They don't merge.

---

## Milestone 1 — TypeScript for Java veterans
**Effort: 4-6 hours**
**Strategy: contrasts, not basics**

You don't need "what is a type." You need to know where TypeScript
diverges from Java in ways that will cost you.

### What matters

**Structural typing, not nominal typing.**
Java: two classes are compatible if one extends the other.
TypeScript: two types are compatible if their shapes match.
A `VoidShip` and a `StationVessel` with identical fields are
interchangeable. This is not a bug. It's the whole philosophy.

```typescript
// These are compatible. TypeScript doesn't care they have different names.
interface HehkuRoute {
  origin: StationId;
  destination: StationId;
  flowRate: number;
}

interface CorridorLink {
  origin: StationId;
  destination: StationId;
  flowRate: number;
}
```

**Union types replace inheritance hierarchies.**
Java instinct: model the three types of people with a class hierarchy.
TypeScript instinct: model them with a discriminated union.

```typescript
type PersonType = 'worldborn' | 'stationborn' | 'voidborn';

interface WorldbornCreature {
  kind: 'worldborn';
  homeWorld: WorldId;
  lifespanRemaining: number; // counts down
}

interface StationbornCreature {
  kind: 'stationborn';
  homeStation: StationId;
  voidExposure: number; // affects aging rate
}

interface VoidbornCreature {
  kind: 'voidborn';
  sequenceNumber: number; // no timestamp. sequence only.
  // no lifespan field. not applicable.
}

type Creature = WorldbornCreature | StationbornCreature | VoidbornCreature;
```

Type narrowing via the discriminant field replaces instanceof checks.
The compiler enforces exhaustiveness. Miss a case and it tells you.

**Interfaces vs types.**
Use `interface` for shapes that might be extended or implemented.
Use `type` for unions, intersections, and aliases.
In practice the distinction matters less than the Java developer expects
and more than the JavaScript developer realizes.

**Generics behave like Java generics with less ceremony.**
No `<T extends Comparable<T>>` boilerplate. Constraints exist but
are lighter. The game state container will need generics.
Cross that bridge when you build it.

**Key traps for Java developers:**
- `any` is a trap. Use `unknown` when you don't know the type.
  Then narrow it. Never use `any` in game state code.
- Enums in TypeScript are weird. Use string literal unions instead.
  `'worldborn' | 'stationborn' | 'voidborn'` beats `enum PersonType`.
- `undefined` is not `null` is not absence. TypeScript has both.
  Decide on a convention and hold it. Game state: prefer `undefined`
  for optional fields, never `null`.

**Example to build:**
Model the full `Creature` type hierarchy for the Expanse.
Model a `HehkuFlow` type that represents current flow on a route
with a `disrupted` field that changes the shape of the type.
Write a function that accepts a `Creature` and returns their
relationship to sequence — worldborn counts time, stationborn
counts slowly, voidborn returns `undefined`. Make the compiler
enforce that you've handled all three cases.

---

## Milestone 2 — Hex grid mathematics
**Effort: 6-10 hours**
**Strategy: get the coordinate system right before writing one
line of rendering code. Wrong coordinates poison everything downstream.**

### The reference
Amit Patel's Red Blob Games hex grid guide.
`redblobgames.com/grids/hexagons/`
Read all of it. Not skimming. Read it. The guide is the trigonometry
published in the manual. Invasion Orion approach.

### What matters

**Axial coordinates, not offset coordinates.**
Offset feels natural coming from a square grid. It's wrong.
The moment you need distance, line of sight, or the Tholian web
closing algorithm, offset coordinates become a liability.

Axial coordinates: two axes (q, r), third implicit (s = -q-r).
Every hex operation becomes clean arithmetic.

```typescript
interface HexCoord {
  q: number;
  r: number;
}

// Distance between two hexes. Clean. No edge cases.
function hexDistance(a: HexCoord, b: HexCoord): number {
  return (
    Math.abs(a.q - b.q) +
    Math.abs(a.q + a.r - b.q - b.r) +
    Math.abs(a.r - b.r)
  ) / 2;
}

// The six neighbors of any hex. Always six. No edge cases.
const HEX_DIRECTIONS: HexCoord[] = [
  { q: 1, r: 0 }, { q: 1, r: -1 }, { q: 0, r: -1 },
  { q: -1, r: 0 }, { q: -1, r: 1 }, { q: 0, r: 1 }
];

function hexNeighbors(hex: HexCoord): HexCoord[] {
  return HEX_DIRECTIONS.map(d => ({ q: hex.q + d.q, r: hex.r + d.r }));
}
```

**Hex to pixel and pixel to hex.**
These two transforms are where most implementations go wrong.
The math is in the Red Blob guide. The key: decide on flat-top
or pointy-top hexes early and hold it everywhere.

For a space game: flat-top. The constellation reads better.
The routes look like routes, not a path through a forest.

```typescript
interface Point {
  x: number;
  y: number;
}

// Flat-top hex to pixel center
function hexToPixel(hex: HexCoord, size: number): Point {
  return {
    x: size * (3/2 * hex.q),
    y: size * (Math.sqrt(3)/2 * hex.q + Math.sqrt(3) * hex.r)
  };
}
```

**The Hiljaisuus web mechanic.**
The web closing is a flood fill from the disruption origin,
constrained by route adjacency. Each sequence step the disruption
spreads to adjacent route hexes. The player watches the reachable
constellation shrink.

```typescript
function getDisruptedHexes(
  origin: HexCoord,
  sequenceStep: number,
  routes: Set<string> // serialized HexCoords
): Set<string> {
  // BFS outward from origin, constrained to route hexes only
  // Returns all hexes reachable within sequenceStep steps
  // This is your Tholian web
}
```

**Line of sight.**
The hex raycast. Required for the tactical layer.
Red Blob guide has the algorithm. Implement it once. Test it.
Never rewrite it.

**Pathfinding.**
A* on a hex grid. The heuristic is hex distance. Otherwise standard.
Required for autonomous station routing during disruption.

**Example to build:**
A flat hex grid rendered in plain HTML canvas, no React yet.
Click a hex, highlight its neighbors. Click two hexes, draw the
line of sight between them. Click a third, show the shortest path.
All three operations using axial coordinates.
Name the hexes after stations: Tuonela, Manala, Ikävä, Usher Reach,
Diotima. The constellation is already there. You're just rendering it.

---

## Milestone 3 — Canvas 2D API
**Effort: 4-6 hours for the map layer**
**Strategy: the render loop first, then hex rendering, then interaction**

### What matters

**The render loop.**
`requestAnimationFrame` is your game loop. Not `setInterval`.
Not React's render cycle. `requestAnimationFrame`.

```typescript
class ConstellationRenderer {
  private canvas: HTMLCanvasElement;
  private ctx: CanvasRenderingContext2D;
  private animFrameId: number = 0;

  constructor(canvas: HTMLCanvasElement) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d')!;
  }

  start(): void {
    const loop = (timestamp: number) => {
      this.render(timestamp);
      this.animFrameId = requestAnimationFrame(loop);
    };
    this.animFrameId = requestAnimationFrame(loop);
  }

  stop(): void {
    cancelAnimationFrame(this.animFrameId);
  }

  private render(timestamp: number): void {
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    // draw constellation
    // draw hehku flow
    // draw disruption pattern
    // draw faction positions
  }
}
```

**Hit testing.**
Mouse click to hex coordinate. The inverse of hexToPixel.
The Red Blob guide has this. It's not obvious. Get it right once.

**The void aesthetic.**
Canvas gives you full control. The constellation isn't a bright
tactical display on a starship bridge. It's something older.

Dark background. The routes as faint lines, brighter where hehku
flows strongly. The disruption spreading from Hiljaisuus in a color
that Aava would recognize. Stations as nodes with different visual
weight depending on their dependency on the disrupted routes.

The player who reads the brightness of the routes reads the
hehku flow without looking at a number.

**Retina / HiDPI.**
Canvas has a devicePixelRatio problem. Address it at setup or
your map looks blurry on every modern display.

```typescript
function setupHiDPI(canvas: HTMLCanvasElement, width: number, height: number): void {
  const dpr = window.devicePixelRatio || 1;
  canvas.width = width * dpr;
  canvas.height = height * dpr;
  canvas.style.width = `${width}px`;
  canvas.style.height = `${height}px`;
  canvas.getContext('2d')!.scale(dpr, dpr);
}
```

**Example to build:**
Render the full Helka Expanse constellation. Five stations.
Routes as lines with opacity proportional to hehku flow rate.
Hiljaisuus as a special hex in the center. Click a station,
display its name and current hehku reserve. Click Hiljaisuus,
begin the disruption animation — the web starting to close.

---

## Milestone 4 — React 18 for the UI shell
**Effort: 8-12 hours to React rockstar fundamentals**
**Strategy: hooks are the whole game. Master hooks and the rest follows.**

### What matters

**React is not a templating engine.**
Java developer instinct: React is JSP with better syntax.
Wrong frame. React is a state synchronization system.
The UI is a function of state. Change the state, the UI updates.
You don't manipulate the DOM. You change the state.

**The hooks that matter for this game:**

`useState` — local component state. The merchant panel's open/closed
state. The currently selected hex. Fine-grained, component-local.

`useReducer` — complex state with multiple sub-values that change
together. The game state. The constellation. The sequence log.
Use a reducer when the next state depends on the previous state
in non-trivial ways.

```typescript
type GameAction =
  | { type: 'ADVANCE_SEQUENCE' }
  | { type: 'DISRUPT_ROUTE'; payload: HexCoord }
  | { type: 'VISIT_SELLI'; payload: { item: TradeItem } }
  | { type: 'SHIP_MOVES'; payload: { destination: HexCoord } };

function gameReducer(state: GameState, action: GameAction): GameState {
  switch (action.type) {
    case 'ADVANCE_SEQUENCE':
      return {
        ...state,
        sequenceNumber: state.sequenceNumber + 1,
        // Emo records this. sequence not time.
        emoLog: [...state.emoLog, `Sequence ${state.sequenceNumber + 1}.`]
      };
    case 'DISRUPT_ROUTE':
      // Tholian web spreads one hex
      return applyDisruption(state, action.payload);
    // etc.
  }
}
```

`useEffect` — side effects. Initializing the canvas renderer.
Subscribing to resize events. Anything that reaches outside React.
The dependency array is not optional. Understand it completely.
Stale closures will cost you days.

`useRef` — mutable values that don't trigger re-renders. The canvas
element reference. The renderer instance. Animation frame IDs.
Anything the render loop needs to touch without React knowing.

`useCallback` and `useMemo` — performance. Don't reach for these
first. Reach for them when profiling tells you to.

**The canvas pattern in React:**

```typescript
const ConstellationMap: React.FC<{ gameState: GameState }> = ({ gameState }) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const rendererRef = useRef<ConstellationRenderer | null>(null);

  // Initialize renderer once
  useEffect(() => {
    if (!canvasRef.current) return;
    rendererRef.current = new ConstellationRenderer(canvasRef.current);
    rendererRef.current.start();
    return () => rendererRef.current?.stop();
  }, []); // empty deps: run once on mount

  // Update renderer when game state changes
  useEffect(() => {
    rendererRef.current?.updateState(gameState);
  }, [gameState]);

  return <canvas ref={canvasRef} />;
};
```

React does not touch the canvas internals.
The renderer does not touch React state.
The boundary is the `updateState` call.

**The merchant screen — Selli's component:**

Selli's screen is a separate component with its own state.
What Selli offers depends on the game state passed in as props.
What the player does in Selli's screen dispatches actions to the
game reducer. Selli doesn't know about the constellation.
The constellation doesn't know about Selli.

This is the separate-program philosophy in component architecture.

**Emo's log:**

A scrolling sequence log. Each entry is flat, precise, complete.
No timestamps. Sequence numbers only.

```typescript
const EmoLog: React.FC<{ entries: EmoEntry[] }> = ({ entries }) => (
  <div className="emo-log">
    {entries.map(entry => (
      <div key={entry.sequenceNumber} className="emo-entry">
        <span className="seq">{entry.sequenceNumber}</span>
        <span className="data">{entry.text}</span>
      </div>
    ))}
  </div>
);
```

Emo never uses nicknames. Never elides data. The log component
enforces this by design — it renders what it's given, formatted
the same way every time.

**Example to build:**
Full UI shell. Canvas map component center. Emo log right panel.
Merchant screen as a modal that overlays when the player reaches
Usher Reach. Faction status left panel. All wired to a single
game state via useReducer. Dispatch an action from the merchant
screen and watch it propagate to the constellation map.

---

## Milestone 5 — Game state architecture
**Effort: 8-12 hours, ongoing**
**Strategy: model the world before writing game logic**

### The state shape

```typescript
interface GameState {
  // The constellation
  constellation: Map<string, HexCell>; // serialized HexCoord -> cell
  routes: Route[];
  disruption: DisruptionState;

  // The player
  ship: Ship;
  sequenceNumber: number;
  milestones: MilestoneState;

  // Factions
  factions: Map<FactionId, FactionState>;

  // Emo's record
  emoLog: EmoEntry[];

  // Selli's memory
  selliMemory: SelliMemory;
}

interface DisruptionState {
  origin: HexCoord; // Hiljaisuus
  affectedHexes: Set<string>;
  sequenceStep: number; // how many steps since disruption began
}

interface Ship {
  position: HexCoord;
  hehkuReserve: number;
  crew: Creature[];
  equipment: Equipment[];
  experienceLog: ExperienceEntry[]; // Fantasy General persistence
}

interface MilestoneState {
  completed: Set<MilestoneId>;
  available: Set<MilestoneId>; // derived from completed
  // Not exposed to player. Emo has this. Nobody has asked.
}
```

**The sequence milestone system:**

Milestones are preconditions, not objectives. The available set
is derived from the completed set by a pure function. The player
never sees the milestone system directly. They see its consequences
in what becomes possible.

```typescript
function deriveAvailableMilestones(
  completed: Set<MilestoneId>,
  state: GameState
): Set<MilestoneId> {
  // Each milestone has a predicate
  // A milestone becomes available when its predicate is satisfied
  // The predicate checks completed milestones and game state
  // This is the sequence. Emo has it. Nobody has asked.
}
```

**Example to build:**
Full TypeScript model of the Helka Expanse at game start.
Five stations, their routes, initial hehku flow rates.
The player's ship at the world they started on.
Hiljaisuus at the center of the constellation, undisrupted.
Three factions with starting positions and policy settings.
The first three milestones with their preconditions.
A test suite (Vitest) that verifies the disruption spreads
correctly from Hiljaisuus and the milestone system responds.

---

## Milestone 6 — Build tooling
**Effort: 2-4 hours**
**Strategy: Vite, not webpack. Don't argue with this.**

Vite. Not Create React App (deprecated). Not webpack (correct but
slow and configuration-heavy). Vite.

```bash
npm create vite@latest kaamos -- --template react-ts
cd kaamos
npm install
npm run dev
```

That's it. Hot module replacement out of the box. TypeScript out
of the box. React out of the box. Build in milliseconds not minutes.

**Vitest for testing.**
Same config as Vite. Test the hex math. Test the game reducer.
Test the milestone system. The rendering doesn't need unit tests.
The game logic does.

**Project structure:**
```
src/
  hex/          # coordinate math, pure functions, no UI
  game/         # state, reducer, milestone system
  render/       # canvas renderer, no React
  components/   # React components, no game logic
  types/        # shared TypeScript types
```

The separation is enforced by the directory structure.
`hex/` doesn't import from `components/`.
`render/` doesn't import from `game/`.
The boundaries are the architecture.

---

## Milestone 7 — The depth layer (3D constellation)
**Effort: 12-20 hours if you go WebGL**
**Strategy: fake it with layer toggling first**

The 8x8x3 grid from the zine. Three constellation layers.
Routes that pass through depth.

**The pragmatic approach:**
Three separate 2D hex grids. A layer selector in the UI.
The player toggles between them. Routes that connect layers
are rendered as special indicators on both layers.

This is honest to the design intent — the player is reading
three maps that reference each other — without requiring WebGL.
Build this first. It's playable.

**The ambitious approach:**
WebGL with Three.js or raw WebGL. The three layers rendered
in 3D space, the player rotating the view. Technically impressive.
A significant time investment before you've proven the game is fun.

Build the layer toggle. Prove the game. Then decide if the 3D
view earns the investment.

---

## The tutorial sequence

Build in this order:

1. TypeScript types for the game world. No rendering. No React.
   Just the model. Get the types right. Everything downstream
   depends on them.

2. Hex math in isolation. Pure TypeScript functions. Full test
   coverage. This is the foundation. It has to be solid.

3. Canvas rendering of the constellation. No React yet. Just
   the map, the routes, the stations. Get the aesthetics right.
   This is where the fine arts background earns its place.

4. React shell around the canvas. Wire the components. Build
   Emo's log. Build Selli's merchant screen. Get the architecture
   clean.

5. Game state and reducer. The sequence milestone system. The
   disruption mechanic. The Tholian web closing.

6. The player ship. Movement. Hehku consumption. The first death.

7. Factions. Autonomous station behavior. Policy and consequence.

8. The depth layer, when the first seven are solid.

Each milestone produces something playable or testable.
Nothing decorative ships before the foundation is proven.

---

*The butterknife is in your inventory.*
*The constellation is waiting.*
*The void does what it does.*

---
