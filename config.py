"""
Config file for the project
"""

cfg = {
    # Probability for every agent to be mutated after the cross overs
    'mutation_probability': 0.3,
    'population_size': 1000,
    # Crossover percentage parameters
    # Describes respectively how many client and target are to be taken from the other parent
    'client_crossover_percentage' : 0.5,
    'target_crossover_percentage' : 0.5,
    # Proportion of the links between target_steiner to be mutated
    'target_steiner_mutation_proportion' : 0.5,
    'client_target_mutation_proportion' : 0.5,
    # Top X% de la population selectionée pour procreer
    'selected_proportion_of_population' : 0.5
}
