"""Description

Librairie permettant de résoudre le sujet donné.
"""

from dataclasses import dataclass
import networkx as nx
import matplotlib.pyplot as plt


@dataclass(frozen=True, unsafe_hash=True)
class Graphe:
    """Dataclass représentant la ville sous forme d'un Graphe

        sommets représente les différents emplacements de la ville.
        arretes représente les différentes routes reliant les emplacements de la ville.

        On veille à ce que les distances soit positives via le poids des arrêtes, et à ce que le départ et l'arrivée soit bien un des emplacements existants.

        Exemple :

    >>> G=Graphe(
    ...         sommets=["1", "2", "3", "4", "5"],
    ...         arretes=[
    ...             ("1", "2", 2.0),
    ...             ("1", "3", 4.0),
    ...             ("3", "4", 1.0),
    ...             ("2", "4", 2.0),
    ...             ("2", "5", 6.0),
    ...             ("4", "5", 3.0),
    ...         ],
    ...     )
    """

    sommets: list[str]
    arretes: list[tuple[str, str, float]]

    def __post_init__(self):
        for depart, arrivee, poids in self.arretes:
            if poids < 0:
                raise ValueError("Les pondérations des arrêtes doivent être positives!")
            if depart not in self.sommets:
                raise ValueError(f"{depart=} n'est pas dans la liste des sommets!")
            if arrivee not in self.sommets:
                raise ValueError(f"{arrivee=} n'est pas dans la liste des sommets!")


def bellman_ford(graphe: Graphe, depart: str, arrivee: str) -> dict:
    """Fonction nous permettant d'exécuter l'algorithme de bellman-ford afin d'obtenir le chemin le plus court entre 2 emplacements de la ville.
        Cette fonction prend en entrée 3 arguments, à savoir le graphe de la ville, le point de départ et le point d'arrivée.
        Elle renvoie un dictionnaire avec la distance totale parcourue et les sommets visités.

        Exemple:
    >>> bellman_ford(G,"1","5")
    {'distance': 7.0, 'chemins': [['1', '2', '4', '5']]}

    >>> bellman_ford(Ex_graphe,"1","16")
    {'distance': 18.0, 'chemins': [['1', '2', '6', '7', '15', '16']]}


    """
    distance = {sommet: float("inf") for sommet in graphe.sommets}
    distance[depart] = 0
    predecesseurs = {sommet: [] for sommet in graphe.sommets}

    for _ in range(len(graphe.sommets) - 1):
        for sommet_depart, sommet_arrivee, poids in graphe.arretes:
            if distance[sommet_depart] + poids < distance[sommet_arrivee]:
                distance[sommet_arrivee] = distance[sommet_depart] + poids
                predecesseurs[sommet_arrivee] = [sommet_depart]
            elif distance[sommet_depart] + poids == distance[sommet_arrivee]:
                predecesseurs[sommet_arrivee].append(sommet_depart)

    for sommet_depart, sommet_arrivee, poids in graphe.arretes:
        if distance[sommet_depart] + poids < distance[sommet_arrivee]:
            raise ValueError("Le graphe contient un cycle de poids négatif")

    if not predecesseurs[arrivee]:
        raise ValueError(f"Aucun chemin trouvé entre {depart} et {arrivee}")

    chemins = []
    for pred in predecesseurs[arrivee]:
        chemin = [arrivee]
        while pred:
            chemin.insert(0, pred)
            pred = predecesseurs[pred][0] if predecesseurs[pred] else None
        if chemin not in chemins:
            chemins.append(chemin)

    return {"distance": distance[arrivee], "chemins": chemins}


def _ralentissement(
    graphe: Graphe, sommet_depart: str, sommet_arrivee: str, temps: float
) -> Graphe:
    """Fonction renvoyant un graphe représentant la ville modifiée par les ralentissement potentiels.

    Args:
        graphe (Graphe): Graphe de la ville
        sommet_depart (str): emplacement impactée par le ralentissement
        sommet_arrivee (str): emplacement impactée par le ralentissement
        temps (float): durée de la fluidification entre les 2 emplacements

    Raises:
        ValueError: Si le temps de travaux est négatif

    Returns:
        Graphe: Graphe de la ville en prenant en compte les ralentissements
    """
    if temps < 0:
        raise ValueError("La durée indiquée doit être positive")
    arretes_modifiees = []
    for depart, arrivee, poids in graphe.arretes:
        if (depart == sommet_depart and arrivee == sommet_arrivee) or (
            depart == sommet_arrivee and arrivee == sommet_depart
        ):
            poids_modifie = poids + temps
            arretes_modifiees.append((depart, arrivee, poids_modifie))
        else:
            arretes_modifiees.append((depart, arrivee, poids))

    return Graphe(graphe.sommets, arretes_modifiees)


def chemin_ralentissement(
    graphe: Graphe,
    depart: str,
    arrivee: str,
    emplacement_1: str,
    emplacement_2: str,
    temps: float,
) -> dict:
    """Fonction qui renvoie le chemin optimal et la distance parcourue entre 2 sommets en prenant en compte les ralentissements potentiels.

            Args:
                graphe (Graphe): Graphe de la ville
                depart (str): Point de départ
                arrivee (str): Point d'arrivée
                emplacement_1 (str): emplacement en travaux
                emplacement_2 (str): emplacement en travaux
                temps (float): durée du ralentissement entre les 2 emplacements

            Returns:
                dict: chemin optimal et distance parcourue

            Exemple:
        >>> chemin_ralentissement(G,"1","5","1","2",3.0)
        {'distance': 8.0, 'chemins': [['1', '3', '4', '5']]}

        >>> chemin_ralentissement(Ex_graphe,"5","13","9","13",3.0)
    {'distance': 14.0, 'chemins': [['5', '10', '13']]}
    """
    A = _ralentissement(graphe, emplacement_1, emplacement_2, temps)
    return bellman_ford(A, depart, arrivee)


def _fluidification(
    graphe: Graphe, sommet_depart: str, sommet_arrivee: str, temps: float
) -> Graphe:
    """Fonction renvoyant un graphe représentant la ville modifiée par les fluidifications potentielles.

    Args:
        graphe (Graphe): Graphe de la ville
        sommet_depart (str): emplacement impactée par la fluidification
        sommet_arrivee (str): emplacement impactée par la fluidification
        temps (float): durée de la fluidification entre les 2 emplacements

    Raises:
        ValueError: vérifie que la durée indiquée est positive
        ValueError: vérifie que la distance entre 2 points est positive

    Returns:
        Graphe: Graphe de la ville modifié
    """
    if temps < 0:
        raise ValueError("La durée indiquée doit être positive")
    arretes_modifiees = []
    for depart, arrivee, poids in graphe.arretes:
        if (depart == sommet_depart and arrivee == sommet_arrivee) or (
            depart == sommet_arrivee and arrivee == sommet_depart
        ):
            poids_modifie = poids - temps
            if poids_modifie < 0:
                raise ValueError(
                    "La durée entre 2 emplacements ne peut pas être négative"
                )
            arretes_modifiees.append((depart, arrivee, poids_modifie))
        else:
            arretes_modifiees.append((depart, arrivee, poids))

    return Graphe(graphe.sommets, arretes_modifiees)


def chemin_fluidification(
    graphe: Graphe,
    depart: str,
    arrivee: str,
    emplacement_1: str,
    emplacement_2: str,
    temps: float,
) -> dict:
    """Fonction qui renvoie le chemin optimal et la distance parcourue entre 2 sommets en prenant en compte les fluidifications potentielles.

            Args:
                graphe (Graphe): Graphe de la ville
                depart (str): Point de départ
                arrivee (str): Point d'arrivée
                emplacement_1 (str): emplacement fluidifié
                emplacement_2 (str): emplacement fluidifié
                temps (float): durée de la fluidification entre les 2 emplacements

            Returns:
                dict: chemin optimal et distance parcourue

            Exemple:
        >>> chemin_fluidification(G,"1","5","1","2",1.0)
        {'distance': 6.0, 'chemins': [['1', '2', '4', '5']]}

        >>> chemin_fluidification(Ex_graphe,"5","13","9","13",3.0)
    {'distance': 9.0, 'chemins': [['5', '9', '13']]}
    """
    A = _fluidification(graphe, emplacement_1, emplacement_2, temps)
    return bellman_ford(A, depart, arrivee)


def _travaux(graphe: Graphe, sommets_travaux: list[str]) -> Graphe:
    """Fonction renvoyant un graphe représentant la ville modifiée par les travaux potentiels.

    Args:
        graphe (Graphe): Graphe de la ville
        sommets_travaux (list[str]): emplacement(s) en travaux

    Returns:
        Graphe: Graphe de la ville modifié par les travaux
    """

    arretes_modifiees = []
    for depart, arrivee, poids in graphe.arretes:
        poids_modifie = poids
        if depart in sommets_travaux or arrivee in sommets_travaux:
            poids_modifie = poids + 1.0
        arretes_modifiees.append((depart, arrivee, poids_modifie))
    return Graphe(graphe.sommets, arretes_modifiees)


def chemin_travaux(
    graphe: Graphe, depart: str, arrivee: str, sommets_travaux: list[str]
) -> dict:
    """Fonction renvoyant le chemin optimal et la distance parcourue en prenant en compte les travaux potentiels.

            Args:
                graphe (Graphe): Graphe de la ville
                depart (str): point de départ
                arrivee (str): point d'arrivée
                sommets_travaux (list[str]): emplacement(s) en travaux

            Returns:
                dict: chemin optimal et distance parcourue

            Exemple:

            >>> chemin_travaux(G,"1","5",["1","2","4"])
    {'distance': 10.0, 'chemins': [['1', '2', '5'], ['1', '2', '4', '5']]}

            >>> chemin_travaux(Ex_graphe,"1","16",["3","5","7","9","11"])
        {'distance': 20.0, 'chemins': [['1', '2', '6', '7', '15', '16']]}
    """
    A = _travaux(graphe, sommets_travaux)
    return bellman_ford(A, depart, arrivee)


def carte_graphe(
    graphe: Graphe, chemin: dict = None, travaux: list[str] = None
) -> nx.Graph:
    """Fonction renvoyant le graphe de la ville en fonction du chemin emprunté et des travaux potentiels."""
    G = nx.Graph()
    G.add_nodes_from(graphe.sommets)
    G.add_weighted_edges_from(graphe.arretes)

    positions = nx.spring_layout(G)

    edge_labels = {(a, b): poids for a, b, poids in graphe.arretes}
    nx.draw_networkx_edges(G, positions, edge_color="gray")
    nx.draw_networkx_edge_labels(G, positions, edge_labels=edge_labels)
    nx.draw_networkx_labels(G, positions)

    if chemin:
        nodes_visites = chemin["chemins"][0]
        node_colors = [
            "red" if node in nodes_visites else "green" for node in G.nodes()
        ]
        nx.draw_networkx_nodes(G, positions, node_color=node_colors, node_size=500)
        plt.title("Carte de la ville avec le chemin emprunté")

    elif travaux:
        node_colors = ["yellow" if node in travaux else "green" for node in G.nodes()]
        nx.draw_networkx_nodes(G, positions, node_color=node_colors, node_size=500)
        plt.title("Carte de la ville avec travaux")

    else:
        nx.draw_networkx_nodes(G, positions, node_color="green", node_size=500)
        plt.title("Carte de la ville")

    plt.show()

    return G


def bellman_ford_2(graphe: Graphe) -> dict:
    """Pour trouver les chemins les plus courts entre tous les points de la ville."""
    distances = {}
    for sommet in graphe.sommets:
        distances[sommet] = {}
        for autre_sommet in graphe.sommets:
            if sommet == autre_sommet:
                distances[sommet][autre_sommet] = 0
            else:
                distances[sommet][autre_sommet] = float("inf")
    for depart, arrivee, poids in graphe.arretes:
        distances[depart][arrivee] = poids
    for k in graphe.sommets:
        for i in graphe.sommets:
            for j in graphe.sommets:
                if distances[i][k] + distances[k][j] < distances[i][j]:
                    distances[i][j] = distances[i][k] + distances[k][j]
    return distances


from tabulate import tabulate


def afficher_distances(distances: dict):
    """Pour afficher les distances entre tous les points de la ville sous forme de tableau."""
    headers = [""] + list(distances.keys())
    rows = []
    for sommet, distances_vers_autres in distances.items():
        row = [sommet]
        for autre_sommet, distance in distances_vers_autres.items():
            row.append(distance)
        rows.append(row)
    print(tabulate(rows, headers=headers, tablefmt="grid"))
