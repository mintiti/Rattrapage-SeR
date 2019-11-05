# coding=utf-8
import random as rd
import numpy as np
from config import cfg

## CONSTANTS ##
MUTATION_PROBABILITY = cfg['mutation_probability']


class Solution:
    # TODO : définir comment on veut coder les gènes, càd les attributs
    """
    Décrit une solution pour le jeu de telecom
    Attributs ;
        - X : matrice [x_ij] qui vaut 1 si et seulement si le target node i est lié au steiner node j
        - Y : liste [Y_j] qui decrit le traveling salesman sur les steiner nodes
        - Z : matrice [z_ki] qui vaut 1 si et seulement si le client k est lié au target node i
    """

    def __init__(self, environnement):
        """
        Initialise une solution aléatoire pour le jeu
        :param environnement: l'environnement pour lequel on créée une solution
        """
        nb_steiner = environnement.nb_steiner
        nb_target = environnement.nb_target_node
        nb_client = environnement.nb_clients

        # création aléatoire de Y :
        nb_de_steiner_actives = rd.randint(3, nb_steiner)
        liste_steiner = [i for i in range(nb_steiner)]
        rd.shuffle(liste_steiner)
        self.Y = liste_steiner[:nb_de_steiner_actives]

        # création aléatoire de X :
        X = np.zeros((nb_target, nb_steiner))
        for i in range(nb_target):
            steiner_choisi = self.Y[rd.randint(0, nb_de_steiner_actives - 1)]
            X[i, steiner_choisi] = 1
        self.X = X

        # création aléatoire de Z :
        Z = np.zeros((nb_client, nb_target))
        for k in range(nb_client):
            index = rd.randint(0, nb_target - 1)
            Z[k, index] = 1
        self.Z = Z


#    def mutation(self):
# TODO : Ecrire

#    def croisement(self, sol1, sol2):
# TODO : Ecrire


if __name__ == '__main__':
    import Environnement

    env = Environnement.ReseauTelecom()
    S = Solution(env)
    print(S.X)
    print(S.Y)
    print(S.Z)
