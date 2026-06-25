import * as THREE from 'three';
export class ParticleField { constructor(count){ const g=new THREE.BufferGeometry(), arr=new Float32Array(count*3); for(let i=0;i<count;i++){ arr[i*3]=(Math.random()-.5)*180; arr[i*3+1]=(Math.random()-.5)*100; arr[i*3+2]=(Math.random()-.5)*180;} g.setAttribute('position',new THREE.BufferAttribute(arr,3)); this.points=new THREE.Points(g,new THREE.PointsMaterial({color:0x8defff,size:.18,transparent:true,opacity:.55,depthWrite:false})); }
 update(dt,t){ this.points.rotation.y=t*.015; this.points.rotation.x=Math.sin(t*.08)*.04; }}
