import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="NeuoTunnel — Dispensary Kiosk",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
  #MainMenu, header, footer { visibility: hidden; }
  .block-container { padding: 0 !important; margin: 0 !important; max-width: 100% !important; }
  html, body, [data-testid="stAppViewContainer"] { background: #000 !important; }
</style>
""", unsafe_allow_html=True)

TUNNEL_HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>NeuoTunnel</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#000;font-family:'Segoe UI',sans-serif;overflow:hidden;color:#fff;width:100vw;height:100vh}

/* ── LAYOUT ── */
#app{display:grid;grid-template-columns:220px 1fr 260px;grid-template-rows:56px 1fr 110px;width:100vw;height:100vh}

/* ── TOP BAR ── */
#topbar{grid-column:1/-1;background:rgba(0,10,20,.92);border-bottom:1px solid rgba(80,200,255,.25);display:flex;align-items:center;gap:16px;padding:0 18px;z-index:30}
.logo{font-size:17px;font-weight:800;letter-spacing:2px;color:#0ff;text-shadow:0 0 12px #0ff8}
.logo span{color:#7fff7f;font-size:11px;display:block;letter-spacing:3px;font-weight:400}
#topbar .loc{font-size:12px;color:#aaf;margin-left:8px}
#topbar .loc b{color:#fff}
#cat-tabs{display:flex;gap:6px;margin-left:auto}
.cat-btn{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.12);color:#aaa;font-size:11px;padding:5px 13px;border-radius:20px;cursor:pointer;transition:.2s;display:flex;align-items:center;gap:5px}
.cat-btn:hover,.cat-btn.active{background:rgba(0,255,200,.15);border-color:#0fc;color:#0fc;box-shadow:0 0 10px #0fc4}
.cat-btn svg{width:14px;height:14px}

/* ── LEFT SIDEBAR ── */
#sidebar{grid-column:1;grid-row:2/4;background:rgba(0,8,18,.9);border-right:1px solid rgba(80,200,255,.15);padding:14px;overflow-y:auto;z-index:20}
.sb-section{margin-bottom:18px}
.sb-label{font-size:10px;letter-spacing:2px;color:#0fc;text-transform:uppercase;margin-bottom:8px;opacity:.8}
.sb-item{font-size:12px;color:#ccc;padding:5px 8px;border-radius:6px;cursor:pointer;display:flex;align-items:center;gap:7px;transition:.15s}
.sb-item:hover,.sb-item.active{background:rgba(0,255,200,.08);color:#0fc}
.sb-item .dot{width:9px;height:9px;border-radius:50%;flex-shrink:0}
.dot-sativa{background:#7fff7f;box-shadow:0 0 6px #7fff7f}
.dot-indica{background:#a06fff;box-shadow:0 0 6px #a06fff}
.dot-hybrid{background:#0ff;box-shadow:0 0 6px #0ff}
.sb-range{width:100%;accent-color:#0fc;cursor:pointer}
.sb-mini-map{width:100%;height:90px;border:1px solid rgba(0,255,200,.2);border-radius:8px;background:rgba(0,20,40,.6);position:relative;overflow:hidden;margin-top:6px}
.mini-node{position:absolute;border-radius:50%;opacity:.7}
.mini-you{position:absolute;width:8px;height:8px;border-radius:50%;background:#fff;box-shadow:0 0 10px #fff;transform:translate(-50%,-50%);transition:.4s}

/* ── TUNNEL ── */
#tunnel-wrap{grid-column:2;grid-row:2;position:relative;overflow:hidden;background:radial-gradient(ellipse at 50% 50%,#000820 0%,#000 100%)}
#tunnel-canvas{width:100%;height:100%}
/* static rings */
.ring{position:absolute;border-radius:50%;border:1px solid rgba(0,200,255,.1);transform-origin:center center;pointer-events:none}

/* ── PRODUCT CARDS (hex-ish) ── */
.pcard{position:absolute;width:148px;cursor:pointer;transform-origin:center center;transition:filter .2s;user-select:none}
.pcard-inner{background:rgba(0,15,35,.88);border:1.5px solid var(--bc);border-radius:12px;padding:9px 10px;box-shadow:0 0 18px var(--glow),inset 0 0 12px rgba(0,0,0,.5);backdrop-filter:blur(4px);position:relative;overflow:hidden;transition:.25s}
.pcard-inner::before{content:'';position:absolute;inset:0;background:linear-gradient(135deg,var(--glow2) 0%,transparent 60%);opacity:.13;pointer-events:none}
.pcard:hover .pcard-inner,.pcard.selected .pcard-inner{border-color:var(--bc-h);box-shadow:0 0 28px var(--glow-h),inset 0 0 18px rgba(0,0,0,.3)}
.pcard.selected .pcard-inner{box-shadow:0 0 40px var(--glow-h),0 0 80px var(--glow-h2)}
.pcard-type{font-size:8.5px;letter-spacing:2px;text-transform:uppercase;margin-bottom:3px;opacity:.7}
.pcard-name{font-size:12px;font-weight:700;line-height:1.25;margin-bottom:4px}
.pcard-sub{font-size:10px;color:#aaa;margin-bottom:6px}
.pcard-row{display:flex;align-items:center;justify-content:space-between}
.pcard-price{font-size:16px;font-weight:800;color:#fff}
.pcard-thc{font-size:10px;color:#aaa}
.pcard-badge{display:inline-block;font-size:9px;padding:2px 6px;border-radius:10px;background:var(--badge);color:#000;font-weight:700;margin-bottom:4px}
.pcard-img{width:38px;height:38px;object-fit:contain;float:right;margin:-4px -2px 0 6px;filter:drop-shadow(0 0 6px var(--glow))}
.pcard-terpene{font-size:9px;color:#888;margin-top:3px}

/* group label ribbons */
.group-label{position:absolute;pointer-events:none;white-space:nowrap;font-size:11px;letter-spacing:2px;text-transform:uppercase;opacity:0;transition:opacity .4s}
.group-label.visible{opacity:.6}

/* ── BOTTOM CONTROLS ── */
#controls{grid-column:2;grid-row:3;background:rgba(0,8,20,.9);border-top:1px solid rgba(80,200,255,.15);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;z-index:20}
.ctrl-btns{display:flex;align-items:center;gap:22px}
.ctrl-btn{background:rgba(0,255,200,.07);border:1.5px solid rgba(0,255,200,.3);color:#0fc;width:48px;height:48px;border-radius:50%;font-size:18px;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:.2s}
.ctrl-btn:hover{background:rgba(0,255,200,.18);box-shadow:0 0 16px #0fc6}
.ctrl-btn.pause-btn{width:58px;height:58px;font-size:22px}
.price-track{display:flex;align-items:center;gap:10px;font-size:11px;color:#aaa}
.price-track input{width:180px;accent-color:#0fc}
.price-marks{display:flex;justify-content:space-between;width:180px;font-size:10px;color:#555}

/* ── RIGHT PANEL ── */
#detail-panel{grid-column:3;grid-row:2/4;background:rgba(0,8,18,.92);border-left:1px solid rgba(80,200,255,.15);padding:16px;overflow-y:auto;z-index:20}
#detail-panel h3{font-size:14px;letter-spacing:1px;margin-bottom:12px;color:#0fc}
.detail-none{color:#555;font-size:12px;text-align:center;margin-top:40px}
.det-name{font-size:18px;font-weight:800;margin-bottom:4px}
.det-sub{font-size:12px;color:#aaa;margin-bottom:12px}
.det-badge{display:inline-block;padding:3px 10px;border-radius:12px;font-size:11px;font-weight:700;margin-bottom:12px}
.det-row{display:flex;justify-content:space-between;font-size:12px;border-bottom:1px solid rgba(255,255,255,.06);padding:5px 0;color:#ccc}
.det-row b{color:#fff}
.det-price{font-size:28px;font-weight:800;color:#fff;margin:10px 0 4px}
.det-btn{display:block;width:100%;padding:11px;background:linear-gradient(135deg,#0fc,#0af);color:#000;font-weight:800;font-size:13px;border:none;border-radius:8px;cursor:pointer;text-align:center;margin-top:14px;transition:.2s}
.det-btn:hover{opacity:.85;box-shadow:0 0 20px #0fc6}
.det-fav{display:block;width:100%;padding:9px;background:transparent;color:#aaa;font-size:12px;border:1px solid rgba(255,255,255,.12);border-radius:8px;cursor:pointer;text-align:center;margin-top:8px;transition:.2s}
.det-fav:hover{color:#fff;border-color:#fff}
.det-terpenes{margin-top:12px}
.ter-chip{display:inline-block;background:rgba(0,255,200,.08);border:1px solid rgba(0,255,200,.2);border-radius:12px;font-size:10px;padding:3px 9px;margin:3px 3px 0 0;color:#0fc}
.phylo-tree{margin-top:14px;border:1px solid rgba(80,200,255,.15);border-radius:8px;padding:10px;background:rgba(0,10,25,.5)}
.phylo-tree h4{font-size:10px;letter-spacing:2px;text-transform:uppercase;color:#5af;margin-bottom:8px}
.phylo-line{font-size:11px;color:#aaa;line-height:1.8}
.phylo-line span{color:#fff}

/* tunnel path SVG overlay */
#path-overlay{position:absolute;inset:0;pointer-events:none}

/* glow particles */
.particle{position:absolute;border-radius:50%;pointer-events:none;animation:float linear infinite}
@keyframes float{0%{transform:translateY(0) translateX(0);opacity:.8}100%{transform:translateY(-200px) translateX(var(--dx));opacity:0}}

/* price range mini map bottom */
.range-wrap{display:flex;align-items:center;gap:8px;width:100%}
.range-seg{flex:1;height:4px;border-radius:2px;opacity:.4;transition:.3s}
.range-seg.active-seg{opacity:1}

/* you-are-here beacon */
.you-beacon{position:absolute;width:12px;height:12px;border:2px solid #fff;border-radius:50%;transform:translate(-50%,-50%);z-index:10;animation:pulse 1.5s ease-in-out infinite}
@keyframes pulse{0%,100%{box-shadow:0 0 0 0 rgba(255,255,255,.6)}50%{box-shadow:0 0 0 8px rgba(255,255,255,0)}}

/* connection lines between cards */
.conn-svg{position:absolute;inset:0;pointer-events:none;z-index:1}
</style>
</head>
<body>
<div id="app">

<!-- TOP BAR -->
<div id="topbar">
  <div class="logo">NEUOTUNNEL<span>DISPENSARY KIOSK</span></div>
  <div class="loc">Location: <b>Edibles Tunnel</b> &nbsp;·&nbsp; Sorted by: <b id="sort-label">Price Low→High</b></div>
  <div id="cat-tabs">
    <button class="cat-btn" data-cat="flower" onclick="setCategory('flower')">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2C8 2 5 5 5 9c0 5 7 13 7 13s7-8 7-13c0-4-3-7-7-7z"/></svg>
      Flower
    </button>
    <button class="cat-btn" data-cat="vapes" onclick="setCategory('vapes')">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="7" y="3" width="10" height="18" rx="3"/><line x1="12" y1="7" x2="12" y2="11"/></svg>
      Vapes
    </button>
    <button class="cat-btn" data-cat="concentrates" onclick="setCategory('concentrates')">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M8 12c0-2.2 1.8-4 4-4s4 1.8 4 4"/></svg>
      Concentrates
    </button>
    <button class="cat-btn active" data-cat="edibles" onclick="setCategory('edibles')">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2l3 7h7l-5.5 4 2 7L12 16l-6.5 4 2-7L2 9h7z"/></svg>
      Edibles
    </button>
    <button class="cat-btn" data-cat="tinctures" onclick="setCategory('tinctures')">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 3h6v7l3 4v4a2 2 0 01-2 2H8a2 2 0 01-2-2v-4l3-4V3z"/></svg>
      Tinctures
    </button>
    <button class="cat-btn" data-cat="topicals" onclick="setCategory('topicals')">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 7H4a2 2 0 00-2 2v6a2 2 0 002 2h16a2 2 0 002-2V9a2 2 0 00-2-2z"/></svg>
      Topicals
    </button>
  </div>
</div>

<!-- LEFT SIDEBAR -->
<div id="sidebar">
  <div class="sb-section">
    <div class="sb-label">Strain Family</div>
    <div class="sb-item active" onclick="filterStrain('all',this)"><div class="dot" style="background:#555"></div>All Strains</div>
    <div class="sb-item" onclick="filterStrain('sativa',this)"><div class="dot dot-sativa"></div>Sativa</div>
    <div class="sb-item" onclick="filterStrain('indica',this)"><div class="dot dot-indica"></div>Indica</div>
    <div class="sb-item" onclick="filterStrain('hybrid',this)"><div class="dot dot-hybrid"></div>Hybrid</div>
  </div>

  <div class="sb-section">
    <div class="sb-label">Sort Heuristic</div>
    <div class="sb-item active" onclick="setSort('price_asc',this)">↑ Price Low→High</div>
    <div class="sb-item" onclick="setSort('price_desc',this)">↓ Price High→Low</div>
    <div class="sb-item" onclick="setSort('thc_desc',this)">⚡ THC % High</div>
    <div class="sb-item" onclick="setSort('name',this)">A→Z Name</div>
    <div class="sb-item" onclick="setSort('terpene',this)">🌿 Terpene</div>
  </div>

  <div class="sb-section">
    <div class="sb-label">THC Range</div>
    <input type="range" class="sb-range" id="thc-range" min="0" max="100" value="100" oninput="setTHCMax(this.value)"/>
    <div style="font-size:10px;color:#aaa;margin-top:4px">Max: <span id="thc-val">100</span>mg</div>
  </div>

  <div class="sb-section">
    <div class="sb-label">Tunnel Map</div>
    <div class="sb-mini-map" id="mini-map">
      <div class="mini-you" id="mini-you"></div>
    </div>
    <div style="font-size:9px;color:#555;margin-top:5px">● You Are Here &nbsp; → Direction</div>
  </div>

  <div class="sb-section">
    <div class="sb-label">Controls</div>
    <div class="sb-item" style="font-size:10px;color:#666">← / → &nbsp; Navigate tunnel</div>
    <div class="sb-item" style="font-size:10px;color:#666">Click &nbsp;&nbsp; Select product</div>
    <div class="sb-item" style="font-size:10px;color:#666">Space &nbsp; Pause / Resume</div>
  </div>
</div>

<!-- TUNNEL -->
<div id="tunnel-wrap">
  <canvas id="tunnel-canvas"></canvas>
  <svg id="path-overlay"></svg>
  <svg class="conn-svg" id="conn-svg"></svg>
  <!-- cards injected here -->
</div>

<!-- BOTTOM CONTROLS -->
<div id="controls">
  <div class="ctrl-btns">
    <button class="ctrl-btn" onclick="navigate(-3)" title="Back">⏮</button>
    <button class="ctrl-btn" onclick="navigate(-1)" title="Reverse">◀</button>
    <button class="ctrl-btn pause-btn" id="pause-btn" onclick="togglePause()" title="Pause">⏸</button>
    <button class="ctrl-btn" onclick="navigate(1)" title="Forward">▶</button>
    <button class="ctrl-btn" onclick="navigate(3)" title="Skip">⏭</button>
  </div>
  <div class="price-track">
    <span>$0</span>
    <input type="range" id="price-slider" min="0" max="100" value="0" oninput="seekPrice(this.value)" style="width:200px;accent-color:#0fc"/>
    <span>$80+</span>
    <span style="margin-left:10px;color:#0fc;font-weight:700" id="price-here-label">$0–$15</span>
  </div>
</div>

<!-- RIGHT DETAIL PANEL -->
<div id="detail-panel">
  <h3>PRODUCT DETAILS</h3>
  <div id="detail-content"><div class="detail-none">Move through the tunnel<br/>to select a product</div></div>
</div>

</div><!-- /app -->

<script>
// ═══════════════════════════════════════════════════════════
//  DATA — cannabis products with phyletic groupings
// ═══════════════════════════════════════════════════════════
const PRODUCTS = [
  // EDIBLES — Sativa branch
  {id:1,name:'Sour Cherry Gummies',sub:'Sativa / Energizing',type:'edibles',strain:'sativa',price:5,thc:50,cbd:5,terpenes:['Myrcene','Limonene'],brand:'Kiva',effect:'Energize',genetics:'Cherry AK × Sour Diesel',lineage:['AK-47','Sour Diesel'],desc:'Bright citrus-forward gummies with a energizing cerebral onset.',color:'#7fff7f',glow:'rgba(127,255,127,.35)',glow2:'rgba(127,255,127,.6)',badge:'#7fff7f'},
  {id:2,name:'Citrus Blast Gummies',sub:'Sativa / Uplifting',type:'edibles',strain:'sativa',price:13,thc:20,cbd:0,terpenes:['Limonene','Terpinolene'],brand:'Wana',effect:'Uplift',genetics:'Tangie × Jack Herer',lineage:['Tangie','Jack Herer'],desc:'Sun-drenched citrus burst for creative focus.',color:'#ffdf40',glow:'rgba(255,220,60,.35)',glow2:'rgba(255,220,60,.6)',badge:'#ffdf40'},
  {id:3,name:'Sunny Day Chews',sub:'Sativa / Focus',type:'edibles',strain:'sativa',price:14,thc:25,cbd:5,terpenes:['Limonene','Pinene'],brand:'Kanha',effect:'Focus',genetics:'Lemon Haze × Durban',lineage:['Lemon Haze','Durban Poison'],desc:'Clean lemon-pine clarity for daytime productivity.',color:'#ffe066',glow:'rgba(255,224,102,.35)',glow2:'rgba(255,224,102,.6)',badge:'#ffe066'},
  {id:4,name:'Green Apple Gummies',sub:'Sativa / Energize',type:'edibles',strain:'sativa',price:12,thc:20,cbd:0,terpenes:['Limonene','Citrus'],brand:'Nebula',effect:'Energize',genetics:'Apple Fritter × Trainwreck',lineage:['Apple Fritter','Trainwreck'],desc:'Tart green apple pop with a clean, focused high.',color:'#90ee90',glow:'rgba(144,238,144,.35)',glow2:'rgba(144,238,144,.6)',badge:'#90ee90'},
  {id:5,name:'Lemon Spark Dreams',sub:'Sativa / Creative',type:'edibles',strain:'sativa',price:15,thc:30,cbd:0,terpenes:['Terpinolene','Limonene'],brand:'Wyld',effect:'Create',genetics:'Lemon Skunk × Super Silver Haze',lineage:['Lemon Skunk','Super Silver Haze'],desc:'Dreamy lemon haze for artists and wanderers.',color:'#fff176',glow:'rgba(255,241,118,.35)',glow2:'rgba(255,241,118,.6)',badge:'#fff176'},

  // EDIBLES — Hybrid branch
  {id:6,name:'Balanced Fruit Gums',sub:'Hybrid / Balanced',type:'edibles',strain:'hybrid',price:28,thc:100,cbd:100,terpenes:['Myrcene','Caryophyllene'],brand:'Kiva',effect:'Balance',genetics:'Blue Dream × Cannatonic',lineage:['Blue Dream','Cannatonic'],desc:'Perfect 1:1 THC:CBD ratio for calm clarity without sedation.',color:'#00ffff',glow:'rgba(0,255,255,.35)',glow2:'rgba(0,255,255,.6)',badge:'#00ffff'},
  {id:7,name:'Peach Party Gummies',sub:'Hybrid / Social',type:'edibles',strain:'hybrid',price:14,thc:25,cbd:5,terpenes:['Myrcene','Ocimene'],brand:'Wana',effect:'Social',genetics:'Peach Ringz × Gelato',lineage:['Peach Ringz','Gelato 41'],desc:'Juicy peach sweetness with a warm, sociable body feel.',color:'#ffa07a',glow:'rgba(255,160,122,.35)',glow2:'rgba(255,160,122,.6)',badge:'#ffa07a'},
  {id:8,name:'Blackberry Dreams',sub:'Hybrid / Relax',type:'edibles',strain:'hybrid',price:15,thc:25,cbd:5,terpenes:['Caryophyllene','Linalool'],brand:'Kanha',effect:'Relax',genetics:'Blackberry Kush × Blue Dream',lineage:['Blackberry Kush','Blue Dream'],desc:'Rich berry sweetness transitioning to gentle body relaxation.',color:'#9b59b6',glow:'rgba(155,89,182,.35)',glow2:'rgba(155,89,182,.6)',badge:'#da70d6'},
  {id:9,name:'Calm & Chill Drops',sub:'Hybrid / Decompress',type:'edibles',strain:'hybrid',price:22,thc:50,cbd:50,terpenes:['Linalool','Myrcene'],brand:'Wyld',effect:'Relax',genetics:'Purple Punch × ACDC',lineage:['Purple Punch','ACDC'],desc:'Equal THC/CBD blend for winding down without full sedation.',color:'#87ceeb',glow:'rgba(135,206,235,.35)',glow2:'rgba(135,206,235,.6)',badge:'#87ceeb'},
  {id:10,name:'Mango Sunrise Chews',sub:'Hybrid / Euphoric',type:'edibles',strain:'hybrid',price:16,thc:30,cbd:0,terpenes:['Myrcene','Ocimene','Limonene'],brand:'Plus',effect:'Euphoria',genetics:'Mango Kush × Pineapple Express',lineage:['Mango Kush','Pineapple Express'],desc:'Tropical mango burst with an uplifting euphoric wave.',color:'#ffaa00',glow:'rgba(255,170,0,.35)',glow2:'rgba(255,170,0,.6)',badge:'#ffaa00'},

  // EDIBLES — Indica branch
  {id:11,name:'Midnight Berry Gummies',sub:'Indica / Sleep',type:'edibles',strain:'indica',price:32,thc:100,cbd:10,terpenes:['Myrcene','Linalool'],brand:'Kiva',effect:'Sleep',genetics:'Granddaddy Purple × Blueberry',lineage:['Granddaddy Purple','Blueberry'],desc:'Deep berry sedation for full-body sleep support.',color:'#a06fff',glow:'rgba(160,111,255,.35)',glow2:'rgba(160,111,255,.6)',badge:'#a06fff'},
  {id:12,name:'Velvet Sleep Rosin Gummies',sub:'Indica / Sedating',type:'edibles',strain:'indica',price:14,thc:20,cbd:0,terpenes:['Myrcene','Caryophyllene'],brand:'CloudRoot',effect:'Sleep',genetics:'Zkittlez × Kosher Kush',lineage:['Zkittlez','Kosher Kush'],desc:'Velvety smooth sedation from live-rosin infused gummies.',color:'#8b008b',glow:'rgba(139,0,139,.35)',glow2:'rgba(139,0,139,.6)',badge:'#da70d6'},
  {id:13,name:'Sleepy Time Bites',sub:'Indica / Nighttime',type:'edibles',strain:'indica',price:11,thc:20,cbd:0,terpenes:['Linalool','Terpineol'],brand:'Wyld',effect:'Sleep',genetics:'Northern Lights × Lavender',lineage:['Northern Lights','Lavender'],desc:'Classic indica nightcap with floral lavender notes.',color:'#b39ddb',glow:'rgba(179,157,219,.35)',glow2:'rgba(179,157,219,.6)',badge:'#b39ddb'},
  {id:14,name:'Clementine Soother',sub:'Indica-Hybrid / Pain',type:'edibles',strain:'indica',price:75,thc:300,cbd:5,terpenes:['Caryophyllene','Humulene'],brand:'Select',effect:'Relief',genetics:'Clementine × Purple Hindu Kush',lineage:['Clementine','Hindu Kush'],desc:'High-potency relief drops for chronic discomfort.',color:'#ff8c00',glow:'rgba(255,140,0,.35)',glow2:'rgba(255,140,0,.6)',badge:'#ff8c00'},
  {id:15,name:'Midnight Mango Gummies',sub:'Indica / Relaxing',type:'edibles',strain:'indica',price:14,thc:25,cbd:0,terpenes:['Myrcene','Caryophyllene'],brand:'Wana',effect:'Relax',genetics:'Mango × Granddaddy Purple',lineage:['Mango Kush','GDP'],desc:'Exotic mango warmth settling into full body ease.',color:'#c2185b',glow:'rgba(194,24,91,.35)',glow2:'rgba(194,24,91,.6)',badge:'#e91e8c'},

  // FLOWER
  {id:16,name:'Girl Scout Cookies',sub:'Hybrid / Euphoric',type:'flower',strain:'hybrid',price:45,thc:280,cbd:1,terpenes:['Caryophyllene','Limonene','Humulene'],brand:'Cookies',effect:'Euphoria',genetics:'OG Kush × Durban Poison',lineage:['OG Kush','Durban Poison'],desc:'Iconic sweet, earthy hybrid with full-body euphoria.',color:'#00ffff',glow:'rgba(0,255,255,.35)',glow2:'rgba(0,255,255,.6)',badge:'#00ffff'},
  {id:17,name:'Blue Dream',sub:'Hybrid / Balanced',type:'flower',strain:'hybrid',price:38,thc:210,cbd:2,terpenes:['Myrcene','Pinene','Caryophyllene'],brand:'Haze',effect:'Balance',genetics:'Blueberry × Haze',lineage:['Blueberry','Haze'],desc:'Pacific coast staple delivering gentle cerebral invigoration.',color:'#4fc3f7',glow:'rgba(79,195,247,.35)',glow2:'rgba(79,195,247,.6)',badge:'#4fc3f7'},
  {id:18,name:'Gelato 41',sub:'Hybrid / Creative',type:'flower',strain:'hybrid',price:52,thc:250,cbd:1,terpenes:['Limonene','Caryophyllene','Linalool'],brand:'Sherbinski',effect:'Create',genetics:'Sunset Sherbet × Thin Mint GSC',lineage:['Sunset Sherbet','GSC'],desc:'Dessert-like aroma with a potent, long-lasting cerebral rush.',color:'#ce93d8',glow:'rgba(206,147,216,.35)',glow2:'rgba(206,147,216,.6)',badge:'#ce93d8'},
  {id:19,name:'Jack Herer',sub:'Sativa / Focus',type:'flower',strain:'sativa',price:42,thc:220,cbd:0,terpenes:['Terpinolene','Pinene','Ocimene'],brand:'Sensi',effect:'Focus',genetics:'Haze × NL#5 × Shiva Skunk',lineage:['Haze','Northern Lights #5'],desc:'Legend of sativas — piney, spicy uplift for creative minds.',color:'#7fff7f',glow:'rgba(127,255,127,.35)',glow2:'rgba(127,255,127,.6)',badge:'#7fff7f'},
  {id:20,name:'OG Kush',sub:'Indica-Hybrid / Relax',type:'flower',strain:'indica',price:48,thc:260,cbd:1,terpenes:['Myrcene','Limonene','Caryophyllene'],brand:'Top Shelf',effect:'Relax',genetics:'Chemdawg × Hindu Kush',lineage:['Chemdawg','Hindu Kush'],desc:'West Coast classic — earthy, pine, and lemon with heavy body relaxation.',color:'#a06fff',glow:'rgba(160,111,255,.35)',glow2:'rgba(160,111,255,.6)',badge:'#a06fff'},

  // VAPES
  {id:21,name:'Durban Poison Cart',sub:'Sativa / Energize',type:'vapes',strain:'sativa',price:35,thc:800,cbd:5,terpenes:['Terpinolene','Ocimene'],brand:'Bloom',effect:'Energize',genetics:'South African Landrace',lineage:['Durban Poison'],desc:'Pure South African sativa — licorice and anise with a clear electric buzz.',color:'#7fff7f',glow:'rgba(127,255,127,.35)',glow2:'rgba(127,255,127,.6)',badge:'#7fff7f'},
  {id:22,name:'Wedding Cake Pod',sub:'Hybrid / Euphoric',type:'vapes',strain:'hybrid',price:42,thc:850,cbd:2,terpenes:['Caryophyllene','Limonene'],brand:'Select',effect:'Euphoria',genetics:'Triangle Kush × Animal Mints',lineage:['Triangle Kush','Animal Mints'],desc:'Rich vanilla and tangy peppery exhale. Full-body euphoria.',color:'#00ffff',glow:'rgba(0,255,255,.35)',glow2:'rgba(0,255,255,.6)',badge:'#00ffff'},
  {id:23,name:'Northern Lights Cart',sub:'Indica / Sleep',type:'vapes',strain:'indica',price:30,thc:820,cbd:1,terpenes:['Myrcene','Linalool'],brand:'Rove',effect:'Sleep',genetics:'Afghani × Thai',lineage:['Afghani','Thai'],desc:'Musky, sweet indica classic — body melt and restful sleep.',color:'#a06fff',glow:'rgba(160,111,255,.35)',glow2:'rgba(160,111,255,.6)',badge:'#a06fff'},

  // CONCENTRATES
  {id:24,name:'Strawberry Cough Live Resin',sub:'Sativa / Uplift',type:'concentrates',strain:'sativa',price:55,thc:780,cbd:3,terpenes:['Myrcene','Caryophyllene','Limonene'],brand:'Jetty',effect:'Uplift',genetics:'Haze × Strawberry Fields',lineage:['Haze','Strawberry Fields'],desc:'Vivid strawberry essence preserved in live resin extraction.',color:'#ff6b6b',glow:'rgba(255,107,107,.35)',glow2:'rgba(255,107,107,.6)',badge:'#ff6b6b'},
  {id:25,name:'Pineapple OG Badder',sub:'Hybrid / Euphoric',type:'concentrates',strain:'hybrid',price:60,thc:820,cbd:1,terpenes:['Limonene','Myrcene','Pinene'],brand:'Raw Garden',effect:'Euphoria',genetics:'Pineapple × OG Kush',lineage:['Pineapple','OG Kush'],desc:'Tropical pineapple burst in a creamy, workable badder consistency.',color:'#00ffff',glow:'rgba(0,255,255,.35)',glow2:'rgba(0,255,255,.6)',badge:'#00ffff'},

  // TINCTURES
  {id:26,name:'1:1 Rest Formula',sub:'Hybrid / Sleep Support',type:'tinctures',strain:'hybrid',price:40,thc:300,cbd:300,terpenes:['Linalool','Myrcene'],brand:'Papa & Barkley',effect:'Sleep',genetics:'Balanced Extract Blend',lineage:['Broad-spectrum'],desc:'Sublingual drops for nighttime recovery with balanced cannabinoids.',color:'#4fc3f7',glow:'rgba(79,195,247,.35)',glow2:'rgba(79,195,247,.6)',badge:'#4fc3f7'},
  {id:27,name:'Sativa Rise Drops',sub:'Sativa / AM Boost',type:'tinctures',strain:'sativa',price:36,thc:250,cbd:50,terpenes:['Limonene','Pinene'],brand:'Dosist',effect:'Energize',genetics:'High-CBD Sativa Blend',lineage:['ACDC','Jack Herer'],desc:'Morning formula to sharpen focus and elevate mood.',color:'#7fff7f',glow:'rgba(127,255,127,.35)',glow2:'rgba(127,255,127,.6)',badge:'#7fff7f'},

  // TOPICALS
  {id:28,name:'CBD Relief Balm',sub:'CBD / Anti-inflammatory',type:'topicals',strain:'hybrid',price:28,thc:0,cbd:500,terpenes:['Caryophyllene','Menthol'],brand:'Lord Jones',effect:'Relief',genetics:'Hemp Extract',lineage:['Hemp CBD'],desc:'Cooling menthol balm with high-potency CBD for targeted relief.',color:'#80cbc4',glow:'rgba(128,203,196,.35)',glow2:'rgba(128,203,196,.6)',badge:'#80cbc4'},
];

// ═══════════════════════════════════════════════════════════
//  STATE
// ═══════════════════════════════════════════════════════════
let currentCategory = 'edibles';
let currentSort = 'price_asc';
let strainFilter = 'all';
let thcMax = 100000;
let tunnelOffset = 0;   // 0..1 along tunnel
let paused = false;
let selectedId = null;
let autoSpeed = 0;
let animFrame = null;
let lastTime = null;
let cards = [];         // rendered card objects
let visibleProducts = [];

// ═══════════════════════════════════════════════════════════
//  TUNNEL CANVAS — rings + particles
// ═══════════════════════════════════════════════════════════
const canvas = document.getElementById('tunnel-canvas');
const ctx = canvas.getContext('2d');

function resizeCanvas(){
  const wrap = document.getElementById('tunnel-wrap');
  canvas.width = wrap.clientWidth;
  canvas.height = wrap.clientHeight;
}

const particles = [];
function spawnParticle(){
  const p = {
    x: Math.random()*canvas.width,
    y: canvas.height + 10,
    r: Math.random()*2+.5,
    speed: Math.random()*1.2+.4,
    alpha: Math.random()*.7+.3,
    color: Math.random()<.5 ? '#0ff' : (Math.random()<.5 ? '#7fff7f' : '#a06fff'),
    dx: (Math.random()-.5)*30,
    life: 1,
  };
  particles.push(p);
}

function drawTunnel(t){
  ctx.clearRect(0,0,canvas.width,canvas.height);
  const cx = canvas.width/2, cy = canvas.height/2;
  const maxR = Math.max(canvas.width,canvas.height)*.72;

  // draw rings from outside in (perspective illusion)
  for(let i=12; i>=0; i--){
    const frac = i/12;
    const r = maxR * frac;
    const phase = (t*.15 + frac*2.5) % 1;
    const alpha = .06 + frac*.06;
    // alternating ring colors
    const hue = (frac*180 + t*20) % 360;
    ctx.beginPath();
    ctx.arc(cx, cy, r, 0, Math.PI*2);
    ctx.strokeStyle = `hsla(${hue},80%,55%,${alpha})`;
    ctx.lineWidth = frac<.3 ? 1 : 1.5;
    ctx.stroke();
  }

  // horizon glow
  const grad = ctx.createRadialGradient(cx,cy,0,cx,cy,maxR*.25);
  grad.addColorStop(0,'rgba(0,100,255,.07)');
  grad.addColorStop(1,'transparent');
  ctx.fillStyle = grad;
  ctx.fillRect(0,0,canvas.width,canvas.height);

  // rail lines — 4 rails converging at vanishing point
  const rails = [
    [-.55,1],[.55,1],[-.25,.9],[.25,.9]
  ];
  rails.forEach(([xf,yf],i)=>{
    ctx.beginPath();
    ctx.moveTo(cx + xf*canvas.width*.52, cy + yf*canvas.height*.5);
    ctx.lineTo(cx, cy + canvas.height*.08);
    ctx.strokeStyle = `rgba(0,200,255,${i<2?.09:.05})`;
    ctx.lineWidth = i<2?1.5:.8;
    ctx.stroke();
  });

  // particles
  if(Math.random()<.04) spawnParticle();
  for(let i=particles.length-1; i>=0; i--){
    const p = particles[i];
    p.y -= p.speed*(paused?.3:1);
    p.life -= .008*(paused?.3:1);
    if(p.life<=0||p.y<-10){particles.splice(i,1);continue}
    ctx.beginPath();
    ctx.arc(p.x,p.y,p.r,0,Math.PI*2);
    ctx.fillStyle = p.color.replace(')',`,${p.alpha*p.life})`).replace('rgb','rgba');
    // handle hex colors
    ctx.globalAlpha = p.alpha*p.life;
    ctx.fillStyle = p.color;
    ctx.fill();
    ctx.globalAlpha = 1;
  }
}

// ═══════════════════════════════════════════════════════════
//  CARD LAYOUT — phyletic tunnel arrangement
// ═══════════════════════════════════════════════════════════
const wrap = document.getElementById('tunnel-wrap');

// Groups of products arranged on three "branches" (phyletic lanes)
const LANE_CONFIG = {
  sativa: { xBias: -.38, yBias: -.12, label:'Sativa Family', color:'#7fff7f' },
  hybrid: { xBias:  .0,  yBias:  .12, label:'Hybrid Family', color:'#00ffff' },
  indica: { xBias:  .38, yBias: -.12, label:'Indica Family', color:'#a06fff' },
};

function getFilteredProducts(){
  return PRODUCTS
    .filter(p=> p.type === currentCategory)
    .filter(p=> strainFilter==='all' || p.strain===strainFilter)
    .filter(p=> p.thc <= thcMax)
    .sort((a,b)=>{
      if(currentSort==='price_asc') return a.price-b.price;
      if(currentSort==='price_desc') return b.price-a.price;
      if(currentSort==='thc_desc') return b.thc-a.thc;
      if(currentSort==='name') return a.name.localeCompare(b.name);
      if(currentSort==='terpene') return a.terpenes[0].localeCompare(b.terpenes[0]);
      return 0;
    });
}

function buildLayout(){
  // group by strain within current category
  const prods = getFilteredProducts();
  visibleProducts = prods;

  // assign tunnel depth positions
  // products are placed in a 3D perspective tunnel
  // depth goes from near (big) to far (small)
  // we "unfurl" them along a helix-ish path grouped by strain lane
  const strainGroups = {sativa:[],hybrid:[],indica:[]};
  prods.forEach(p=>{ if(strainGroups[p.strain]) strainGroups[p.strain].push(p); });

  const all = [];
  // interleave by strain in tunnel depth order
  const maxLen = Math.max(...Object.values(strainGroups).map(a=>a.length));
  for(let i=0; i<maxLen; i++){
    ['sativa','hybrid','indica'].forEach(s=>{ if(strainGroups[s][i]) all.push({...strainGroups[s][i], tunnelIdx: all.length}); });
  }
  return all;
}

function cardDepth(tunnelIdx, totalCards, offset){
  // offset is 0..totalCards-1 progress through tunnel
  // returns 0(far) .. 1(near)
  let rel = (tunnelIdx - offset + totalCards) % totalCards;
  if(rel > totalCards/2) rel -= totalCards;
  // map rel to depth: 0 = center(nearest), ±N = far
  const halfSpan = Math.min(4, totalCards*.5);
  if(Math.abs(rel) > halfSpan) return null; // hidden
  const depth = 1 - Math.abs(rel)/halfSpan;
  return {depth, rel};
}

function renderCards(){
  // remove old cards
  wrap.querySelectorAll('.pcard').forEach(el=>el.remove());
  wrap.querySelectorAll('.group-label').forEach(el=>el.remove());
  const connSvg = document.getElementById('conn-svg');
  connSvg.innerHTML = '';

  const layout = buildLayout();
  const W = wrap.clientWidth, H = wrap.clientHeight;
  const cx = W/2, cy = H/2;
  cards = [];

  const CARD_NEAR_W = 160;
  const CARD_FAR_W  = 70;
  const NEAR_DIST = 0.82; // depth threshold for "very close"

  layout.forEach((prod, idx)=>{
    const di = cardDepth(idx, layout.length, tunnelOffset % layout.length);
    if(!di) return;
    const {depth, rel} = di;

    const lane = LANE_CONFIG[prod.strain] || LANE_CONFIG.hybrid;

    // 3D perspective: x converges toward center, y same
    const perspX = cx + lane.xBias * W * depth * .65;
    const perspY = cy + lane.yBias * H * depth * .5 + rel * H * .06;

    const scale = CARD_FAR_W/CARD_NEAR_W + depth*(1 - CARD_FAR_W/CARD_NEAR_W);
    const cardW = CARD_NEAR_W * scale;
    const opacity = .3 + depth*.7;
    const zIndex = Math.round(depth*100);

    const card = document.createElement('div');
    card.className = 'pcard' + (selectedId===prod.id?' selected':'');
    card.id = 'card-'+prod.id;
    card.style.cssText = `
      left:${perspX - cardW/2}px;
      top:${perspY - cardW*.7}px;
      width:${cardW}px;
      opacity:${opacity};
      z-index:${zIndex};
      transform:scale(1);
      --bc:${prod.color}66;
      --bc-h:${prod.color};
      --glow:${prod.glow};
      --glow-h:${prod.glow};
      --glow-h2:${prod.glow2};
      --glow2:${prod.glow2};
      --badge:${prod.badge};
    `;

    const thcDisplay = prod.thc > 99 ? (prod.thc/10).toFixed(0)+'mg' : prod.thc+'mg';
    const strainShort = prod.strain.charAt(0).toUpperCase()+prod.strain.slice(1);
    card.innerHTML = `
      <div class="pcard-inner">
        <div class="pcard-type" style="color:${prod.color}">${strainShort} · ${prod.effect}</div>
        <div class="pcard-badge">${prod.effect}</div>
        <div class="pcard-name">${prod.name}</div>
        <div class="pcard-sub">${prod.terpenes[0]}</div>
        <div class="pcard-row">
          <div class="pcard-price">$${prod.price}</div>
          <div class="pcard-thc">${thcDisplay} THC</div>
        </div>
        <div class="pcard-terpene">${prod.terpenes.join(' · ')}</div>
      </div>`;

    card.addEventListener('click',()=>selectProduct(prod.id));
    wrap.appendChild(card);
    cards.push({el:card, prod, x:perspX, y:perspY, depth});

    // draw connection lines between same-strain cards in SVG
    // (handled after all cards placed)
  });

  // draw lines between adjacent same-strain cards
  const prevByStrain = {};
  cards.forEach(c=>{
    const s = c.prod.strain;
    if(prevByStrain[s]){
      const prev = prevByStrain[s];
      // only draw if both visible and depth > .25
      if(c.depth > .25 && prev.depth > .25){
        const line = document.createElementNS('http://www.w3.org/2000/svg','line');
        line.setAttribute('x1', prev.x);
        line.setAttribute('y1', prev.y);
        line.setAttribute('x2', c.x);
        line.setAttribute('y2', c.y);
        const col = LANE_CONFIG[s]?.color || '#fff';
        line.setAttribute('stroke', col);
        line.setAttribute('stroke-width','1');
        line.setAttribute('stroke-opacity', String(Math.min(c.depth, prev.depth)*.3));
        line.setAttribute('stroke-dasharray','4 6');
        connSvg.appendChild(line);
      }
    }
    prevByStrain[s] = c;
  });

  // group labels
  Object.entries(LANE_CONFIG).forEach(([strain,cfg])=>{
    const firstCard = cards.find(c=>c.prod.strain===strain && c.depth>.7);
    if(!firstCard) return;
    const lbl = document.createElement('div');
    lbl.className = 'group-label visible';
    lbl.style.cssText = `left:${firstCard.x-40}px;top:${firstCard.y - 90}px;color:${cfg.color};text-shadow:0 0 10px ${cfg.color};z-index:200`;
    lbl.textContent = cfg.label;
    wrap.appendChild(lbl);
  });

  updateMiniMap(layout);
  updatePriceLabel();
}

// ═══════════════════════════════════════════════════════════
//  MINI MAP
// ═══════════════════════════════════════════════════════════
function updateMiniMap(layout){
  const mm = document.getElementById('mini-map');
  mm.querySelectorAll('.mini-node').forEach(e=>e.remove());
  const W = mm.clientWidth, H = mm.clientHeight;
  const total = layout.length || 1;
  layout.forEach((p,i)=>{
    const lane = LANE_CONFIG[p.strain] || LANE_CONFIG.hybrid;
    const x = (i/total)*W;
    const y = H/2 + lane.xBias*H*.35;
    const node = document.createElement('div');
    node.className = 'mini-node';
    node.style.cssText = `width:5px;height:5px;background:${p.color};left:${x}px;top:${y}px`;
    mm.appendChild(node);
  });
  // you-beacon
  const youX = ((tunnelOffset % total)/total)*W;
  const myou = document.getElementById('mini-you');
  myou.style.left = youX+'px';
  myou.style.top  = H/2+'px';
}

// ═══════════════════════════════════════════════════════════
//  DETAIL PANEL
// ═══════════════════════════════════════════════════════════
function selectProduct(id){
  selectedId = id;
  const p = PRODUCTS.find(x=>x.id===id);
  if(!p) return;

  const strainColor = LANE_CONFIG[p.strain]?.color || '#fff';
  const thcDisplay = p.thc > 99 ? (p.thc/10).toFixed(0)+'mg' : p.thc+'mg';
  const cbdDisplay = p.cbd > 0 ? (p.cbd > 99 ? (p.cbd/10).toFixed(0)+'mg' : p.cbd+'mg') : 'None';

  document.getElementById('detail-content').innerHTML = `
    <div class="det-name">${p.name}</div>
    <div class="det-sub">${p.sub}</div>
    <div class="det-badge" style="background:${strainColor}22;color:${strainColor};border:1px solid ${strainColor}44">${p.strain.charAt(0).toUpperCase()+p.strain.slice(1)} · ${p.effect}</div>
    <div class="det-price">$${p.price}</div>
    <div class="det-row"><span>THC</span><b>${thcDisplay}</b></div>
    <div class="det-row"><span>CBD</span><b>${cbdDisplay}</b></div>
    <div class="det-row"><span>Brand</span><b>${p.brand}</b></div>
    <div class="det-row"><span>Effect</span><b>${p.effect}</b></div>
    <p style="font-size:11px;color:#aaa;margin:10px 0;line-height:1.6">${p.desc}</p>
    <div class="det-terpenes">
      <div style="font-size:10px;letter-spacing:2px;color:#5af;margin-bottom:6px">TERPENES</div>
      ${p.terpenes.map(t=>`<span class="ter-chip">${t}</span>`).join('')}
    </div>
    <div class="phylo-tree">
      <h4>Phyletic Lineage</h4>
      <div class="phylo-line">
        ${p.lineage.map((l,i)=>`<span style="padding-left:${i*12}px">${i>0?'└─ ':''}<span>${l}</span></span><br/>`).join('')}
        └─ <span style="color:${strainColor}">${p.name}</span>
      </div>
    </div>
    <button class="det-btn">Add to Cart</button>
    <button class="det-fav">☆ Add to Favorites</button>
  `;
  renderCards(); // re-render to show selected state
}

// ═══════════════════════════════════════════════════════════
//  NAVIGATION
// ═══════════════════════════════════════════════════════════
function navigate(delta){
  tunnelOffset += delta;
  renderCards();
}

function togglePause(){
  paused = !paused;
  document.getElementById('pause-btn').textContent = paused ? '▶' : '⏸';
}

function seekPrice(val){
  // map slider to tunnel offset based on price ordering
  const prods = getFilteredProducts();
  if(!prods.length) return;
  const idx = Math.round((val/100)*(prods.length-1));
  tunnelOffset = idx;
  renderCards();
}

function updatePriceLabel(){
  const prods = getFilteredProducts();
  if(!prods.length) return;
  const idx = Math.max(0, Math.min(prods.length-1, Math.round(tunnelOffset) % prods.length));
  const p = prods[idx];
  if(p) document.getElementById('price-here-label').textContent = '$'+p.price;
}

// ═══════════════════════════════════════════════════════════
//  FILTERS / SORT
// ═══════════════════════════════════════════════════════════
function setCategory(cat){
  currentCategory = cat;
  tunnelOffset = 0;
  selectedId = null;
  document.getElementById('detail-content').innerHTML = '<div class="detail-none">Move through the tunnel<br/>to select a product</div>';
  document.querySelectorAll('.cat-btn').forEach(b=>b.classList.toggle('active', b.dataset.cat===cat));
  renderCards();
}

function filterStrain(s, el){
  strainFilter = s;
  document.querySelectorAll('#sidebar .sb-item').forEach(x=>x.classList.remove('active'));
  el.classList.add('active');
  renderCards();
}

function setSort(s, el){
  currentSort = s;
  const labels = {price_asc:'Price Low→High',price_desc:'Price High→Low',thc_desc:'THC % High',name:'A→Z Name',terpene:'Terpene'};
  document.getElementById('sort-label').textContent = labels[s];
  // mark active in sidebar
  renderCards();
}

function setTHCMax(val){
  thcMax = parseInt(val)*10; // scale 0-100 to 0-1000mg
  document.getElementById('thc-val').textContent = val;
  renderCards();
}

// ═══════════════════════════════════════════════════════════
//  KEYBOARD
// ═══════════════════════════════════════════════════════════
document.addEventListener('keydown', e=>{
  if(e.key==='ArrowRight'||e.key==='ArrowDown') { navigate(1); e.preventDefault(); }
  if(e.key==='ArrowLeft'||e.key==='ArrowUp')    { navigate(-1); e.preventDefault(); }
  if(e.key===' ') { togglePause(); e.preventDefault(); }
  if(e.key==='Escape') { selectedId=null; renderCards(); }
});

// ═══════════════════════════════════════════════════════════
//  AUTO-SCROLL ANIMATION LOOP
// ═══════════════════════════════════════════════════════════
let tunnelTime = 0;
function loop(ts){
  if(lastTime===null) lastTime=ts;
  const dt = (ts-lastTime)/1000;
  lastTime = ts;
  tunnelTime += dt;

  if(!paused){
    tunnelOffset += dt * 0.35; // gentle auto-scroll speed
    const prods = getFilteredProducts();
    if(prods.length) tunnelOffset = tunnelOffset % prods.length;
    renderCards();
  }

  drawTunnel(tunnelTime);
  animFrame = requestAnimationFrame(loop);
}

// ═══════════════════════════════════════════════════════════
//  INIT
// ═══════════════════════════════════════════════════════════
window.addEventListener('resize',()=>{
  resizeCanvas();
  renderCards();
});

resizeCanvas();
renderCards();
animFrame = requestAnimationFrame(loop);

// Expose for inline handlers
window.setCategory = setCategory;
window.filterStrain = filterStrain;
window.setSort = setSort;
window.setTHCMax = setTHCMax;
window.navigate = navigate;
window.togglePause = togglePause;
window.seekPrice = seekPrice;
</script>
</body>
</html>
"""

components.html(TUNNEL_HTML, height=900, scrolling=False)
