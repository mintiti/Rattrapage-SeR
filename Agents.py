# coding=utf-8


class Solutions :
    #TODO : définir comment on veut coder les gènes, càd les attributs
    """
    Décrit une solution pour le jeu de telecom
    Attributs ;
        - X : matrice [x_ij] qui vaut 1 si et seulement si le tqarget node i est lié au steiner node j
        - Y : matrice [y_ij] qui vaut 1 si et seulement si le steiner node est lié au steiner node k (j<k)
        - Z = matrice [z_j] qui vaut 1 si et seulement si le steiner node j est activé
    """

    def __init__(self,environnement):
        """
        Initialise une solution aléatoire pour le jeu
        :param environnement: l'environnement pour lequel on créée une solution
        """
        nb_steiner = environnement.nb_steiner
        nb_target = environnement.nb_target_node
        nb_client = environnement.nb_clients
        self.X =
        self.Y =
        self.z =