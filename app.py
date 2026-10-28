"""Streamlit frontend for the Smart Campus Navigation System."""
from pathlib import Path
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from campus_navigation import CampusMap, SearchAlgorithms, dijkstra_distance

ROOT = Path(__file__).resolve().parent

st.set_page_config(
    page_title="Smart Campus Navigation",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
.main .block-container {padding-top: 1.6rem; padding-bottom: 2rem; max-width: 1400px;}
.hero {padding: 1.25rem 1.5rem; border-radius: 16px; background: linear-gradient(120deg,#10243a,#245b69); color: white; margin-bottom: 1rem;}
.hero h1 {color: white; margin-bottom: .25rem;}
.hero p {color: #dceaf0; margin-bottom: 0;}
.small-note {color: #64748b; font-size: .9rem;}
</style>
<div class="hero">
  <h1>Smart Campus Navigation</h1>
  <p>AI search in action — compare BFS, DFS, and A* across university campus networks.</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("Plan your route")
    dataset_option = st.selectbox(
        "Campus Map Dataset",
        ["Standard Campus (10 Locations)", "Extended University Campus (16 Locations)"],
        index=0,
    )
    dataset_file = "campus_map.json" if "Standard" in dataset_option else "campus_map_extended.json"
    CAMPUS = CampusMap.from_json(ROOT / "data" / dataset_file)
    SEARCH = SearchAlgorithms(CAMPUS)

    locations = list(CAMPUS.graph.keys())
    start = st.selectbox("Starting location", locations, index=0)
    goal_options = [p for p in locations if p != start]
    goal = st.selectbox("Destination", goal_options, index=min(4, len(goal_options) - 1))
    show_all = st.toggle("Show all three routes", value=True)
    st.divider()
    st.caption(f"Active Map: {dataset_option}")
    st.caption("Distances are calibrated walking paths in metres.")

results = {
    "BFS": SEARCH.bfs(start, goal),
    "DFS": SEARCH.dfs(start, goal),
    "A*": SEARCH.astar(start, goal),
}
dijkstra_best = dijkstra_distance(CAMPUS, start, goal)
astar_distance = results["A*"]["distance"] if results["A*"] else float("inf")

tabs = st.tabs(["Route planner", "Algorithm comparison", "About the project"])

with tabs[0]:
    st.subheader(f"{start}  →  {goal}")
    astar = results["A*"]
    if astar:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("A* route distance", f"{astar['distance']:.1f} m")
        c2.metric("Stops / edges", astar["edges"])
        c3.metric("Nodes expanded", astar["nodes_expanded"])
        c4.metric("Execution time", f"{astar['time_ms']:.3f} ms")
        st.success("Recommended route: " + "  →  ".join(astar["path"]))
    else:
        st.error("No route found for this pair.")

    fig, ax = plt.subplots(figsize=(12, 7))
    seen = set()
    for a, neighbors in CAMPUS.graph.items():
        for b, dist in neighbors.items():
            edge = tuple(sorted((a, b)))
            if edge in seen:
                continue
            seen.add(edge)
            x1, y1 = CAMPUS.locations[a]
            x2, y2 = CAMPUS.locations[b]
            ax.plot([x1, x2], [y1, y2], color="#cbd5e1", linewidth=2, zorder=1)
            ax.text((x1+x2)/2, (y1+y2)/2, f"{dist:g}m", fontsize=8,
                    color="#64748b", ha="center",
                    bbox=dict(facecolor="white", edgecolor="none", alpha=.8, pad=1))

    palette = {"BFS": "#2563eb", "DFS": "#f59e0b", "A*": "#059669"}
    styles = {"BFS": "--", "DFS": ":", "A*": "-"}
    selected_names = ["BFS", "DFS", "A*"] if show_all else ["A*"]
    offsets = {"BFS": 1.0, "DFS": -1.0, "A*": 0.0}
    for name in selected_names:
        result = results[name]
        if not result:
            continue
        path = result["path"]
        for index, (a, b) in enumerate(zip(path, path[1:])):
            x1, y1 = CAMPUS.locations[a]
            x2, y2 = CAMPUS.locations[b]
            dx, dy = x2-x1, y2-y1
            length = (dx*dx + dy*dy) ** .5 or 1
            offset = offsets[name] * 0.45
            ox, oy = -dy/length*offset, dx/length*offset
            ax.plot([x1+ox, x2+ox], [y1+oy, y2+oy],
                    color=palette[name], linestyle=styles[name],
                    linewidth=4, zorder=2, label=name if index == 0 else None)

    for name, (x, y) in CAMPUS.locations.items():
        is_endpoint = name in (start, goal)
        ax.scatter(x, y, s=190 if is_endpoint else 115,
                   color=("#dc2626" if name == start else "#7c3aed" if name == goal else "white"),
                   edgecolor="#0f172a", linewidth=1.3, zorder=4)
        ax.annotate(name, (x, y), xytext=(6, 8), textcoords="offset points",
                    fontsize=9, fontweight="bold" if is_endpoint else "normal", zorder=5)
    ax.set_xlabel("Campus X coordinate")
    ax.set_ylabel("Campus Y coordinate")
    ax.set_title("Campus graph and calculated routes")
    ax.grid(True, alpha=.2)
    ax.set_aspect("equal", adjustable="datalim")
    handles, labels = ax.get_legend_handles_labels()
    if handles:
        unique = dict(zip(labels, handles))
        ax.legend(unique.values(), unique.keys(), loc="best")
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.markdown("**Route steps**")
    if astar:
        for i, place in enumerate(astar["path"], 1):
            st.write(f"{i}. {place}")

with tabs[1]:
    st.subheader("Search algorithm performance")
    rows = []
    for name, result in results.items():
        if result:
            rows.append({
                "Algorithm": name,
                "Route distance (m)": round(result["distance"], 2),
                "Edges": result["edges"],
                "Nodes expanded": result["nodes_expanded"],
                "Execution time (ms)": round(result["time_ms"], 4),
                "Route": " → ".join(result["path"]),
            })
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)
    if not df.empty:
        left, right = st.columns(2)
        with left:
            st.markdown("**Route distance**")
            st.bar_chart(df.set_index("Algorithm")[["Route distance (m)"]])
        with right:
            st.markdown("**Nodes expanded**")
            st.bar_chart(df.set_index("Algorithm")[["Nodes expanded"]])
    st.info(
        f"Dijkstra baseline minimum distance for this route: {dijkstra_best:.1f} m. "
        f"A* distance: {astar_distance:.1f} m. "
        "Timing values vary between runs and should not be treated as fixed benchmarks."
    )
    st.markdown("""
**How to interpret the comparison**
- **BFS** explores level by level and minimizes the number of edges when all edges are treated equally; it does not guarantee minimum weighted distance.
- **DFS** explores a branch deeply before backtracking and does not guarantee an optimal route.
- **A\*** combines travelled cost `g(n)` and a heuristic estimate `h(n)` using `f(n) = g(n) + h(n)`.
""")

with tabs[2]:
    st.subheader("Project overview")
    st.markdown("""
**Problem definition:** Find a route between two campus locations and compare search methods.

**AI problem formulation**
- Initial state: selected starting location.
- State space: campus locations (graph vertices).
- Actions: move along a connected walkway.
- Transition model: move to an adjacent location.
- Goal test: current location equals the selected destination.
- Path cost: total walkway distance in metres.
- A* heuristic: scaled straight-line distance between map coordinates.

**Implementation:** Python, Streamlit, Matplotlib, and a JSON file containing sample map data.

**Evaluation metrics:** route distance, number of edges, nodes expanded, and execution time.

**Limitations:** This is a fictional sample map. It assumes walkways are bidirectional and static; it does not model accessibility, closures, or live crowd levels. Replace the map data with verified campus locations for a realistic deployment.
""")
    st.download_button(
        "Download route comparison as CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="route_comparison.csv",
        mime="text/csv",
        use_container_width=True,
    )

st.caption("M.Tech Fundamentals of Artificial Intelligence • Mini-project prototype")
