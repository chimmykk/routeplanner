"""Command-line version; the Streamlit frontend is launched with run_app.sh."""
import sys
from pathlib import Path
from campus_navigation import CampusMap, SearchAlgorithms

ROOT = Path(__file__).resolve().parent

def main():
    map_file = "campus_map_extended.json" if "--extended" in sys.argv else "campus_map.json"
    campus = CampusMap.from_json(ROOT / "data" / map_file)
    print("\nSMART CAMPUS NAVIGATION SYSTEM - BFS vs DFS vs A*")
    print(f"Loaded dataset: {map_file}\n")
    for i, place in enumerate(campus.graph, 1):
        print(f"{i:2}. {place}")
    start = input("\nStarting location: ").strip()
    goal = input("Destination: ").strip()
    if start not in campus.graph or goal not in campus.graph:
        print("Invalid location. Choose a name exactly as listed.")
        return
    search = SearchAlgorithms(campus)
    for name, fn in (("BFS", search.bfs), ("DFS", search.dfs), ("A*", search.astar)):
        result = fn(start, goal)
        print(f"\n{name}")
        if result is None:
            print("No route found.")
        else:
            print("Route:", " -> ".join(result["path"]))
            print(f"Distance: {result['distance']:.1f} m | Edges: {result['edges']} | "
                  f"Nodes expanded: {result['nodes_expanded']} | Time: {result['time_ms']:.4f} ms")

if __name__ == "__main__":
    main()
