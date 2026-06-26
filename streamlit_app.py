import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

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

html = Path(__file__).parent / "kiosk.html"
components.html(html.read_text(), height=900, scrolling=False)
