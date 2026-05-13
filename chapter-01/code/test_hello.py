from hello import add, greet


def test_add():
    assert add(1, 2) == 3


def test_greet():
    assert greet("MLOps") == "Hello, MLOps!"
