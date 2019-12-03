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
from copy import copy

from Agents import Solution
from config import cfg
from Telecom import TelecomEnvFromExcel
import random as rd
from display import Display
from tqdm import tqdm

# CONSTANTS
POPULATION_SIZE = cfg['population_size']
MUTATION_PROBABILITY = cfg['mutation_probability']
SELECTED_PROPORTION_OF_POPULATION = cfg['selected_proportion_of_population']
SMALL_DATA_INSTANCE = 'InputDataTelecomSmallInstance.xlsx'
LARGE_DATA_INSTANCE = "InputDataTelecomLargeInstance.xlsx"



def selection_procreators(agents_list_with_scores):
    nb_selected = round(len(agents_list_with_scores) * SELECTED_PROPORTION_OF_POPULATION)
    return agents_list_with_scores[:nb_selected]

class Genetic :
    "Class doing the purely evolutive stuff "
    def __init__(self,data_instance):
        """
        Initializes and evaluates the first generation's scores
        :param data_instance: the data instance toi work on
        """
        self.generation_counter = 0
        self.reseau_telecom = TelecomEnvFromExcel(data_instance)
        self.population = [Solution(self.reseau_telecom.reseau_telecom) for i in range(POPULATION_SIZE)]
        self.population_with_scores = []
        for sol in self.population:
            observation, reward, done, info = self.reseau_telecom.step(sol)
            self.population_with_scores.append((sol,reward))
        self.population_with_scores.sort(key= sort_by_score)
        self.best_scores_history = []
        self.current_best = None
        self.current_best_list = []

    def selection(self):
        procreators_with_scores =selection_procreators(self.population_with_scores)
        self.population = [individual_with_score[0] for individual_with_score in procreators_with_scores]
    # TODO : maybe skew the crossover towards the best scoring parents
    def crossover(self):
        procreators = self.population.copy()
        while len(self.population) < POPULATION_SIZE:
            # Select the parents
            [index1, index2] = rd.sample(range(len(procreators)), 2)
            # Cross them over
            enfant1, enfant2 = procreators[index1].croisement(procreators[index2])
            # Add them to the population
            self.population.append(enfant1)
            self.population.append(enfant2)

    def mutate(self):
        for individual in self.population:
            individual.mutation()

    def evaluate(self):
        self.population_with_scores = []
        #evaluate the population
        for individual in self.population:
            _, reward, _, _ = self.reseau_telecom.step(individual)
            self.population_with_scores.append((individual, reward))
        # Sort the population
        self.population_with_scores.sort(key = sort_by_score)
        #update the best score history and current best
        generations_best = self.population_with_scores[0]
        self.current_best_list.append(generations_best)
        self.best_scores_history.append(generations_best)
        if self.current_best == None :
            self.current_best = generations_best
        elif generations_best[1] < self.current_best[1] :
            self.current_best = generations_best
        self.generation_counter += 1

    def render(self):
        print("""Current generation : {0}
Current best score : {1}
Best score history : {2}
Best solution found :
    Steiner cycle : {3}
    Target to steiner connections : {4}
    Client to target connection : {5}
        """.format(self.generation_counter,
                   self.current_best[1],
                   [self.best_scores_history[i][1] for i in range(len(self.best_scores_history))],
                   self.current_best[0].Y,
                   self.current_best[0].X,
                   self.current_best[0].Z))

    def render_final(self):
        print("""Ended at generation {0}
Best score obtained : {1}
Best solution found :
    Steiner cycle : {2}
    Target to steiner connections : {3}
    Client to target connection : {4}
        """.format(self.generation_counter,
                   self.current_best[1],
                   self.current_best[0].Y,
                   self.current_best[0].X,
                   self.current_best[0].Z))
    @classmethod
    def render_initial(self):
        print( 'Initializing the problem with parameters ', cfg)




#TODO : creer fonctiobn de crossover
#TODO : creer fonctiobn de mutation
#TODO : creer fonctiobn de selection
#TODO : ecrire boucle de recherche

def sort_by_score(tuple):
    return tuple[1]


if __name__ == '__main__':
    genetic = None
    # Chose data instance
    data_key = input("Hi, welcome to the genetic algorithm for the Telecom network problem \n" + "To test the algorithm on the small data instance type 'S' \n"+ "For the large data instance, type 'L'\n")
    data_key = data_key.lower()
    ok_input = False
    while not ok_input:
        if data_key == 's' :
            Genetic.render_initial()
            genetic = Genetic(SMALL_DATA_INSTANCE)
            ok_input = True
        elif data_key == 'l':
            genetic = Genetic(LARGE_DATA_INSTANCE)
            genetic.render_initial()
            ok_input = True
        else :
            data_key = input("Wrong Key\n"+  "To test the algorithm on the small data instance type 'S' \n"+ "For the large data instance, type 'L'\n")

    #Initialize the display
    genetic.evaluate()
    genetic.render()
    while True :
        input_key = input("To run one generation, type 'G'\nTo run 100 generations, type 'C'\nTo stop the simulation type 'S' ")
        input_key = input_key.lower()
        if input_key == 's':
            genetic.render_final()
            # Output results to an image
            data_instance = SMALL_DATA_INSTANCE if data_key == 's' else LARGE_DATA_INSTANCE
            figure = Display(genetic,data_instance)
            figure.save("genetic.png")
            break

        elif input_key == 'g' :
            genetic.selection()
            genetic.crossover()
            genetic.mutate()
            genetic.evaluate()
            genetic.render()
        elif input_key == 'c':
            for i in tqdm(range(100), unit= 'generation'):
                #print('s')
                genetic.selection()
                #print('c')
                genetic.crossover()
                #print('m')
                genetic.mutate()
                #print('eval')
                genetic.evaluate()
            genetic.render()
        else :
            input_key = input('Wrong key\n' + "To run one generation, type 'G'\nTo run 100 generations, type 'C'\nTo stop the simulation type 'S' " )



