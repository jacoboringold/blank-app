# Kiosk Tunnel

A production-oriented browser kiosk prototype where fictional cannabis products are explored as a living 3D constellation instead of a dispensary list.

## Highlights

- Three.js spatial graph with 360 generated products and thousands of weighted relationships.
- Glass hexagonal 3D product tiles rendered as meshes, not HTML cards.
- Cinematic camera drift, orbit, zoom, search fly-to, hover glow, and selection focus.
- Morphing layouts for brand galaxies, price radius, THC height, terpene clusters, and effect regions.
- Premium dark visual system with fog, particles, neon cyan, purple accents, and gold price treatment.
- Chrome kiosk friendly fullscreen button and minimal DOM updates during animation.

## Run locally

```bash
npm install
npm run dev
```

## Build

```bash
npm run build
```

## Architecture

- `src/App.js` wires the rendering, graph, layout, interaction, and UI systems.
- `src/Products/FakeInventoryGenerator.js` creates fictional brands and products with cannabinoids, terpenes, lineage, pricing, popularity, ratings, image placeholders, and inventory.
- `src/Graph/SimilarityEngine.js` scores product relationships across brand, lineage, terpenes, effect, category, THC, price, popularity, and inventory.
- `src/Graph/LayoutEngine.js` owns morph targets for every supported spatial layout.
- `src/Products/TileMesh.js` creates 3D tile meshes and fiber-optic graph lines.
- `src/Interaction/*` handles hover, selection, and search-driven camera movement.
