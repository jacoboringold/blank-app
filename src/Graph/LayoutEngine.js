import { brands, effects, terpenes } from '../Products/FakeInventoryGenerator.js';
import * as THREE from 'three';
const modes = ['brand','price','thc','terpenes','effects'];
export class LayoutEngine {
  constructor(products) { this.products = products; this.mode = 'brand'; this.positions = new Map(); this.targets = new Map(); products.forEach((p,i)=>this.positions.set(p.id, this.brandPosition(p,i))); this.retarget(); }
  setMode(mode) { if (modes.includes(mode)) { this.mode = mode; this.retarget(); } }
  retarget() { this.products.forEach((p,i)=>this.targets.set(p.id, this[`${this.mode}Position`](p,i))); }
  update(dt) { for (const p of this.products) this.positions.get(p.id).lerp(this.targets.get(p.id), Math.min(1, dt * 0.9)); }
  get(id) { return this.positions.get(id); }
  brandPosition(p,i) { const bi = brands.indexOf(p.brand), a = bi/brands.length*Math.PI*2, center = new THREE.Vector3(Math.cos(a)*42, Math.sin(bi*1.7)*10, Math.sin(a)*42); const t=i*.53, r=2+(i%30)*.42; return center.add(new THREE.Vector3(Math.cos(t)*r, Math.sin(t*.7)*r*.45, Math.sin(t)*r)); }
  pricePosition(p,i) { const a=i*.55, r=p.price*.72; return new THREE.Vector3(Math.cos(a)*r, (p.THC-24)*.7, Math.sin(a)*r); }
  thcPosition(p,i) { const a=i*.38, r=18+(i%24)*1.2; return new THREE.Vector3(Math.cos(a)*r, (p.THC-26)*2.1, Math.sin(a)*r); }
  terpenesPosition(p,i) { const ti=terpenes.indexOf(p.primaryTerpene), a=ti/terpenes.length*Math.PI*2, c=new THREE.Vector3(Math.cos(a)*48, 0, Math.sin(a)*48); return c.add(new THREE.Vector3(Math.cos(i)*8, Math.sin(i*.9)*10, Math.sin(i*1.3)*8)); }
  effectsPosition(p,i) { const ei=effects.indexOf(p.effect), a=ei/effects.length*Math.PI*2, c=new THREE.Vector3(Math.cos(a)*55, Math.sin(a*2)*9, Math.sin(a)*55); return c.add(new THREE.Vector3(Math.sin(i)*10, Math.cos(i*.4)*8, Math.cos(i)*10)); }
}
