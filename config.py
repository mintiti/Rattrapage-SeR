"""
Config file for the project
"""

cfg = {
    # Probability for every agent to be mutated after the cross overs
    'mutation_probability': 0.05,
    # Probability for 2 given parents to be crossed over, else they are simply copied down
    'crossover_probability': 0.8,
    'population_size': 50,
    # How many generations back we look at to be sure taht we have converged
    'lookback' : 100,
    # Delta under which we consider a difference null
    'epsilon' : 10,
    # Crossover percentage parameters
    # Describes respectively how many client and target are to be taken from the other parent
    'client_crossover_percentage' : 0.3,
    'target_crossover_percentage' : 0.3,
    # Proportion of the links between target_steiner to be mutated
    'target_steiner_mutation_proportion' : 0.2,
    'client_target_mutation_proportion' : 0.2
}
