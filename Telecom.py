# IMPORTS


import gym
from gym import error, spaces, utils
from gym.utils import seeding
import random
from Environnement import ReseauTelecom
from Agents import Solution
from math import sqrt
import numpy as np
import matplotlib


class TelecomEnv(gym.Env):
    """
    Environnement OpenAI Gym pour le probleme de télécom

    Décris l'environnement
    contient Steiner Node, target node et les clients
    contient les coûts de liaison de chaque poste
    contient la fonction qui calcule le cout total de construction

    Attributs :
        - steiners : numpy array d'un nb fixé de couple, décrivant une coordonnée
        - target_nodes : numpy array d'un nb fixé de couple, décrivant une coordonnée
        - clients : numpy array d'un nb fixé de couple, décrivant une coordonnée
    """

    # TODO : Render video
    # TODO : init from data excel
    metadata = {'render.modes': ['human']}

    def __init__(self, nb_steiner=6, nb_targetNode=5, nb_clients=8, grid_size=(10, 10)):
        """
        Initialise le Réseau telecom aléatoirement uniformement sur la grille
        Attributs :
            - reseau_telecom : type ReseauTelecom, reseau Telecom que l'on cherche a optimiser


        """
        # random initalization of the telecom network
        self.reseau_telecom = ReseauTelecom(nb_steiner, nb_targetNode, nb_clients, grid_size)

        # Pre calculate cost matrices
        self.C_target_steiner = cout_target_steiner(self.reseau_telecom)
        self.C_steiner = cout_steiner(self.reseau_telecom)

        # Empty solution
        self.solution = Solution.Vide(self.reseau_telecom)

        self.reward_range = (-float('inf'), float("inf"))
        self.action_space = None
        self.observation_space = None

    def step(self, action):
        self.solution = action
        observation = [self.reseau_telecom, self.solution]
        reward = self.cout_total()
        done = True
        info = dict()
        return observation, reward, done, info

    def cout_total(self):
        solution = self.solution
        reseau_telecom = self.reseau_telecom

        # Calcul du cout de connexion target-steiner
        cout_total_connexion_1 = 0
        for target in range(reseau_telecom.nb_target_node):
            # Calcul du nombre de clients connecté
            connexions = solution.Z[:, target]
            nb_connexions = sum(connexions)
            cout_connexion = 0
            for steiner in range(reseau_telecom.nb_steiner):
                cout_connexion += nb_connexions * self.C_target_steiner[target, steiner] * solution.X[target, steiner]
            cout_total_connexion_1 += cout_connexion
        if cout_total_connexion_1 == 0:
            cout_total_connexion_1 = float('inf')

        # Calcul du cout de connexion du ring de steiner
        print(self.solution.Y[0], self.solution.Y[-1])
        cout_total_connexion_2 = self.C_steiner[self.solution.Y[0], self.solution.Y[-1]]

        for i in range(len(self.solution.Y) - 1):
            #print("wqefasdgawger",self.solution.Y[i], self.solution.Y[i + 1])
            cout_total_connexion_2 += self.C_steiner[self.solution.Y[i], self.solution.Y[i + 1]]
        if cout_total_connexion_2 == 0:
            cout_total_connexion_2 = float('inf')
        return bridging_costs(self.solution, self.reseau_telecom) + cout_total_connexion_1 + cout_total_connexion_2

    def reset(self):
        return [self.reseau_telecom, Solution.Vide(self.reseau_telecom)]

    def render(self, mode='human'):
        if mode == 'human' :
            print("Steiners : ", self.reseau_telecom.steiners)
            print("Target Offices :", self.reseau_telecom.target_nodes)
            print("Clients : ", self.reseau_telecom.clients)
            print("Ring :", self.solution.Y)
            print("C_target_steiner : \n", self.solution.X)
            print("C_clients_target \n", self.solution.Z)


    def close(self):
        return


# Cost functions


def distance(x, y):
    s = 0
    for i in range(len(x)):
        s += (x[i] ** 2) + (y[i] ** 2)
    return sqrt(s)


# Calcul des 3 composantes qui composent la fitness function
def cout_steiner(reseau_telecom):
    """
    Calcule les link costs des steiner  nodes aux steiner nodes
    :param reseau_telecom: le réseau télécom pour lequel on calcule les couts
    :return: C = [c_ij] où c_ij est le link cost de i à j
    """
    nb_steiner = reseau_telecom.nb_steiner
    C = np.zeros((nb_steiner, nb_steiner))
    for i in range(nb_steiner):
        for j in range(nb_steiner):
            cout = 0
            steiner_1 = reseau_telecom.steiners[i]
            steiner_2 = reseau_telecom.steiners[j]
            d = distance(steiner_1, steiner_2)
            if d < 1:
                cout = 30
            elif 1 <= d <= 15:
                cout = 125 + d * 1.2
            else:
                cout = 130 + d * 1.5
            C[i, j] = cout

    return C


def cout_target_steiner(reseau_telecom):
    """
    Calcule les link costs des target nodes aux steiner nodes
    :param reseau_telecom: le reseau telecom qui nous interesse
    :return: C = [c_ij] où c_ij est le cout de connection du target node i au steiner node j
    """
    nb_steiner = reseau_telecom.nb_steiner
    nb_target = reseau_telecom.nb_target_node
    C = np.zeros((nb_target, nb_steiner))
    for i in range(nb_target):
        for j in range(nb_steiner):
            cout = 0
            target = reseau_telecom.target_nodes[i]
            steiner = reseau_telecom.steiners[j]
            d = distance(target, steiner)
            if d < 1:
                cout = 30
            elif 1 <= d <= 15:
                cout = 125 + d * 1.2
            else:
                cout = 130 + d * 1.5
            C[i, j] = cout

    return C


def bridging_costs(solution, reseau_telecom):
    # Calcul du nombre de links steiner - target
    nb_bridges = reseau_telecom.nb_clients + 2 * len(solution.Y)
    return nb_bridges * 41 + 82 * len(solution.Y)


if __name__ == '__main__':
    env = TelecomEnv()
    sol1 = Solution(env.reseau_telecom)
    sol2 = Solution(env.reseau_telecom)
    observation1, reward1, done1, info1 = env.step(sol1)
    env.render()
    print('1:' ,reward1)
    observation2, reward2, done2, info2 = env.step(sol2)
    env.render()
    print("2", reward2)
    enfant1, enfant2 = sol1.croisement(sol2)
    _, re3, _, _ = env.step(enfant1)
    env.render()
    print("enafant 1 :" , re3)
    _, re4, _, _ = env.step(enfant2)
    env.render()
    print("enafant 2 :", re4)


