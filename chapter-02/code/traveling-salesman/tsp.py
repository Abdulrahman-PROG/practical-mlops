import itertools
import math
import json
import urllib.request


def haversine(coord1, coord2):
    """Distance in km between two (lat, lon) coordinates."""
    R = 6371
    lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
    lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return R * 2 * math.asin(math.sqrt(a))


def fetch_restaurants(city="Cairo", limit=8):
    """Fetch restaurant coordinates from Nominatim (OpenStreetMap) — no API key needed."""
    query = urllib.parse.quote(f"restaurant in {city}")
    url = (
        f"https://nominatim.openstreetmap.org/search"
        f"?q={query}&format=json&limit={limit}&addressdetails=0"
    )
    req = urllib.request.Request(url, headers={"User-Agent": "mlops-tsp-exercise/1.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read())
    places = [(item["display_name"].split(",")[0], float(item["lat"]), float(item["lon"]))
              for item in data]
    return places


def brute_force_tsp(places):
    """Exact solution via brute force — practical for up to ~10 places."""
    names = [p[0] for p in places]
    coords = [(p[1], p[2]) for p in places]
    best_distance = float("inf")
    best_route = None

    for perm in itertools.permutations(range(len(coords))):
        dist = sum(
            haversine(coords[perm[i]], coords[perm[(i + 1) % len(perm)]])
            for i in range(len(perm))
        )
        if dist < best_distance:
            best_distance = dist
            best_route = perm

    return [names[i] for i in best_route], best_distance


def nearest_neighbor_tsp(places):
    """Greedy nearest-neighbor heuristic — fast for larger inputs."""
    names = [p[0] for p in places]
    coords = [(p[1], p[2]) for p in places]
    unvisited = list(range(len(coords)))
    route = [unvisited.pop(0)]
    total = 0.0

    while unvisited:
        last = route[-1]
        nearest = min(unvisited, key=lambda i: haversine(coords[last], coords[i]))
        total += haversine(coords[last], coords[nearest])
        route.append(nearest)
        unvisited.remove(nearest)

    total += haversine(coords[route[-1]], coords[route[0]])
    return [names[i] for i in route], total


if __name__ == "__main__":
    import urllib.parse
    import sys

    city = sys.argv[1] if len(sys.argv) > 1 else "Cairo"
    print(f"Fetching restaurants in {city}...")

    try:
        places = fetch_restaurants(city)
        if len(places) < 2:
            print("Not enough results. Try a different city.")
            sys.exit(1)
    except Exception as e:
        print(f"API unavailable ({e}), using sample data.")
        places = [
            ("Koshary El Tahrir", 30.0444, 31.2357),
            ("Abou Tarek", 30.0626, 31.2497),
            ("Kebdet El Prince", 30.0580, 31.2290),
            ("Felfela", 30.0459, 31.2395),
            ("Lucille's", 30.0711, 31.2161),
        ]

    print(f"\nFound {len(places)} restaurants:")
    for name, lat, lon in places:
        print(f"  {name} ({lat:.4f}, {lon:.4f})")

    route, distance = nearest_neighbor_tsp(places)
    print(f"\nOptimal visit order (nearest-neighbor):")
    for i, name in enumerate(route, 1):
        print(f"  {i}. {name}")
    print(f"\nTotal distance: {distance:.2f} km")
