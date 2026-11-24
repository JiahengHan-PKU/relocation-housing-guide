"""Measure street-network walking distances from buildings to nearby places."""

import csv
import heapq
import json
import math

from build_walk_graph import build_walk_graph


def route_pois(table_path, pois_path, network_path, out_path, radius=2000, bus_radius=400, limit=3500):
    """Write walking distances from each building to the places around it.

    Routes run on the local OpenStreetMap walk network from
    fetch_walk_network.py, so no routing service is called. The straight-line
    gaps between each point and the network are added to the shortest path.
    Every node within 80 m of a building is a starting
    point, and the best node within 60 m of a place is its end point, so a
    point that falls inside a large lot does not get stuck on one driveway.
    Places with no network node within 150 m are skipped.

    Args:
        table_path: Path to data/buildings.csv.
        pois_path: Path to data/pois.json; keys in the output are list indexes.
        network_path: Path to data/walk_network_raw.json.
        out_path: Destination JSON, {building_id: {poi_index: meters}}.
        radius: Straight-line cutoff in meters for most places.
        bus_radius: Straight-line cutoff in meters for bus stops.
        limit: Longest route searched, in meters.

    Returns:
        The number of buildings routed.
    """
    coords, adjacency, grid = build_walk_graph(network_path)
    flat = lambda a, b: math.hypot((a[0] - b[0]) * 110540, (a[1] - b[1]) * 111320 * math.cos(math.radians(a[0])))

    def near(point, reach):
        cells = [(round(point[0], 3) + i / 1000, round(point[1], 3) + j / 1000) for i in (-1, 0, 1) for j in (-1, 0, 1)]
        found = sorted((flat(point, coords[n]), n) for c in cells for n in grid.get((round(c[0], 3), round(c[1], 3)), []) if n in adjacency)
        return [x for x in found if x[0] <= reach] or found[:1]

    pois = json.load(open(pois_path))
    out = {}
    for b in csv.DictReader(open(table_path)):
        if b["status"] != "include" or not b["lat"]:
            continue
        home = (float(b["lat"]), float(b["lon"]))
        dist = {n: gap for gap, n in near(home, 80)}
        queue = [(gap, n) for n, gap in dist.items()]
        heapq.heapify(queue)
        while queue:
            d, node = heapq.heappop(queue)
            if d > dist.get(node, math.inf) or d > limit:
                continue
            for nxt, w in adjacency[node]:
                if d + w < dist.get(nxt, math.inf):
                    dist[nxt] = d + w
                    heapq.heappush(queue, (d + w, nxt))
        out[b["id"]] = {}
        for i, p in enumerate(pois):
            if p.get("lat") and flat(home, (p["lat"], p["lon"])) <= (bus_radius if p["kind"] == "bus_stop" else radius):
                ends = [gap + dist[n] for gap, n in near((p["lat"], p["lon"]), 60) if gap <= 150 and n in dist]
                if ends:
                    out[b["id"]][str(i)] = round(min(ends))
    json.dump(out, open(out_path, "w"))
    return len(out)


if __name__ == "__main__":
    print(route_pois("data/buildings.csv", "data/pois.json", "data/walk_network_raw.json", "data/poi_routes.json"))
