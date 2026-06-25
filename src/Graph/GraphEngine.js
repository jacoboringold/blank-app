import { similarity } from './SimilarityEngine.js';
export class GraphEngine {
  constructor(products) { this.products = products; this.edges = []; this.neighbors = new Map(); }
  build() {
    for (const p of this.products) this.neighbors.set(p.id, []);
    for (let i = 0; i < this.products.length; i++) {
      const ranked = [];
      for (let j = 0; j < this.products.length; j++) if (i !== j) ranked.push({ target: this.products[j], weight: similarity(this.products[i], this.products[j]) });
      ranked.sort((a,b)=>b.weight-a.weight).slice(0, 6).forEach(e => { this.edges.push({ source: this.products[i], target: e.target, weight: e.weight }); this.neighbors.get(this.products[i].id).push(e); });
    }
    return this;
  }
}
