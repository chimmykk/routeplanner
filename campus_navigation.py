"""Graph model and search algorithms for the Smart Campus Navigation System."""
from collections import deque
import json
from time import perf_counter
import heapq
import itertools
import math


class CampusMap:
    def __init__(self, locations, edges, heuristic_scale=None):
        self.locations = locations
        self.graph = {name: {} for name in locations}
        min_ratio = float("inf")
        for a, b, distance in edges:
            if a not in self.graph or b not in self.graph:
                raise ValueError(f"Unknown location in edge: {a}, {b}")
            if distance <= 0:
                raise ValueError("Distances must be positive.")
            self.graph[a][b] = float(distance)
            self.graph[b][a] = float(distance)

            ax, ay = self.locations[a]
            bx, by = self.locations[b]
            euclid = math.hypot(ax - bx, ay - by)
            if euclid > 0:
                min_ratio = min(min_ratio, float(distance) / euclid)

        if heuristic_scale is not None:
            self.heuristic_scale = heuristic_scale
        else:
            self.heuristic_scale = min(0.75, min_ratio * 0.9) if min_ratio < float("inf") else 0.75

    @classmethod
    def from_json(cls, path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls(data["locations"], data["edges"])

    def heuristic(self, a, b):
        """Admissible scaled Euclidean heuristic for the campus map."""
        ax, ay = self.locations[a]
        bx, by = self.locations[b]
        return self.heuristic_scale * math.hypot(ax - bx, ay - by)


class SearchAlgorithms:
    def __init__(self, campus):
        self.campus = campus

    def _result(self, path, expanded, started):
        if path is None:
            return None
        distance = sum(self.campus.graph[u][v] for u, v in zip(path, path[1:]))
        return {
            "path": path,
            "distance": distance,
            "edges": max(0, len(path) - 1),
            "nodes_expanded": expanded,
            "time_ms": (perf_counter() - started) * 1000,
        }

    def bfs(self, start, goal):
        """Breadth-first search; minimizes number of edges, not weighted cost."""
        started = perf_counter()
        queue = deque([start])
        parent = {start: None}
        expanded = 0
        while queue:
            node = queue.popleft()
            expanded += 1
            if node == goal:
                break
            for neighbor in self.campus.graph[node]:
                if neighbor not in parent:
                    parent[neighbor] = node
                    queue.append(neighbor)
        if goal not in parent:
            return None
        return self._result(self._reconstruct(parent, goal), expanded, started)

    def dfs(self, start, goal):
        """Depth-first search; does not guarantee a shortest route."""
        started = perf_counter()
        stack = [start]
        parent = {start: None}
        expanded = 0
        while stack:
            node = stack.pop()
            expanded += 1
            if node == goal:
                break
            for neighbor in reversed(list(self.campus.graph[node].keys())):
                if neighbor not in parent:
                    parent[neighbor] = node
                    stack.append(neighbor)
        if goal not in parent:
            return None
        return self._result(self._reconstruct(parent, goal), expanded, started)

    def astar(self, start, goal):
        """A* with f(n) = g(n) + h(n)."""
        started = perf_counter()
        counter = itertools.count()
        frontier = [(self.campus.heuristic(start, goal), next(counter), start)]
        parent = {start: None}
        g_score = {start: 0.0}
        closed = set()
        expanded = 0
        while frontier:
            _, _, node = heapq.heappop(frontier)
            if node in closed:
                continue
            expanded += 1
            if node == goal:
                return self._result(self._reconstruct(parent, goal), expanded, started)
            closed.add(node)
            for neighbor, distance in self.campus.graph[node].items():
                tentative = g_score[node] + distance
                if tentative < g_score.get(neighbor, float("inf")):
                    g_score[neighbor] = tentative
                    parent[neighbor] = node
                    heapq.heappush(
                        frontier,
                        (tentative + self.campus.heuristic(neighbor, goal),
                         next(counter), neighbor)
                    )
        return None

    @staticmethod
    def _reconstruct(parent, goal):
        path, node = [], goal
        while node is not None:
            path.append(node)
            node = parent[node]
        return list(reversed(path))


def dijkstra_distance(campus, start, goal):
    """Optimal weighted-path baseline used by tests and evaluation."""
    queue = [(0.0, start)]
    best = {start: 0.0}
    while queue:
        cost, node = heapq.heappop(queue)
        if cost != best[node]:
            continue
        if node == goal:
            return cost
        for neighbor, weight in campus.graph[node].items():
            new_cost = cost + weight
            if new_cost < best.get(neighbor, float("inf")):
                best[neighbor] = new_cost
                heapq.heappush(queue, (new_cost, neighbor))
    return float("inf")
