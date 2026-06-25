export function similarity(a, b) {
  let score = 0;
  if (a.brand === b.brand) score += 2.4;
  if (a.category === b.category) score += 1.2;
  if (a.effect === b.effect) score += 1.5;
  if (a.primaryTerpene === b.primaryTerpene) score += 2.0;
  score += a.secondaryTerpenes.filter(t => b.secondaryTerpenes.includes(t) || t === b.primaryTerpene).length * 0.7;
  score += a.lineage.filter(l => b.lineage.includes(l)).length * 1.2;
  score += Math.max(0, 1 - Math.abs(a.THC - b.THC) / 40) * 0.9;
  score += Math.max(0, 1 - Math.abs(a.price - b.price) / 90) * 0.6;
  score += Math.max(0, 1 - Math.abs(a.popularity - b.popularity) / 100) * 0.4;
  if (a.inventoryQuantity > 0 && b.inventoryQuantity > 0) score += 0.25;
  return score;
}
