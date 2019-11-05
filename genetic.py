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
import Agents
import Environnement
from config import cfg

# CONSTANTS
POPULATION_SIZE = cfg['population_size']
MUTATION_PROBABILITY = cfg['mutation_probability']
CROSSOVER_CHANCE = cfg['crossover_chance']
