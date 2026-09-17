# 🧍 3D Body Atlas

An interactive 3D human body study tool for head-to-toe anatomy/assessment review — built with Streamlit and Three.js.

## What it does

- A stylized, rotatable 3D mannequin with 28 glowing, clickable regions covering a full head-to-toe sweep (general survey → skin → HEENT → neck → chest/heart/lungs → abdomen → back → pelvis → extremities → neuro/reflexes).
- Clicking a marker (or picking it from the sidebar list) opens a study panel: **what to assess**, **normal findings**, and **watch for** (red flags).
- **Quiz mode**: flips the flow — it names a region and you click the correct spot on the model, with a running score.
- Front/back camera presets, free rotate/zoom, category filter chips (General, Skin, Neuro, HEENT, Cardio, Resp, GI, GU, MSK), a region search box, and a studied-region progress tracker saved in the browser.

## Run

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Files

- `streamlit_app.py` — thin Streamlit shell (title, instructions) that embeds the atlas.
- `body_atlas.html` — the self-contained 3D atlas (Three.js scene, region data, quiz logic, UI). Loaded via `streamlit.components.v1.html`, so it also works as a standalone HTML file if opened directly in a browser.

## Customizing the content

All study content lives in the `REGIONS` array near the top of the `<script>` block in `body_atlas.html` — each entry has a 3D position, category, and `assess` / `normal` / `watch` text, so it's easy to edit wording or add/remove regions without touching the 3D code.
