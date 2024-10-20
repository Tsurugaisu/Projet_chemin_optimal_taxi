import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Lib.lib_graphe import (
    Graphe,
    bellman_ford,
    chemin_ralentissement,
    chemin_fluidification,
    chemin_travaux,
)
import typer


app = typer.Typer()


Ex_graphe = Graphe(
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


@app.command()
def chemin_optimal_basique(depart: str, arrivee: str):
    resultat = bellman_ford(Ex_graphe, depart, arrivee)
    print(
        f"Pour aller de {depart} à {arrivee}, cela vous prendra {resultat['distance']} minutes et vous passerez par les emplacements {resultat['chemins']}."
    )


@app.command()
def chemin_optimal_ralenti(
    depart: str, arrivee: str, emplacement_1: str, emplacement2: str, temps: float
):
    resultat = chemin_ralentissement(
        Ex_graphe, depart, arrivee, emplacement_1, emplacement2, temps
    )
    print(
        f"En prenant en compte les ralentissements de trafic d'une durée de {temps} minutes, cela vous prendra {resultat['distance']} minutes pour aller de {depart} à {arrivee}, minutes et vous passerez par les emplacements {resultat['chemins']}."
    )


@app.command()
def chemin_optimal_fluidifie(
    depart: str, arrivee: str, emplacement_1: str, emplacement2: str, temps: float
):
    resultat = chemin_fluidification(
        Ex_graphe, depart, arrivee, emplacement_1, emplacement2, temps
    )
    print(
        f"En prenant en compte les fluidifications de trafic d'une durée de {temps} minutes, cela vous prendra {resultat['distance']} minutes pour aller de {depart} à {arrivee}, minutes et vous passerez par les emplacements {resultat['chemins']}."
    )


@app.command()
def chemin_optimal_travaux(depart: str, arrivee: str, emplacements_travaux: list[str]):
    resultat = chemin_travaux(Ex_graphe, depart, arrivee, emplacements_travaux)
    print(
        f"En prenant en compte les emplacements en travaux, cela vous prendra {resultat['distance']} minutes pour aller de {depart} à {arrivee}, minutes et vous passerez par les emplacements {resultat['chemins']}."
    )


if __name__ == "__main__":
    app()
