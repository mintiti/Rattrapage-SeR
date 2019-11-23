# coding=utf-8
import random as rd
from copy import deepcopy

import numpy as np
from config import cfg
from Environnement import ReseauTelecom

## CONSTANTS ##
MUTATION_PROBABILITY = cfg['mutation_probability']
CLIENT_CROSSOVER_PERCENTAGE = cfg['client_crossover_percentage']
TARGET_CROSSOVER_PERCENTAGE = cfg['target_crossover_percentage']
TARGET_STEINER_MUTATION_PROPORTION = cfg['target_steiner_mutation_proportion']
CLIENT_TARGET_MUTATION_PROPORTION = cfg['client_target_mutation_proportion']

class Solution:
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
        self.nb_steiner = nb_steiner
        self.nb_target = nb_target
        self.nb_client = nb_client

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

    @classmethod
    def Vide(cls, environnement):
        """
        Créée un agent vide, sans aucune connexion
        :param environnement:
        :return:
        """
        nb_steiner = environnement.nb_steiner
        nb_target = environnement.nb_target_node
        nb_client = environnement.nb_clients
        agent = cls(environnement)
        agent.X = np.zeros((nb_target, nb_steiner))
        agent.Y = []
        agent.Z = np.zeros((nb_client, nb_target))
        return agent




    def croisement_clients (self, sol):
        """
        croise les clients de self et sol
        :param sol: autre parent
        :return: enfant 1, enfant 2
        """
        #prendre le nombre de client
        nb_clients = self.nb_client
        #en choisir un nombre
        nb_crossover = round(nb_clients * CLIENT_CROSSOVER_PERCENTAGE)
        #selectionner ce nombre de client
        list_crossover = rd.sample(range(0,nb_clients),nb_crossover)
        #echanger les connexions de ces clients
        enfant_1 = deepcopy(self)
        enfant_2 = deepcopy(sol)
        matrice_enfant_1 = enfant_1.Z
        matrice_enfant_2 = enfant_2.Z

        for client in list_crossover :
            ligne_1 = matrice_enfant_1[client,:].copy()
            ligne_2 = matrice_enfant_2[client,:].copy()
            matrice_enfant_1[client,:] = ligne_2
            matrice_enfant_2[client,:] = ligne_1

        return enfant_1, enfant_2
    def croisement_targets(self, sol):
        #prendre le nombre de targets
        nb_target = self.nb_target
        #en choisir un nombre a croiser
        nb_crossover = round(nb_target * TARGET_CROSSOVER_PERCENTAGE)
        # selectionner ce nombre de client
        list_crossover = rd.sample(range(0,nb_target), nb_crossover)
        #echanger les connexions de ces clients
        enfant_1 = deepcopy(self)
        enfant_2 = deepcopy(sol)
        matrice_enfant_1 = enfant_1.X
        matrice_enfant_2 = enfant_2.X

        for target in list_crossover :
            ligne_1 = matrice_enfant_1[target,:].copy()
            ligne_2 = matrice_enfant_2[target,:].copy()
            matrice_enfant_1[target,:] = ligne_2
            matrice_enfant_2[target,:] = ligne_1

        return enfant_1,enfant_2

    def croisement(self,sol):
        enfant1,enfant2 = self.croisement_targets(sol)
        enfant1,enfant2 = enfant1.croisement_clients(sol)

        return enfant1,enfant2
    def _mutation_client_target(self):
        client_mute = rd.randint(0, self.nb_client - 1)
        nouvelle_target = rd.randint(0, self.nb_target - 1)
        for i in range(self.nb_target):
            if i == nouvelle_target :
                self.Z[client_mute,i] = 1
            else :
                self.Z[client_mute, i] = 0

    def _mutation_target_steiner(self):
        target_mute = rd.randint(0, self.nb_target - 1)
        print(target_mute)
        nouveau_steiner = rd.randint(0, self.nb_steiner - 1)
        print(nouveau_steiner)
        for i in range(self.nb_steiner) :
            if i == nouveau_steiner :
                self.X[target_mute,i] = 1
            else :
                self.X[target_mute,i] = 0

    def _mutation_ring(self):
        #choisir un steiner qui n'est pas dans le cycle
        nouveau_steiner = -1
        while nouveau_steiner not in self.Y :
            nouveau_steiner = rd.randint(0, self.nb_steiner - 1)
        #l'ajouter a un endroit aleatoire
        rd_index = rd.randint(0,len(self.Y))
        self.Y.insert(rd_index,nouveau_steiner)


    def mutation(self):
        dice = (rd.randint(1,100) ) / 100
        if dice < MUTATION_PROBABILITY :
            #Ajouter aléatoirement un steiner
            self._mutation_ring()
            #muter la proportion de target_steiner
            nb_mutation_target_steiner = round(self.nb_target * TARGET_STEINER_MUTATION_PROPORTION)
            for i in range(nb_mutation_target_steiner):
                self._mutation_target_steiner()
            #muter la proportion de client_target
            nb_mutation_client_target = round(self.nb_client * CLIENT_TARGET_MUTATION_PROPORTION)




if __name__ == '__main__':
    import Environnement

    env = Environnement.ReseauTelecom()
    S = Solution(env)
    S2 = Solution(env)
    print(S.X)
    S._mutation_target_steiner()
    print(S.X)
