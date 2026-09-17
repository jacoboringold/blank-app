from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="3D Body Atlas", page_icon="🧍", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
header { visibility: hidden; height: 0; }
.block-container { padding: .6rem .8rem 1rem; max-width: 100%; }
iframe { border-radius: 12px; border: 1px solid #2a3555; }
</style>
""", unsafe_allow_html=True)

st.title("🧍 3D Body Atlas — Head-to-Toe Study Tool")
st.caption(
    "Rotate and zoom the model, click the glowing markers (or the region list) to pull up what to assess, "
    "normal findings, and red flags for each body region — in head-to-toe order. "
    "Switch on **Quiz mode** to test yourself: it names a region and you click it on the model."
)

atlas_html = Path(__file__).parent.joinpath("body_atlas.html").read_text(encoding="utf-8")
components.html(atlas_html, height=860, scrolling=False)

with st.expander("How to use this"):
    st.markdown(
        "- **Study mode** (default): browse regions in the left list or click markers on the body; "
        "each click opens a panel with what to assess, normal findings, and things to watch for.\n"
        "- **Quiz mode**: hides nothing but flips the flow — it asks you to *find* a region, and you click "
        "the correct marker on the model. Your score tracks per session.\n"
        "- **Front / Back** buttons snap the camera to the front or back view; you can also freely drag to rotate.\n"
        "- The category chips above the list filter which regions/markers are shown (e.g. only MSK or only HEENT).\n"
        "- Progress (regions you've opened) is saved in your browser so it persists between visits on the same device."
    )
