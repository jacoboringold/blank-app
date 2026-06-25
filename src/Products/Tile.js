export function tileLabel(product) { return `${product.brand}\n${product.strain}\n${product.category} • $${product.price}\n${product.THC}% THC • ${product.effect}\n${product.primaryTerpene}`; }
export function makeTileTexture(product) {
  const c = document.createElement('canvas'); c.width=512; c.height=512; const x=c.getContext('2d');
  x.clearRect(0,0,512,512); x.fillStyle='rgba(4,16,34,.72)'; x.strokeStyle='rgba(95,230,255,.9)'; x.lineWidth=8;
  x.beginPath(); for (let k=0;k<6;k++){const a=Math.PI/6+k*Math.PI/3; const px=256+220*Math.cos(a), py=256+220*Math.sin(a); k?x.lineTo(px,py):x.moveTo(px,py);} x.closePath(); x.fill(); x.stroke();
  x.fillStyle='#8ff6ff'; x.font='700 30px Inter, sans-serif'; x.textAlign='center'; x.fillText(product.brand,256,150);
  x.fillStyle='white'; x.font='600 34px Inter, sans-serif'; x.fillText(product.strain.slice(0,22),256,202);
  x.fillStyle='#ffd36e'; x.font='700 40px Inter, sans-serif'; x.fillText(`$${product.price}`,256,260);
  x.fillStyle='#caa6ff'; x.font='600 26px Inter, sans-serif'; x.fillText(`${product.category}  •  ${product.THC}% THC`,256,315);
  x.fillStyle='#79ffcf'; x.fillText(`${product.effect} / ${product.primaryTerpene}`,256,365);
  return c;
}
