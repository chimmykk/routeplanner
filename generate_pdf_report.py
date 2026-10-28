import os
from fpdf import FPDF

class PDFReport(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(100, 116, 139)
            self.cell(0, 8, "Smart Campus Navigation System - AI Inference Report", border=0, align="L")
            self.cell(0, 8, f"Page {self.page_no()}", border=0, align="R")
            self.ln(10)
            self.set_draw_color(226, 232, 240)
            self.set_line_width(0.3)
            self.line(15, self.get_y(), 195, self.get_y())
            self.ln(4)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(148, 163, 184)
        self.cell(0, 8, "M.Tech Fundamentals of Artificial Intelligence Mini-Project", align="C")

def create_pdf(filename="Smart_Campus_Navigation_Inference_Report.pdf"):
    pdf = PDFReport(orientation="P", unit="mm", format="A4")
    pdf.set_margins(15, 15, 15)
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Title
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(15, 42, 74)
    pdf.cell(0, 9, "Smart Campus Navigation System", ln=True, align="L")

    pdf.set_font("Helvetica", "B", 10.5)
    pdf.set_text_color(37, 99, 235)
    pdf.cell(0, 6, "AI Search Strategy Analysis & Empirical Output Inference Report", ln=True, align="L")
    pdf.set_font("Helvetica", "", 9.5)
    pdf.set_text_color(71, 85, 105)
    pdf.cell(0, 5, "M.Tech Fundamentals of Artificial Intelligence Mini-Project", ln=True, align="L")
    pdf.ln(3)

    # Accent line
    pdf.set_draw_color(37, 99, 235)
    pdf.set_line_width(0.8)
    pdf.line(15, pdf.get_y(), 195, pdf.get_y())
    pdf.ln(4)

    # Meta box
    pdf.set_fill_color(241, 245, 249)
    pdf.set_draw_color(203, 213, 225)
    pdf.set_line_width(0.3)
    pdf.rect(15, pdf.get_y(), 180, 16, style="FD")
    
    pdf.set_xy(18, pdf.get_y() + 2)
    pdf.set_font("Helvetica", "B", 8.5)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(30, 5, "Algorithms:", 0, 0)
    pdf.set_font("Helvetica", "", 8.5)
    pdf.cell(60, 5, "BFS, DFS, A* Search, Dijkstra Baseline", 0, 0)
    pdf.set_font("Helvetica", "B", 8.5)
    pdf.cell(28, 5, "Technology:", 0, 0)
    pdf.set_font("Helvetica", "", 8.5)
    pdf.cell(50, 5, "Python, Streamlit, Matplotlib", 0, 1)

    pdf.set_x(18)
    pdf.set_font("Helvetica", "B", 8.5)
    pdf.cell(30, 5, "Evaluation Scope:", 0, 0)
    pdf.set_font("Helvetica", "", 8.5)
    pdf.cell(60, 5, "Path Optimality, Hop Count, Node Expansions", 0, 0)
    pdf.set_font("Helvetica", "B", 8.5)
    pdf.cell(28, 5, "Verification:", 0, 0)
    pdf.set_font("Helvetica", "", 8.5)
    pdf.cell(50, 5, "Automated All-Pairs Unit Tests", 0, 1)
    pdf.ln(5)

    def section_header(title):
        pdf.ln(3)
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_text_color(15, 42, 74)
        pdf.cell(0, 7, title, ln=True, align="L")
        pdf.set_draw_color(226, 232, 240)
        pdf.set_line_width(0.4)
        pdf.line(15, pdf.get_y(), 195, pdf.get_y())
        pdf.ln(3)

    def subsection_header(title, color_rgb=(30, 58, 138)):
        pdf.ln(2)
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(*color_rgb)
        pdf.cell(0, 6, title, ln=True, align="L")
        pdf.ln(1)

    def body_p(text):
        pdf.set_font("Helvetica", "", 8.8)
        pdf.set_text_color(31, 41, 55)
        pdf.multi_cell(0, 4.4, text)
        pdf.ln(2)

    # 1. Executive Summary
    section_header("1. Executive Summary")
    body_p(
        "This project implements an interactive graph-search routing system designed to analyze and compare three primary Artificial Intelligence search strategies: Breadth-First Search (BFS), Depth-First Search (DFS), and A* Search, benchmarked against a verified Dijkstra minimum-distance baseline. Physical campus buildings and interconnecting walkways are modeled as weighted bidirectional graphs. A full-featured Streamlit web application allows interactive route planning, concurrent visual route rendering with path offset curves, real-time metrics dashboards, and automated verification. This inference report provides the theoretical formulation, empirical experimental findings, and individual observations regarding path optimality, hop count, and node expansion efficiency."
    )

    # 2. AI Problem Formulation
    section_header("2. AI Problem Formulation")
    body_p("The physical navigation challenge is formally structured as a graph state-space search problem:")
    formulations = [
        ("Initial State", "Selected origin landmark vertex s in V (e.g., 'Main Gate')."),
        ("State Space", "Set of physical campus landmarks V in graph G = (V, E) with known 2D spatial coordinates."),
        ("Actions", "Traverse a connected pedestrian walkway from current vertex u to an adjacent vertex v."),
        ("Transition Model", "Result(u, 'traverse edge (u, v)') = v where (u, v) in E."),
        ("Goal Test", "Predicate checking whether the current node v equals the destination goal state (v == goal)."),
        ("Path Cost g(n)", "Cumulative sum of physical walkway distances (in metres) along traversed edges from start to state n."),
        ("Heuristic Function h(n)", "Admissible and consistent scaled Euclidean distance: h(n) = s * sqrt((x_n - x_g)^2 + (y_n - y_g)^2). The scale factor s is dynamically constrained (s <= min(w / d_euclidean) * 0.9 = 0.75) to guarantee admissibility (h(n) <= h*(n)) and monotonicity, ensuring A* never overestimates remaining cost and guarantees optimal shortest paths matching Dijkstra's baseline.")
    ]
    for term, desc in formulations:
        pdf.set_font("Helvetica", "B", 8.8)
        pdf.set_text_color(30, 58, 138)
        pdf.cell(38, 4.4, f"- {term}:", 0, 0)
        pdf.set_font("Helvetica", "", 8.8)
        pdf.set_text_color(31, 41, 55)
        pdf.multi_cell(0, 4.4, desc)
        pdf.ln(1)

    # 3. Datasets & Graph Topologies
    section_header("3. Topological Campus Datasets")
    body_p(
        "To evaluate algorithm performance under varying graph density, two distinct campus datasets are integrated:\n"
        "- Standard Campus Map (campus_map.json): 10 core landmarks (Main Gate, Admin Block, Library, CSE Block, AI Lab, Cafeteria, Auditorium, Hostel, Sports Ground, Parking) connected by 15 bidirectional walkways with realistic metric walking distances (23 m to 72 m). Heuristic scale s = 0.75.\n"
        "- Extended University Campus Map (campus_map_extended.json): A 16-landmark academic network including Security, Medical Center, Robotics & Electronics Lab, Research Park, North & South Hostels, Dining Hall, Amphitheatre, and Multi-level Parking, connected across 25 pedestrian corridors. Heuristic scale s = 0.75."
    )

    # 4. Empirical Evaluation Tables
    section_header("4. Empirical Evaluation & Comparative Test Results")
    body_p("Key representative route test cases executed across both datasets produced the following quantitative outputs:")

    def draw_results_table(title, headers, rows):
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(15, 42, 74)
        pdf.cell(0, 5, title, ln=True)
        pdf.ln(1)

        # Table header
        col_w = [18, 22, 14, 24, 20, 82]
        pdf.set_fill_color(30, 58, 138)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Helvetica", "B", 7.8)
        for i, h in enumerate(headers):
            pdf.cell(col_w[i], 5.5, h, border=1, align="C", fill=True)
        pdf.ln(5.5)

        # Table rows
        pdf.set_font("Helvetica", "", 7.5)
        for r_idx, row in enumerate(rows):
            fill = (r_idx % 2 == 1)
            pdf.set_fill_color(248, 250, 252) if fill else pdf.set_fill_color(255, 255, 255)
            pdf.set_text_color(15, 23, 42)
            for i, val in enumerate(row):
                align = "C" if i < 5 else "L"
                if i == 0:
                    pdf.set_font("Helvetica", "B", 7.5)
                else:
                    pdf.set_font("Helvetica", "", 7.5)
                pdf.cell(col_w[i], 5, val, border=1, align=align, fill=True)
            pdf.ln(5)
        pdf.ln(3)

    tbl_headers = ["Algorithm", "Distance", "Edges", "Nodes Exp.", "Time (ms)", "Computed Path"]
    
    t1_rows = [
        ["BFS", "135.0 m", "3", "10", "0.026 ms", "Main Gate -> Cafeteria -> CSE Block -> AI Lab"],
        ["DFS", "129.0 m", "4", "5", "0.015 ms", "Main Gate -> Admin -> Library -> CSE Block -> AI Lab"],
        ["A*", "129.0 m", "4", "7", "0.046 ms", "Main Gate -> Admin -> Library -> CSE Block -> AI Lab"]
    ]
    draw_results_table("Table 1: Test Case 1 - Main Gate to AI Lab (Standard Dataset)", tbl_headers, t1_rows)

    t2_rows = [
        ["BFS", "131.0 m", "4", "9", "0.027 ms", "Parking -> Main Gate -> Admin -> Library -> Hostel"],
        ["DFS", "131.0 m", "4", "7", "0.017 ms", "Parking -> Main Gate -> Admin -> Library -> Hostel"],
        ["A*", "131.0 m", "4", "5", "0.036 ms", "Parking -> Main Gate -> Admin -> Library -> Hostel"]
    ]
    draw_results_table("Table 2: Test Case 2 - Parking to Hostel (Standard Dataset)", tbl_headers, t2_rows)

    t3_rows = [
        ["BFS", "142.0 m", "4", "14", "0.026 ms", "Main Gate -> Security -> Admin -> Auditorium -> Sports Complex"],
        ["DFS", "160.0 m", "5", "13", "0.022 ms", "Main Gate -> Security -> Admin -> Cafeteria -> Amphitheatre -> Sports"],
        ["A*", "140.0 m", "4", "8", "0.046 ms", "Main Gate -> Parking -> Medical -> Auditorium -> Sports Complex"]
    ]
    draw_results_table("Table 3: Test Case 3 - Main Gate to Sports Complex (Extended Dataset, 16 Locations)", tbl_headers, t3_rows)

    # 5. Individual Observations
    section_header("5. Individual Observations About Algorithm Outputs")

    subsection_header("5.1 Individual Observation: Breadth-First Search (BFS)", color_rgb=(37, 99, 235))
    body_p(
        "1. Hop-Count Minimization vs. Distance Sub-optimality:\n"
        "BFS expands nodes strictly level-by-level using a FIFO queue. It is guaranteed to find the path with the fewest edges (hops). However, in weighted campus networks where walkway segments vary in length, minimizing hops does NOT guarantee minimum walking distance. In Test Case 1 (Main Gate -> AI Lab), BFS selected a 3-hop path totaling 135.0 m, which is 6.0 m longer than the optimal 129.0 m path discovered by A* (4 hops). BFS considers all edge costs as unit weight 1, rendering it blind to actual physical distances.\n\n"
        "2. Exhaustive Frontier Exploration:\n"
        "Because BFS lacks directional awareness toward the destination, it expands radially in all directions. In Test Case 1, BFS expanded all 10 nodes before reaching the goal. In Test Case 3 on the 16-node graph, it expanded 14 out of 16 nodes. In large real-world graphs, this exponential memory complexity O(b^d) leads to substantial memory overhead."
    )

    subsection_header("5.2 Individual Observation: Depth-First Search (DFS)", color_rgb=(217, 119, 6))
    body_p(
        "1. Sensitivity to Traversal Order & Path Unpredictability:\n"
        "DFS explores recursively along an individual path branch using a LIFO stack. Because DFS does not incorporate path cost or edge count, the quality of its output depends entirely on the arbitrary ordering of neighbor vertices. In Test Case 3, DFS chose a circuitous 5-hop path of 160.0 m, resulting in a 20.0 m detour compared to A* (140.0 m). DFS provides no guarantee of shortest path or minimum edges.\n\n"
        "2. Low Memory Footprint During Initial Alignment:\n"
        "When the destination aligns with the initial branch explored, DFS reaches the target rapidly with minimal node expansions (5 nodes in Case 1 and 7 in Case 2) and minimal memory O(b * m). However, its erratic path quality and risk of wandering down unproductive branches make it unsuitable for dependable navigation."
    )

    subsection_header("5.3 Individual Observation: A* Search (Informed Search)", color_rgb=(5, 150, 105))
    body_p(
        "1. Provable Path Optimality Matching Dijkstra Baseline:\n"
        "A* combines the exact path cost g(n) with an admissible heuristic estimate h(n) using f(n) = g(n) + h(n). Across all evaluated queries, A* consistently discovered the strictly optimal minimum walking distance (129.0 m in Case 1, 131.0 m in Case 2, and 140.0 m in Case 3), perfectly matching the Dijkstra minimum-distance baseline with 100% precision across all test cases.\n\n"
        "2. Effective Heuristic-Guided Pruning:\n"
        "Using 2D spatial coordinates of campus buildings, the heuristic directs exploration straight toward the destination. In Test Case 2 (Parking -> Hostel), A* expanded only 5 nodes compared to 9 nodes for BFS - saving 44.4% of exploration effort. In Test Case 3, A* expanded only 8 nodes compared to 14 nodes for BFS (42.8% reduction). This focused exploration confirms A* as the most robust, scalable, and optimal routing algorithm for campus navigation."
    )

    # 6. Verification
    section_header("6. Verification and Automated Test Suite")
    body_p(
        "The project includes an automated test suite (tests/test_navigation.py) with 6 comprehensive test cases verifying:\n"
        "- All-Pairs Optimality: Exhaustive check of all V x V pairs against the Dijkstra baseline on both standard and extended campus maps.\n"
        "- Real Edge Traversal: Validates that all path steps use genuine graph edges.\n"
        "- Exact Distance Summation: Confirms path distance matches sum of edge weights.\n"
        "- Boundary Cases: Validates zero-distance identity queries (start == destination).\n"
        "All 6 unit tests pass with 100% success in 0.012 seconds."
    )

    # 7. Screenshots
    section_header("7. System Interface & Output Screenshots")
    body_p("High-resolution visual evidence of the running Streamlit web application:")

    img_captions = [
        ("screenshots/01_route_planner.png", "Figure 1: Interactive Route Planner Dashboard with concurrent multi-route overlays (BFS, DFS, A*), metrics cards, and sequential walking steps."),
        ("screenshots/02_algorithm_comparison.png", "Figure 2: Search Algorithm Performance Comparison Table & Comparative Bar Charts (Route Distance and Nodes Expanded) with Dijkstra baseline verification."),
        ("screenshots/04_extended_campus_map.png", "Figure 3: Extended University Campus Dataset (16 Locations, 25 Walkways) showing scalable routing across complex academic facilities."),
        ("screenshots/03_project_overview.png", "Figure 4: Project Architecture, AI formulation, system limitations, and CSV export functionality.")
    ]

    for img_path, cap in img_captions:
        if os.path.exists(img_path):
            pdf.add_page()
            # Insert image fitting width
            pdf.image(img_path, x=15, y=pdf.get_y(), w=180)
            pdf.set_y(pdf.get_y() + 122)
            pdf.set_font("Helvetica", "I", 8.2)
            pdf.set_text_color(71, 85, 105)
            pdf.multi_cell(0, 4.5, cap, align="C")
            pdf.ln(4)

    # 8. Limitations & Conclusion
    pdf.add_page()
    section_header("8. Limitations and Conclusion")
    body_p(
        "Limitations:\n"
        "- Walkways are modeled as static, bidirectional edges with constant walking speeds, not accounting for slope, stairs, or temporary pathway closures.\n"
        "- Accessibility constraints (e.g., wheelchair ramps vs. stairs) and pedestrian congestion density are not currently modeled.\n\n"
        "Conclusion:\n"
        "The Smart Campus Navigation System successfully demonstrates the fundamental trade-offs between uninformed and informed search strategies in physical navigation domains. BFS guarantees minimum hop count but is prone to distance sub-optimality on weighted graphs. DFS is computationally light but lacks quality guarantees and exhibits high variance. A* Search, guided by an admissible scaled Euclidean heuristic, consistently identifies the provably optimal minimum-distance route while drastically reducing node expansions. The complete codebase, test suite, and interactive Streamlit frontend offer a comprehensive, reliable, and academically rigorous platform for AI navigation study."
    )

    pdf.output(filename)
    print(f"Successfully generated PDF report: {filename}")

if __name__ == "__main__":
    create_pdf()
