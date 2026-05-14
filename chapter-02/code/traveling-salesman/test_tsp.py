from tsp import haversine, nearest_neighbor_tsp, brute_force_tsp

PLACES = [
    ("A", 30.0444, 31.2357),
    ("B", 30.0626, 31.2497),
    ("C", 30.0580, 31.2290),
    ("D", 30.0459, 31.2395),
]


def test_haversine_same_point():
    assert haversine((30.0, 31.0), (30.0, 31.0)) == 0.0


def test_haversine_positive():
    assert haversine((30.0, 31.0), (31.0, 32.0)) > 0


def test_nearest_neighbor_returns_all_places():
    route, dist = nearest_neighbor_tsp(PLACES)
    assert len(route) == len(PLACES)
    assert dist > 0


def test_brute_force_returns_all_places():
    route, dist = brute_force_tsp(PLACES)
    assert len(route) == len(PLACES)
    assert dist > 0


def test_brute_force_optimal():
    # brute force must be <= nearest neighbor
    _, bf_dist = brute_force_tsp(PLACES)
    _, nn_dist = nearest_neighbor_tsp(PLACES)
    assert bf_dist <= nn_dist + 0.001
