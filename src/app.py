import os

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from pyvis.network import Network

from config import PROCESSED_DATA_PATH

# Page setup
st.set_page_config(page_title="News Network Analysis", layout="wide")
st.title("Network Analysis: Chilean News Ecosystem")
st.markdown(
    "**Interactive visualization of entities mentioned together in the press.**"
)


@st.cache_data
def load_data():
    """Loads pre-computed graph data."""
    if not os.path.exists(PROCESSED_DATA_PATH):
        return None
    return pd.read_csv(PROCESSED_DATA_PATH)


def render_graph(df, min_weight, max_edges):
    """Builds and renders the PyVis network."""

    # Filter by weight (strength of connection)
    df_filtered = df[df["weight"] >= min_weight]

    # Sort by weight and limit edges for performance
    df_filtered = df_filtered.sort_values(by="weight", ascending=False).head(max_edges)

    # Calculate node importance (Degree Centrality proxy)
    # Sum of weights for sources and targets
    weight_src = df_filtered.groupby("source")["weight"].sum()
    weight_tgt = df_filtered.groupby("target")["weight"].sum()
    total_weight = weight_src.add(weight_tgt, fill_value=0)
    node_sizes = total_weight.to_dict()

    # Initialize PyVis network
    net = Network(
        height="600px",
        width="100%",
        bgcolor="#1E1E1E",
        font_color="white",
        cdn_resources="in_line",
    )
    net.force_atlas_2based(
        gravity=-50, central_gravity=0.01, spring_length=100, overlap=0
    )

    # Add nodes and edges
    for _, row in df_filtered.iterrows():
        src, dst, w = row["source"], row["target"], row["weight"]

        # Default size if missing
        size_src = node_sizes.get(src, 5)
        size_dst = node_sizes.get(dst, 5)

        net.add_node(src, title=src, value=size_src, color="#97C2FC")
        net.add_node(dst, title=dst, value=size_dst, color="#FFFF00")
        net.add_edge(src, dst, value=w, title=f"Co-occurrences: {w}", color="#555555")

    # Save to temporary HTML and read back
    tmp_path = "/tmp/graph.html"
    net.save_graph(tmp_path)

    with open(tmp_path, "r", encoding="utf-8") as f:
        return f.read()


# --- Main App Logic ---

df = load_data()

if df is None:
    st.error("Data file not found. Please run processor.py first.")
else:
    # Sidebar Controls
    st.sidebar.header("Graph Controls")
    min_weight = st.sidebar.slider("Minimum Connection Strength", 1, 20, 2)
    max_edges = st.sidebar.slider("Max Connections to Show", 50, 1000, 200)

    # Search functionality
    search_query = st.sidebar.text_input("Search Entity", "")
    if search_query:
        df = df[
            df["source"].str.contains(search_query, case=False)
            | df["target"].str.contains(search_query, case=False)
        ]

    # Render
    html_data = render_graph(df, min_weight, max_edges)
    components.html(html_data, height=610, scrolling=False)

    st.info(f"Visualizing top {len(df)} relationships.")
