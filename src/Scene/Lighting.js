import * as THREE from 'three';
export function createLighting(){ const g=new THREE.Group(); g.add(new THREE.AmbientLight(0x6ab8ff,.5)); const a=new THREE.PointLight(0x00d9ff,70,140); a.position.set(25,35,35); const b=new THREE.PointLight(0x8a4dff,55,150); b.position.set(-45,-10,-30); const c=new THREE.PointLight(0xffc75f,22,80); c.position.set(0,20,0); g.add(a,b,c); return g; }
