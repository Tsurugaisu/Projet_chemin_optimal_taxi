import pytest
from Lib.lib_graphe import (
    Graphe,
    bellman_ford,
    _ralentissement,
    _fluidification,
    _travaux,
    chemin_ralentissement,
    chemin_fluidification,
    chemin_travaux,
)


def test_initialisation():
    g = Graphe(sommets=list("ABC"), arretes=[("A", "B", 1.5)])
    assert isinstance(g, Graphe)


def test_verifications_ponderations():
    with pytest.raises(ValueError):
        g = Graphe(sommets=list("ABC"), arretes=[("A", "B", -1.5)])


def test_verifications_sommets():
    with pytest.raises(ValueError):
        g = Graphe(sommets=list("AC"), arretes=[("A", "B", 1.5)])
    with pytest.raises(ValueError):
        g = Graphe(sommets=list("BC"), arretes=[("A", "B", 1.5)])


@pytest.fixture
def Ex_graphe():
    return Graphe(
        sommets=[
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
            "11",
            "12",
            "13",
            "14",
            "15",
            "16",
        ],
        arretes=[
            ("1", "2", 5.0),
            ("1", "3", 9.0),
            ("1", "4", 4.0),
            ("2", "5", 3.0),
            ("2", "6", 2.0),
            ("3", "4", 4.0),
            ("3", "6", 1.0),
            ("4", "7", 7.0),
            ("5", "8", 4.0),
            ("5", "9", 2.0),
            ("5", "10", 9.0),
            ("6", "7", 3.0),
            ("6", "10", 9.0),
            ("6", "11", 6.0),
            ("7", "11", 8.0),
            ("7", "15", 5.0),
            ("8", "12", 5.0),
            ("9", "8", 3.0),
            ("9", "13", 10.0),
            ("10", "9", 6.0),
            ("10", "13", 5.0),
            ("10", "14", 1.0),
            ("11", "14", 2.0),
            ("12", "16", 9.0),
            ("13", "12", 4.0),
            ("13", "14", 3.0),
            ("14", "16", 4.0),
            ("15", "14", 4.0),
            ("15", "16", 3.0),
        ],
    )


@pytest.fixture
def Ex_graphe2():
    return Graphe(
        sommets=["1", "2", "3", "4", "5"],
        arretes=[
            ("1", "2", 2.0),
            ("1", "3", 4.0),
            ("3", "4", 1.0),
            ("2", "4", 2.0),
            ("2", "5", 6.0),
            ("4", "5", 3.0),
        ],
    )


def test_bellman_ford_1(Ex_graphe):
    attendue = {"distance": 18.0, "chemins": [["1", "2", "6", "7", "15", "16"]]}
    assert bellman_ford(Ex_graphe, "1", "16") == attendue


def test_bellman_ford_1_1(Ex_graphe2):
    attendue = {"distance": 7.0, "chemins": [["1", "2", "4", "5"]]}
    assert bellman_ford(Ex_graphe2, "1", "5") == attendue


def test_ralentissement(Ex_graphe2):
    attendue = Graphe(
        sommets=["1", "2", "3", "4", "5"],
        arretes=[
            ("1", "2", 5.0),
            ("1", "3", 4.0),
            ("3", "4", 1.0),
            ("2", "4", 2.0),
            ("2", "5", 6.0),
            ("4", "5", 3.0),
        ],
    )
    assert _ralentissement(Ex_graphe2, "1", "2", 3.0) == attendue


def test_ralentissement_2(Ex_graphe2):
    attendue = Graphe(
        sommets=["1", "2", "3", "4", "5"],
        arretes=[
            ("1", "2", 5.0),
            ("1", "3", 4.0),
            ("3", "4", 1.0),
            ("2", "4", 2.0),
            ("2", "5", 6.0),
            ("4", "5", 3.0),
        ],
    )
    assert _ralentissement(Ex_graphe2, "2", "1", 3.0) == attendue


def test_ralentissement_3(Ex_graphe2):
    with pytest.raises(ValueError):
        _ralentissement(Ex_graphe2, "1", "2", -3.0)


def test_chemin_ralentissement(Ex_graphe):
    attendue = {"distance": 14.0, "chemins": [["5", "10", "13"]]}
    assert chemin_ralentissement(Ex_graphe, "5", "13", "9", "13", 3.0) == attendue


def test_fluidification(Ex_graphe2):
    attendue = Graphe(
        sommets=["1", "2", "3", "4", "5"],
        arretes=[
            ("1", "2", 2.0),
            ("1", "3", 4.0),
            ("3", "4", 1.0),
            ("2", "4", 2.0),
            ("2", "5", 3.0),
            ("4", "5", 3.0),
        ],
    )
    assert _fluidification(Ex_graphe2, "2", "5", 3.0) == attendue


def test_fluidification_2(Ex_graphe2):
    ## pour vérifier que la durée d'un chemin ne soit pas négatif
    with pytest.raises(ValueError):
        _fluidification(Ex_graphe2, "1", "2", 6.0)


def test_chemin_fluidification(Ex_graphe):
    attendue = {"distance": 9.0, "chemins": [["5", "9", "13"]]}
    assert chemin_fluidification(Ex_graphe, "5", "13", "9", "13", 3.0) == attendue


def test_travaux(Ex_graphe2):
    attendue = Graphe(
        sommets=["1", "2", "3", "4", "5"],
        arretes=[
            ("1", "2", 3.0),
            ("1", "3", 5.0),
            ("3", "4", 1.0),
            ("2", "4", 3.0),
            ("2", "5", 7.0),
            ("4", "5", 3.0),
        ],
    )
    assert _travaux(Ex_graphe2, ["1", "2"]) == attendue


def test_chemin_travaux(Ex_graphe):
    attendue = {"distance": 20.0, "chemins": [["1", "2", "6", "7", "15", "16"]]}
    assert chemin_travaux(Ex_graphe, "1", "16", ["3", "5", "7", "9", "11"]) == attendue

