# Présentation

Ce projet a pour but de résoudre le problème présenté dans `Sujet7.md`. On s'est basé sur l'algorithme de Bellman-Ford afin de le résoudre.

- Tests à l'aide de `pytest`.
- Utilisation de `black` pour formatter le code.
- Gestion des dépendances via `poetry`.
- Application en ligne de commande avec `typer`.
- Utilisation de `ruff` comme linter.

# Utilisation de l'application

- On peut accéder à l'aide de l'application à l'aide de la commande `--help`.

<img src=Images/App_help.PNG>

On constate qu'il y a 4 commandes différentes, qui permettent de trouver les chemins optimaux en fonctions des potentiels ralentissements/fluidifications/travaux sur les routes.

- On peut regarder l'aide d'une commande en particulier, par exemple `chemin-optimal-basique`

<img src=Images/chemin_optimal_basique_help.PNG>

On peut voir qu'elle prend comme argument un sommet de `départ` et un sommet d'`arrivée`. À noter également qu'il faut les rentrer comme chaîne de caractères, c'est à dire avec des guillemets, comme ceci: 

<img src=Images/chemin_optimal_basique(1,16).PNG>


- On peut faire de même pour la commande `chemin-optimal-ralenti`

<img src=Images/chemin_optimal_ralenti_help.PNG>

<img src=Images/chemin_optimal_ralenti_AN.PNG>


