# coding=utf-8
##### IMPORTS #####
import numpy as np
import random


class ReseauTelecom:
    """
    Décris l'environnement
    contient Steiner Node, target node et les clients
    contient les coûts de liaison de chaque poste
    contient la fonction qui calcule le cout total de construction

    Attributs :
        - steiners : numpy array d'un nb fixé de couple, décrivant une coordonnée
        - targetNodes : numpy array d'un nb fixé de couple, décrivant une coordonnée
        - clients : numpy array d'un nb fixé de couple, décrivant une coordonnée
    """

    def __init__(self, nb_steiner=6, nb_targetNode=5, nb_clients=8, grid_size=(10, 10)):
        """
        Initialise le Réseau de neurones aléatoirement uniformement sur la grille

        :param nb_steiner: nombre de Steiner node voulus
        :param nb_targetNode: nombre de Target Node voulus
        :param nb_clients: nombre de clients voulus
        :param grid_size: taille de la grille
        :type grid_size: couple
        """

        (x, y) = grid_size
        self.steiners = [(random.uniform(0, x), random.uniform(0, y)) for i in range(nb_steiner)]
        self.nb_steiner = nb_steiner

        self.targetNodes = [(random.uniform(0, x), random.uniform(0, y)) for i in range(nb_targetNode)]
        self.nb_target_node = nb_targetNode

        self.clients = [(random.uniform(0, x), random.uniform(0, y)) for i in range(nb_clients)]
        self.nb_clients = nb_clients
