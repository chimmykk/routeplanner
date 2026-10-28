import json
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from campus_navigation import CampusMap, SearchAlgorithms, dijkstra_distance

DATA = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "campus_map.json")
DATA_EXTENDED = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "campus_map_extended.json")

class NavigationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.campus = CampusMap.from_json(DATA)
        cls.search = SearchAlgorithms(cls.campus)
        cls.campus_ext = CampusMap.from_json(DATA_EXTENDED)
        cls.search_ext = SearchAlgorithms(cls.campus_ext)

    def test_all_algorithms_return_valid_endpoints(self):
        for method in (self.search.bfs, self.search.dfs, self.search.astar):
            result = method("Main Gate", "AI Lab")
            self.assertIsNotNone(result)
            self.assertEqual(result["path"][0], "Main Gate")
            self.assertEqual(result["path"][-1], "AI Lab")

    def test_extended_map_all_pairs_astar_matches_dijkstra(self):
        for start in self.campus_ext.graph:
            for goal in self.campus_ext.graph:
                actual = self.search_ext.astar(start, goal)
                expected = dijkstra_distance(self.campus_ext, start, goal)
                self.assertIsNotNone(actual)
                self.assertAlmostEqual(actual["distance"], expected)

    def test_every_path_uses_real_edges(self):
        for method in (self.search.bfs, self.search.dfs, self.search.astar):
            result = method("Parking", "Hostel")
            for a, b in zip(result["path"], result["path"][1:]):
                self.assertIn(b, self.campus.graph[a])

    def test_distance_is_sum_of_edge_costs(self):
        result = self.search.astar("Main Gate", "AI Lab")
        expected = sum(self.campus.graph[a][b]
                       for a, b in zip(result["path"], result["path"][1:]))
        self.assertAlmostEqual(result["distance"], expected)

    def test_astar_matches_dijkstra_for_all_pairs(self):
        for start in self.campus.graph:
            for goal in self.campus.graph:
                actual = self.search.astar(start, goal)
                expected = dijkstra_distance(self.campus, start, goal)
                self.assertIsNotNone(actual)
                self.assertAlmostEqual(actual["distance"], expected)

    def test_same_start_and_goal(self):
        result = self.search.astar("Library", "Library")
        self.assertEqual(result["path"], ["Library"])
        self.assertEqual(result["distance"], 0)

if __name__ == "__main__":
    unittest.main()
