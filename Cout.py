# Classe de calcul de coût d'un agent
# contient des fonction de calcul de cout d'un agent

# IMPORTS
import Environnement as env
import Agents
from math import sqrt
import numpy as np


def distance(x, y):
    s = 0
    for i in range(len(x)):
        s += x[i] ^ 2 + y[i] ^ 2
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
    :param reseau_telecom: le reseau reseau_telecom qui nous interesse
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
            C[i,j] = cout

    return C

def bridging_costs(solution, reseau_telecom ) :
    # Calcul du nombre de links steiner - target
    nb_bridges = reseau_telecom.nb_clients + 2 * len(solution.Y)
    return nb_bridges * 41 + 82 * len(solution.Y)

def cout_total(solution, reseau_telecom):
    bridging_cost = bridging_costs(solution, reseau_telecom)
    C_target_steienr = cout_target_steiner(reseau_telecom)


    # Calcul du cout des connexions steinr à end office :
    ## Pour chaque end
    for end_office in range()
    ## Calculer le nombre de clients connectés au end
    ## Multiplier par le cout de la connexion end - steiner



