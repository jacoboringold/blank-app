# 🧬 Spatial Phyletic Tunnel

A Streamlit prototype for exploring evolutionary relationships as a spatial tunnel. The app combines two early architectural ideas:

- **Spatial tunnel layers** that describe the current clade as an entry aperture, trait corridor, and branching chamber.
- **Phyletic tree hexagon groupings** that arrange clades in axial hex coordinates and highlight the selected clade plus its direct descendants.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://blank-app-template.streamlit.app/)

## How to run it on your own machine

1. Install the requirements

   ```bash
   pip install -r requirements.txt
   ```

2. Run the app

   ```bash
   streamlit run streamlit_app.py
   ```

## Prototype behavior

Use the sidebar to select a clade. The map will illuminate the selected clade as the active tunnel cell, highlight direct descendants as branch cells, and keep neighboring branches visible as contextual hexes.
