import math
from dataclasses import dataclass

import streamlit as st


@dataclass(frozen=True)
class Clade:
    name: str
    era: str
    depth: int
    traits: tuple[str, ...]
    children: tuple[str, ...]


PHYLETIC_TREE = {
    "LUCA": Clade(
        "LUCA",
        "origin",
        0,
        ("cellular metabolism", "replication", "membrane boundary"),
        ("Bacteria", "Archaea", "Eukarya"),
    ),
    "Bacteria": Clade(
        "Bacteria",
        "ancient radiation",
        1,
        ("peptidoglycan walls", "horizontal transfer", "rapid adaptation"),
        ("Cyanobacteria", "Proteobacteria"),
    ),
    "Archaea": Clade(
        "Archaea",
        "ancient radiation",
        1,
        ("ether lipids", "extreme habitats", "methanogenesis"),
        ("Euryarchaeota", "TACK"),
    ),
    "Eukarya": Clade(
        "Eukarya",
        "symbiotic leap",
        1,
        ("nucleus", "mitochondria", "cytoskeleton"),
        ("Opisthokonta", "Archaeplastida"),
    ),
    "Cyanobacteria": Clade("Cyanobacteria", "oxygenation", 2, ("photosynthesis", "oxygen release"), ()),
    "Proteobacteria": Clade("Proteobacteria", "diversification", 2, ("metabolic breadth", "symbiosis"), ()),
    "Euryarchaeota": Clade("Euryarchaeota", "methane cycle", 2, ("methanogens", "halophiles"), ()),
    "TACK": Clade("TACK", "cell complexity", 2, ("eukaryote-like genes", "membrane remodeling"), ()),
    "Opisthokonta": Clade("Opisthokonta", "multicellularity", 2, ("animals", "fungi"), ()),
    "Archaeplastida": Clade("Archaeplastida", "primary plastids", 2, ("plants", "green algae"), ()),
}


def hexagon_points(cx: float, cy: float, radius: float) -> str:
    """Return SVG point coordinates for a flat-top hexagon."""
    points = []
    for index in range(6):
        angle = math.radians(60 * index)
        points.append(f"{cx + radius * math.cos(angle):.1f},{cy + radius * math.sin(angle):.1f}")
    return " ".join(points)


def axial_to_pixel(q: int, r: int, radius: float) -> tuple[float, float]:
    """Map axial hex coordinates to an SVG canvas."""
    x = radius * 1.5 * q
    y = radius * math.sqrt(3) * (r + q / 2)
    return x, y


def build_hex_layout(selected: str) -> str:
    """Render clades as grouped hexagons around the selected lineage."""
    positions = {
        "LUCA": (0, 0),
        "Bacteria": (-1, 1),
        "Archaea": (0, 1),
        "Eukarya": (1, 0),
        "Cyanobacteria": (-2, 2),
        "Proteobacteria": (-1, 2),
        "Euryarchaeota": (0, 2),
        "TACK": (1, 1),
        "Opisthokonta": (2, 0),
        "Archaeplastida": (2, -1),
    }
    radius = 54
    offset_x, offset_y = 260, 90
    selected_children = set(PHYLETIC_TREE[selected].children)
    nodes = []
    for name, (q, r) in positions.items():
        cx, cy = axial_to_pixel(q, r, radius)
        cx += offset_x
        cy += offset_y
        clade = PHYLETIC_TREE[name]
        is_focus = name == selected
        is_child = name in selected_children
        fill = "#f97316" if is_focus else "#38bdf8" if is_child else "#172554"
        stroke = "#fed7aa" if is_focus else "#bae6fd" if is_child else "#64748b"
        opacity = "1" if is_focus or is_child or clade.depth <= PHYLETIC_TREE[selected].depth else "0.72"
        nodes.append(
            f"""
            <g opacity=\"{opacity}\">
              <polygon points=\"{hexagon_points(cx, cy, radius)}\" fill=\"{fill}\" stroke=\"{stroke}\" stroke-width=\"3\" />
              <text x=\"{cx}\" y=\"{cy - 4}\" text-anchor=\"middle\" fill=\"white\" font-size=\"13\" font-weight=\"700\">{name}</text>
              <text x=\"{cx}\" y=\"{cy + 16}\" text-anchor=\"middle\" fill=\"#dbeafe\" font-size=\"10\">depth {clade.depth}</text>
            </g>
            """
        )
    return f"""
    <svg viewBox=\"0 0 620 420\" width=\"100%\" role=\"img\" aria-label=\"Phyletic tree hexagon grouping map\">
      <rect width=\"620\" height=\"420\" rx=\"24\" fill=\"#020617\" />
      <path d=\"M70 350 C170 250, 250 210, 310 120 S470 80, 550 42\" fill=\"none\" stroke=\"#22d3ee\" stroke-width=\"18\" stroke-linecap=\"round\" opacity=\"0.22\" />
      {''.join(nodes)}
    </svg>
    """


def build_tunnel_layers(selected: str) -> list[dict[str, str]]:
    clade = PHYLETIC_TREE[selected]
    return [
        {
            "layer": "Entry aperture",
            "purpose": "Orient users in the current evolutionary neighborhood before spatial movement begins.",
            "signal": f"Focus clade: {clade.name}",
        },
        {
            "layer": "Trait corridor",
            "purpose": "Translate inherited traits into navigable stations along the tunnel wall.",
            "signal": ", ".join(clade.traits),
        },
        {
            "layer": "Branching chamber",
            "purpose": "Expose child lineages as adjacent hex cells that can become the next tunnel segment.",
            "signal": ", ".join(clade.children) if clade.children else "terminal leaf in this prototype",
        },
    ]


st.set_page_config(page_title="Spatial Phyletic Tunnel", page_icon="🧬", layout="wide")
st.title("🧬 Spatial Tunnel for Phyletic Hexagon Groupings")
st.caption("A first architectural pass for navigating evolutionary relationships as spatial tunnel segments and clustered hex cells.")

with st.sidebar:
    st.header("Navigation controls")
    selected = st.selectbox("Tunnel focus", list(PHYLETIC_TREE.keys()), index=0)
    st.metric("Known clades", len(PHYLETIC_TREE))
    st.metric("Child branches", len(PHYLETIC_TREE[selected].children))

left, right = st.columns([1.35, 1])
with left:
    st.subheader("Hexagon grouping map")
    st.components.v1.html(build_hex_layout(selected), height=460)

with right:
    clade = PHYLETIC_TREE[selected]
    st.subheader(f"{clade.name} tunnel brief")
    st.write(f"**Era marker:** {clade.era}")
    st.write("**Trait anchors:**")
    st.write(" · ".join(clade.traits))
    st.write("**Next branch cells:**")
    st.write(", ".join(clade.children) if clade.children else "No child cells yet in this prototype.")

st.divider()
st.subheader("Spatial tunnel architecture")
for layer in build_tunnel_layers(selected):
    with st.container(border=True):
        st.markdown(f"**{layer['layer']}**")
        st.write(layer["purpose"])
        st.caption(layer["signal"])

st.info(
    "Hex logic: one selected clade becomes the illuminated tunnel cell; its direct descendants become adjacent active cells; "
    "older ancestors and non-selected cousin branches remain visible as lower-emphasis spatial context."
)
