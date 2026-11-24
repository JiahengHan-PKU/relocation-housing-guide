"""Turn a raw OpenStreetMap walk network into a routable graph."""

import json
import math


def build_walk_graph(raw_path):
    """Build an undirected graph of walkable ways.

    Each OpenStreetMap node becomes a vertex and each consecutive pair of
    nodes on a way becomes an edge weighted by its length in meters. One-way
    tags are ignored because pedestrians can walk both ways.

    Args:
        raw_path: Overpass JSON from fetch_walk_network.py (ways with "nodes"
            and "geometry").

    Returns:
        (coords, adjacency, grid): coords maps node id to (lat, lon),
        adjacency maps node id to a list of (neighbor id, meters), and grid
        maps a 0.001-degree cell to the node ids inside it, for snapping.
    """
    coords, adjacency, grid = {}, {}, {}
    for way in json.load(open(raw_path))["elements"]:
        points = list(zip(way.get("nodes", []), way.get("geometry", [])))
        for node, g in points:
            if node not in coords:
                coords[node] = (g["lat"], g["lon"])
                grid.setdefault((round(g["lat"], 3), round(g["lon"], 3)), []).append(node)
        for (a, ga), (b, gb) in zip(points, points[1:]):
            k = math.cos(math.radians(ga["lat"]))
            meters = 6371000 * math.hypot(math.radians(gb["lon"] - ga["lon"]) * k, math.radians(gb["lat"] - ga["lat"]))
            adjacency.setdefault(a, []).append((b, meters))
            adjacency.setdefault(b, []).append((a, meters))
    return coords, adjacency, grid
