const brands = ['Astra Bloom','Velvet Comet','Northstar Nectar','Luna Grove','Prism Valley','Golden Orbit','Moss & Meteor','Blue Helix','Cinder Flora','Aurora Kind','Halo Fern','Nightglass'];
const strains = ['Nebula Haze','Citrus Collider','Moon Milk','Velvet Kush','Pine Nova','Grape Signal','Quartz Dream','Solar Mints','Rain Prism','Ghost Orchard','Amber Drift','Sage Rocket','Plum Halo','Mango Static'];
const categories = ['Flower','Pre-Roll','Vaporizer','Edible','Concentrate','Tincture'];
const effects = ['Calm','Creative','Euphoric','Focused','Sleepy','Social','Uplifted','Balanced'];
const terpenes = ['Limonene','Myrcene','Caryophyllene','Pinene','Linalool','Humulene','Terpinolene','Ocimene'];
const flavors = ['citrus','pine','berry','diesel','cream','pepper','mint','grape','mango','earth'];
function pick(a, i = Math.random() * a.length) { return a[Math.floor(i) % a.length]; }
function hash(n) { const x = Math.sin(n * 999) * 10000; return x - Math.floor(x); }
export function generateInventory(count = 360) {
  return Array.from({ length: count }, (_, i) => {
    const brand = brands[i % brands.length];
    const strain = `${pick(strains, i * 1.7)} ${Math.floor(hash(i) * 98) + 1}`;
    const category = pick(categories, i * 2.3);
    const effect = pick(effects, i * 3.1);
    const primaryTerpene = pick(terpenes, i * 1.31);
    const secondaryTerpenes = [...new Set([pick(terpenes, i + 2), pick(terpenes, i + 5), pick(terpenes, i + 9)])].filter(t => t !== primaryTerpene).slice(0, 2);
    const thcBase = category === 'Concentrate' ? 58 : category === 'Edible' ? 8 : 18;
    const thc = +(thcBase + hash(i + 11) * (category === 'Concentrate' ? 35 : 17)).toFixed(1);
    const cbd = +(hash(i + 19) * 8).toFixed(1);
    return { id: `kt-${String(i+1).padStart(4,'0')}`, brand, strain, category, THC: thc, CBD: cbd, CBG: +(hash(i+23)*3).toFixed(1), CBN: +(hash(i+29)*2).toFixed(1), price: Math.round(12 + hash(i+31)*82), popularity: Math.round(hash(i+37)*100), rating: +(3.7 + hash(i+41)*1.3).toFixed(1), effect, primaryTerpene, secondaryTerpenes, lineage: [pick(strains, i+4), pick(strains, i+8)], flavorNotes: [pick(flavors, i), pick(flavors, i+3), pick(flavors, i+6)], packageImage: 'placeholder://hex-glass', inventoryQuantity: Math.floor(hash(i+47)*80) };
  });
}
export { brands, categories, effects, terpenes };
