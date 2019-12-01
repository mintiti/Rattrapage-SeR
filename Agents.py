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


# TODO : coder les contraintes de capacité


class Solution:
    """
    Décrit une solution pour le jeu de reseau_telecom
    Attributs ;
        - X : matrice [x_ij] qui vaut 1 si et seulement si le target node i est lié au steiner node j
        - Y : liste [Y_j] qui decrit le traveling salesman sur les steiner nodes
        - Z : matrice [z_ki] qui vaut 1 si et seulement si le client k est lié au target node i
    """

    # Validity check functions
    def nb_connections_target(self, target):
        target_column = self.Z[:, target]
        target_line = self.X[target, :]
        return sum(target_column) + sum(target_line)

    def nb_connections_steiner(self, steiner):
        count = 0
        if steiner in self.Y:
            count += 2
        steiner_column = self.X[:, steiner]
        count += sum(steiner_column)
        return count

    def steiner_plein(self, steiner):
        return self.nb_connections_steiner(steiner) >= self.steiner_capacity[steiner]

    def target_plein(self, target):
        return self.nb_connections_target(target) >= self.target_capacity[target]

    def steiner_overload(self, steiner):
        return self.nb_connections_steiner(steiner) > self.steiner_capacity[steiner]

    def target_overload(self, target):
        return self.nb_connections_target(target) > self.target_capacity[target]

    def valide(self):
        """
        For now only checks steiner and target node overload
        """
        valid = True
        for steiner in range(self.nb_steiner):
            if not valid:
                break
            valid = valid and not self.steiner_overload(steiner)

        for target in range(self.nb_target):
            if not valid:
                break
            valid = valid and not self.target_overload(target)
        return valid

    def __init__(self, environnement):
        """
        Initialise une solution aléatoire pour le jeu
        :param environnement: l'environnement pour lequel on créée une solution, de type ReseauTelecomExcel
        """
        nb_steiner = environnement.nb_steiner
        nb_target = environnement.nb_targetNode
        nb_client = environnement.nb_client
        self.nb_steiner = nb_steiner
        self.nb_target = nb_target
        self.nb_client = nb_client
        self.steiner_capacity = environnement.steiner_capacity
        self.target_capacity = environnement.target_capacity

        # création aléatoire de Y :

        test = False
        liste_steiner = [i for i in range(nb_steiner)]
        while not test:
            nb_de_steiner_actives = rd.randint(3, nb_steiner)
            self.Y = rd.sample(liste_steiner, nb_de_steiner_actives)
            # calcul du nombre de la capacite totale du hub de steiner
            capacite_steiner = 0
            for steiner in self.Y:
                capacite_steiner += environnement.steiner_capacity[steiner]
            test = capacite_steiner >= environnement.nb_client + environnement.nb_steiner
        # création aléatoire de X :
        self.X = np.zeros((nb_target, nb_steiner))
        for i in range(nb_target):
            inserted = False
            while not inserted:
                steiner_choisi = self.Y[rd.randint(0, nb_de_steiner_actives - 1)]
                if not self.steiner_plein(steiner_choisi):
                    self.X[i, steiner_choisi] = 1
                    inserted = True

        # création aléatoire de Z :
        self.Z = np.zeros((nb_client, nb_target))
        for k in range(nb_client):
            inserted = False

            while not inserted:
                target_choisi = rd.randint(0, nb_target - 1)
                if not self.target_plein(target_choisi):
                    self.Z[k, target_choisi] = 1
                    inserted = True

    @classmethod
    def Vide(cls, environnement):
        """
        Créée un agent vide, sans aucune connexion
        :param environnement:
        :return:
        """
        nb_steiner = environnement.nb_steiner
        nb_target = environnement.nb_targetNode
        nb_client = environnement.nb_client
        agent = cls(environnement)
        agent.X = np.zeros((nb_target, nb_steiner))
        agent.Y = []
        agent.Z = np.zeros((nb_client, nb_target))
        return agent

    def croisement_clients(self, sol):
        """
        croise les clients de self et sol
        :param sol: autre parent
        :return: enfant 1, enfant 2
        """
        # prendre le nombre de client
        nb_clients = self.nb_client
        # en choisir un nombre
        nb_crossover = round(nb_clients * CLIENT_CROSSOVER_PERCENTAGE)
        tries_counter = 0
        valid_childrens = False
        while not valid_childrens:
            print('tentative crossover clients', tries_counter)
            if tries_counter < 100:
                # selectionner ce nombre de client
                list_crossover = rd.sample(range(0, nb_clients), nb_crossover)
                # echanger les connexions de ces clients
                enfant_1 = deepcopy(self)
                enfant_2 = deepcopy(sol)
                matrice_enfant_1 = enfant_1.Z
                matrice_enfant_2 = enfant_2.Z

                for client in list_crossover:
                    ligne_1 = matrice_enfant_1[client, :].copy()
                    ligne_2 = matrice_enfant_2[client, :].copy()
                    matrice_enfant_1[client, :] = ligne_2
                    matrice_enfant_2[client, :] = ligne_1

                valid_childrens = enfant_1.valide() and enfant_2.valide()
            else:
                break

            tries_counter += 1

        return enfant_1, enfant_2

    def croisement_targets(self, sol):
        # prendre le nombre de targets
        nb_target = self.nb_target
        # en choisir un nombre a croiser
        nb_crossover = round(nb_target * TARGET_CROSSOVER_PERCENTAGE)
        valid_children = False
        tries_counter = 0
        while not valid_children:
            if tries_counter < 200:
                # selectionner ce nombre de client
                list_crossover = rd.sample(range(0, nb_target), nb_crossover)
                # echanger les connexions de ces clients
                enfant_1 = deepcopy(self)
                enfant_2 = deepcopy(sol)
                matrice_enfant_1 = enfant_1.X
                matrice_enfant_2 = enfant_2.X

                for target in list_crossover:
                    ligne_1 = matrice_enfant_1[target, :].copy()
                    ligne_2 = matrice_enfant_2[target, :].copy()
                    matrice_enfant_1[target, :] = ligne_2
                    matrice_enfant_2[target, :] = ligne_1
                valid_children = enfant_1.valide() and enfant_2.valide()
                tries_counter += 1
            else:
                break

        return enfant_1, enfant_2

    def croisement(self, sol):
        """
        Croisement total de self et sol
        :param sol: l'autre parent
        :return: enfant1, enfant2 les 2enfants
        """
        enfant1, enfant2 = self.croisement_targets(sol)
        enfant1, enfant2 = enfant1.croisement_clients(enfant2)

        return enfant1, enfant2

    # TODO : mettre des anti blocage de mutation
    def _mutation_client_target(self):
        client_mute = rd.randint(0, self.nb_client - 1)
        mutation_valide = False
        while not mutation_valide:
            nouvelle_target = rd.randint(0, self.nb_target - 1)
            print('recherche nouvelle target', nouvelle_target)
            for i in range(self.nb_target):
                if i == nouvelle_target:
                    self.Z[client_mute, i] = 1
                else:
                    self.Z[client_mute, i] = 0
            mutation_valide = self.valide()

    # TODO : Prendre seulement les steiners actives
    def _mutation_target_steiner(self):
        original = self.X.copy()
        target_mute = rd.randint(0, self.nb_target - 1)
        mutation_valide = False
        tries_counter = 0
        while not mutation_valide:
            # choisir le nouveau steiner auquel se connecter
            if tries_counter < 1000:
                nouveau_steiner = self.Y[rd.randint(0, len(self.Y) - 1)]
                print('recherche nouveau steiner :', nouveau_steiner, 'Essai numéro', tries_counter)
                tries_counter += 1
                for i in range(self.nb_steiner):
                    if i == nouveau_steiner:
                        self.X[target_mute, i] = 1
                    else:
                        self.X[target_mute, i] = 0
                mutation_valide = self.valide()
            else:
                # Don't mutate
                self.X = original
                break

    def _mutation_ring_RSM(self):
        # chose the section to invert
        l = rd.sample(range(self.nb_steiner + 1), 2)
        l.sort()
        [i, j] = l
        # reverse te corresponding part of the steiner ring
        rev = self.Y[i:j]
        rev.reverse()
        self.Y[i:j] = rev

    def _mutation_ring_change(self):
        # Choose a steiner not in the ring
        if len(self.Y) < self.nb_steiner:
            steiner_ok = False
            while not steiner_ok:
                steiner_choisi = rd.randint(0, self.nb_steiner - 1)
                steiner_ok = steiner_choisi not in self.Y
        # mutate a random steiner in the ring
        index = rd.randint(0, len(self.Y) - 1)
        self.Y[index] = steiner_choisi

    def _mutation_ring(self):
        self._mutation_ring_change()
        self._mutation_ring_RSM()

    def mutation(self):
        dice = (rd.randint(1, 100)) / 100
        if dice < MUTATION_PROBABILITY:
            # Ajouter aléatoirement un steiner
            self._mutation_ring()
            # muter la proportion de target_steiner
            nb_mutation_target_steiner = round(self.nb_target * TARGET_STEINER_MUTATION_PROPORTION)
            for i in range(nb_mutation_target_steiner):
                self._mutation_target_steiner()
            # muter la proportion de client_target
            nb_mutation_client_target = round(self.nb_client * CLIENT_TARGET_MUTATION_PROPORTION)


if __name__ == '__main__':
    import Environnement

    excel = "InputDataTelecomSmallInstance.xlsx"

    env = Environnement.ReseauTelecomFromExcel(excel)
    S = Solution(env)
    S2 = Solution(env)
    print(S.X)
    S.mutation()
    print(S.X)
