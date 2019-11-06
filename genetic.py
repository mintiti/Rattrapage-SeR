# Coeur de l'algortihme genetique
# Schéma de fonctionnement :
#   Initilisation
#       |
#   Evaluer fitness <--------------------------------
#       |                                           |
# | Condition d'arret ?                             |
# |     | si non                                    |
# | Selection des procréateurs-----> crossover -->mutation
# |
# -----> si oui output


# IMPORTS
from Agents import Solution
import Environnement
from config import cfg
import Cout

# CONSTANTS
POPULATION_SIZE = cfg['population_size']
MUTATION_PROBABILITY = cfg['mutation_probability']
CROSSOVER_CHANCE = cfg['crossover_probability']
LOOKBACK = cfg['lookback']
EPSILON = cfg['epsilon']

# Variables
score_history = []


# functions
def average(list):
    return sum(list) / len(list)

def stop(score_history, new_score):
    """

    :param score_history: l'historique des scores
    :param new_score: le meilleur score de la derniere itération
    :return: boolean qui indique si la condition d'arrêt est remplie
    """
    if LOOKBACK > len(score_history):
        mean = average(score_history)
        score_history.append(new_score)
        return abs(new_score - mean) < EPSILON

    else:
        mean = average(score_history[-100:])
        score_history.append(new_score)
        return abs(new_score - mean) < EPSILON


#TODO : creer fonctiobn de crossover
#TODO : creer fonctiobn de mutation
#TODO : creer fonctiobn de selection
#TODO : ecrire boucle de recherche
class Genetic:
    #Class used for running a Genetic metaheuristic search on a given environment

    def __init__(self):
        # Initialise un jeu aléatoire
        self.reseau_telecom = Environnement.ReseauTelecom()
        self.agents_list = [Solution(reseau_telecom) for i in range(POPULATION_SIZE)]

        #Calcule les linking costs
        self.steiner_steiner_costs = Cout.cout_steiner(reseau_telecom)
        self.target_steiner_costs = Cout.cout_target_steiner(reseau_telecom)



if __name__ == '__main__':

    # Initialisaton environnement
    reseau_telecom = Environnement.ReseauTelecom()

    # Initialisation aléatoire de la population initiale
    agents_list = [Solution(reseau_telecom) for i in range(POPULATION_SIZE)]
