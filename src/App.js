import { Renderer } from './Scene/Renderer.js';
import { CameraController } from './Scene/CameraController.js';
import { createLighting } from './Scene/Lighting.js';
import { ParticleField } from './Scene/Particles.js';
import { generateInventory } from './Products/FakeInventoryGenerator.js';
import { GraphEngine } from './Graph/GraphEngine.js';
import { LayoutEngine } from './Graph/LayoutEngine.js';
import { TileSystem } from './Products/TileMesh.js';
import { HoverController } from './Interaction/HoverController.js';
import { SelectionController } from './Interaction/SelectionController.js';
import { SearchController } from './Interaction/SearchController.js';
import { SearchBar } from './UI/SearchBar.js';
import { Toolbar } from './UI/Toolbar.js';
import { ProductPanel } from './UI/ProductPanel.js';

export class App {
  constructor(root) {
    this.root = root;
    this.products = generateInventory(360);
    this.graph = new GraphEngine(this.products).build();
    this.layout = new LayoutEngine(this.products, this.graph);
    this.renderer = new Renderer(root);
    this.camera = new CameraController(this.renderer.camera, this.renderer.domElement);
    this.tiles = new TileSystem(this.products, this.graph, this.layout);
    this.particles = new ParticleField(1400);
    this.panel = new ProductPanel(root);
    this.toolbar = new Toolbar(root, (mode) => this.layout.setMode(mode));
    this.searchBar = new SearchBar(root);
    this.search = new SearchController(this.products, this.tiles, this.camera, this.searchBar);
    this.hover = new HoverController(this.renderer, this.tiles, this.camera);
    this.selection = new SelectionController(this.renderer, this.tiles, this.camera, this.panel);
  }

  start() {
    this.renderer.scene.add(createLighting(), this.tiles.group, this.particles.points);
    this.renderer.setFog(0x061122, 35, 155);
    this.renderer.onResize();
    this.search.bind();
    this.hover.bind();
    this.selection.bind();
    this.renderer.start((dt, elapsed) => {
      this.layout.update(dt);
      this.tiles.update(dt, elapsed, this.hover.current, this.selection.selected, this.search.matches);
      this.particles.update(dt, elapsed);
      this.camera.update(dt, elapsed, this.selection.selected ? this.tiles.getPosition(this.selection.selected.id) : null);
      this.renderer.render();
    });
  }
}
