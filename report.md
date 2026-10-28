# Mini-Project Report: Smart Campus Navigation System
### AI Search Strategy Analysis & Empirical Inference Document
**Course:** Fundamentals of Artificial Intelligence  
**AI Techniques:** Breadth-First Search (BFS), Depth-First Search (DFS), and A* Search (Informed Search)  
**Baseline:** Dijkstra Shortest-Path Algorithm  
**Frontend:** Streamlit Interactive Web Application  
**Language:** Python 3  

---

## Abstract
This project implements an interactive campus navigation system designed to evaluate and compare three fundamental Artificial Intelligence search strategies: Breadth-First Search (BFS), Depth-First Search (DFS), and A* Search, evaluated against a provably optimal Dijkstra minimum-distance baseline. Physical campus buildings and interconnecting pedestrian walkways are modeled as weighted graphs. A full-featured Streamlit web application allows users to select source and destination locations, view routes on a 2D coordinate map, compare performance metrics (distance, edge count, nodes expanded, execution time), and export empirical findings.

---

## 1. Problem Definition
Finding an optimal pedestrian route between campus facilities is a fundamental state-space search problem. In physical navigation, minimizing the number of path segments (hops) does not always correspond to minimizing actual walking distance. This project investigates how search algorithms differ in solution quality, computational efficiency, and memory requirements across diverse campus network topologies.

---

## 2. AI Problem Formulation
- **Initial State:** Selected starting location vertex $s \in V$ (e.g., `Main Gate`).
- **State Space:** Finite set of physical campus landmarks $V$ in graph $G = (V, E)$ with known 2D spatial coordinates $(x, y)$.
- **Actions:** Move along a connected pedestrian walkway connecting current vertex $u$ to an adjacent vertex $v$.
- **Transition Model:** Result of action traverse edge $(u, v)$ from state $u$ is successor state $v$.
- **Goal Test:** Predicate checking whether current state $v$ matches the target destination ($v == \text{goal}$).
- **Path Cost $g(n)$:** Sum of physical edge distances (in metres) along traversed walkways from start to node $n$.
- **Heuristic Function $h(n)$:** Scaled Euclidean distance between current node $(x_n, y_n)$ and goal vertex $(x_g, y_g)$:
  $$h(n) = s \times \sqrt{(x_n - x_g)^2 + (y_n - y_g)^2}$$
  The scale factor $s$ is conservatively calibrated ($s \le \min(w / d_{\text{euclid}}) \times 0.9 = 0.75$) ensuring $h(n) \le h^*(n)$ (strict admissibility and monotonicity). A* with this heuristic is guaranteed to find the optimal path matching Dijkstra's baseline.

---

## 3. Campus Datasets
1. **Standard Campus Dataset (`data/campus_map.json`):**
   - 10 core landmarks: Main Gate, Admin Block, Library, CSE Block, AI Lab, Cafeteria, Auditorium, Hostel, Sports Ground, Parking.
   - 15 bidirectional walkways with distances between 23 m and 72 m.
   - Minimum edge-to-Euclidean ratio = 0.92, validated with heuristic scale $s = 0.75$.
2. **Extended University Campus Dataset (`data/campus_map_extended.json`):**
   - 16 academic, residential, and recreational facilities including Security, Medical Center, Robotics Lab, Research Park, Hostels, Dining Hall, Amphitheatre, and Multi-level Parking.
   - 25 bidirectional pedestrian corridors.
   - Minimum edge-to-Euclidean ratio = 0.96, validated with heuristic scale $s = 0.75$.

---

## 4. Empirical Evaluation & Comparison Tables

### Table 1: Route 1 - Main Gate to AI Lab (Standard Dataset)
| Algorithm | Distance (m) | Edges | Nodes Expanded | Time (ms) | Computed Route Path |
|---|---|---|---|---|---|
| **BFS** | 135.0 m | 3 | 10 | 0.026 ms | Main Gate -> Cafeteria -> CSE Block -> AI Lab |
| **DFS** | 129.0 m | 4 | 5 | 0.015 ms | Main Gate -> Admin Block -> Library -> CSE Block -> AI Lab |
| **A\*** | 129.0 m | 4 | 7 | 0.046 ms | Main Gate -> Admin Block -> Library -> CSE Block -> AI Lab |

### Table 2: Route 2 - Parking to Hostel (Standard Dataset)
| Algorithm | Distance (m) | Edges | Nodes Expanded | Time (ms) | Computed Route Path |
|---|---|---|---|---|---|
| **BFS** | 131.0 m | 4 | 9 | 0.027 ms | Parking -> Main Gate -> Admin Block -> Library -> Hostel |
| **DFS** | 131.0 m | 4 | 7 | 0.017 ms | Parking -> Main Gate -> Admin Block -> Library -> Hostel |
| **A\*** | 131.0 m | 4 | 5 | 0.036 ms | Parking -> Main Gate -> Admin Block -> Library -> Hostel |

### Table 3: Route 3 - Main Gate to Sports Complex (Extended Dataset, 16 Locations)
| Algorithm | Distance (m) | Edges | Nodes Expanded | Time (ms) | Computed Route Path |
|---|---|---|---|---|---|
| **BFS** | 142.0 m | 4 | 14 | 0.026 ms | Main Gate -> Security -> Admin Block -> Auditorium -> Sports Complex |
| **DFS** | 160.0 m | 5 | 13 | 0.022 ms | Main Gate -> Security -> Admin -> Cafeteria -> Amphitheatre -> Sports Complex |
| **A\*** | 140.0 m | 4 | 8 | 0.046 ms | Main Gate -> Parking -> Medical Center -> Auditorium -> Sports Complex |

---

## 5. Individual Observations About the Outputs

### 5.1 Individual Observation: Breadth-First Search (BFS)
- **Hop-Count Optimality vs. Path-Cost Sub-optimality:** BFS explores nodes systematically level-by-level using a FIFO queue. BFS is guaranteed to discover the route with the fewest edges. However, in weighted graphs with varying edge costs, minimizing edges does not minimize physical walking distance. In Table 1, BFS selected the 3-hop route via Cafeteria (135.0 m), which is 6.0 m longer than the 4-hop route found by A* (129.0 m).
- **Exhaustive Frontier Expansion:** Because BFS possesses no knowledge of the goal's geometric direction, it radiates uniformly in all directions, expanding 10 out of 10 nodes in Route 1 and 14 out of 16 nodes in Route 3. This leads to exponential memory overhead $O(b^d)$ on large graphs.

### 5.2 Individual Observation: Depth-First Search (DFS)
- **Sensitivity to Traversal Order & Path Unpredictability:** DFS explores recursively down an individual path branch using a LIFO stack. Because DFS does not incorporate edge costs or hop counts, the output route depends entirely on the arbitrary ordering of neighbor vertices. In Table 3, DFS followed an indirect path totaling 160.0 m (a 20.0 m detour compared to A*).
- **Low Memory Footprint During Initial Alignment:** When the destination aligns with the initial branch explored, DFS reaches the target rapidly with minimal node expansions (5 nodes in Route 1) and linear memory complexity $O(b \cdot m)$. However, its erratic route quality makes it unsuitable as a dependable navigation algorithm.

### 5.3 Individual Observation: A* Search (Informed Search)
- **Guaranteed Shortest-Path Optimality:** Guided by $f(n) = g(n) + h(n)$, A* consistently finds the mathematically optimal path distance across all queries (129.0 m, 131.0 m, and 140.0 m), perfectly matching the Dijkstra minimum-distance baseline with 100% precision.
- **Directional Heuristic Pruning:** Using 2D coordinates, the heuristic focuses search effort directly toward the goal. In Route 2, A* expanded only 5 nodes compared to 9 nodes for BFS (44.4% reduction). In Route 3, A* expanded 8 nodes compared to 14 nodes for BFS (42.8% reduction). This makes A* the most robust and scalable choice for campus navigation.

---

## 6. Automated Verification
The project includes automated unit tests (`tests/test_navigation.py`):
- All-Pairs Optimality: Exhaustive check of all $V \times V$ pairs against Dijkstra baseline on both datasets (100% match).
- Edge Integrity: Confirms all path steps use genuine graph edges.
- Exact Distance Summation: Asserts path distance equals the sum of edge weights.
- Boundary Queries: Tests zero-distance identity queries.
All 6 tests execute in 0.012 seconds with 100% pass rate.

---

## 7. Submission Package
- Report formats provided: `Smart_Campus_Navigation_Inference_Report.pdf` and `Smart_Campus_Navigation_Inference_Report.docx`.
- High-resolution visual screenshots included in `screenshots/`.
- Submission archive: `Smart_Campus_Navigation_Solution.zip`.
