# Smart Campus Navigation System
### Fundamentals of Artificial Intelligence Mini-Project
**AI Techniques:** Breadth-First Search (BFS), Depth-First Search (DFS), and A* Search  
**Optimal Baseline:** Dijkstra Algorithm  
**Frontend:** Streamlit Interactive Web Interface  
**Language:** Python 3  

## Features
- Interactive Web Frontend with dataset switching, departure/destination selection, and real-time visualization.
- Dual Campus Datasets:
  - Standard Campus Map (10 locations, 15 walkways)
  - Extended University Campus Map (16 locations, 25 walkways)
- BFS, DFS, and A* Comparison: distance, edges (hops), nodes expanded, and execution latency.
- Concurrent route visualization with path offset curves.
- Provable A* path optimality verified against Dijkstra's shortest-path baseline.
- Export comparison results to CSV.
- Command-line version and automated test suite.
- Clean code with zero emojis.
- Submission-ready reports in both PDF and DOCX formats with individual algorithm observations and embedded screenshots.

## Project Structure
```text
Smart_Campus_Navigation_Full_Project/
├── app.py                                         # Streamlit frontend application
├── campus_navigation.py                           # Core graph search algorithms (BFS, DFS, A*, Dijkstra)
├── main.py                                        # Command-line interface demo
├── data/
│   ├── campus_map.json                            # Standard campus dataset (10 landmarks)
│   └── campus_map_extended.json                   # Extended university dataset (16 landmarks)
├── screenshots/                                   # High-resolution application screenshots
│   ├── 01_route_planner.png                       # Route planner & graph overlay
│   ├── 02_algorithm_comparison.png                # Performance metrics table & charts
│   ├── 03_project_overview.png                    # Project formulation & export view
│   └── 04_extended_campus_map.png                 # Extended campus map view
├── tests/
│   └── test_navigation.py                         # Automated test suite (6/6 tests passing)
├── Smart_Campus_Navigation_Inference_Report.pdf   # Formatted PDF Inference Report
├── Smart_Campus_Navigation_Inference_Report.docx  # Formatted DOCX Inference Report
├── report.md                                      # Markdown report
├── requirements.txt                               # Dependencies
├── run_app.sh                                     # macOS/Linux launcher
└── run_app.bat                                    # Windows launcher
```

## Quick Start

### macOS / Linux
```bash
chmod +x run_app.sh
./run_app.sh
```

Or manually:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

### Windows
```bat
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

### Run Command-Line Version
```bash
# Standard dataset
python main.py

# Extended university campus dataset
python main.py --extended
```

### Run Automated Tests
```bash
python -m unittest discover -s tests -v
```
