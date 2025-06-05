import random
from datetime import datetime
from numpy import argsort

def g_knapsack_solver(item_weights, item_values, knapsack_weight, population_size, generations, mutation_chance):
    """Approximates knapsack problem's solution using genetic algorithm

    Returns the best chromosome, a list of each generation's best chromosome, 
    and runtime.
    Items are represented through two lists: the weights and values. Additional
    parameters are used to configure the genetic simulation. Each gene refers
    to either accepting or not accepting an item into the knapsack. Chromosomes
    are iterated on using random selection, tournament selected crossover,
    mutation, and fitness-based direct selection.
    """
    start = datetime.now()

    item_amount = len(item_weights)
    highest_values = []
    population = []

    def create_population(population, size):
        """Initialise a new random population
        
        Each gene is equally likely to be a 1 or 0
        """
        population = []
        #could be rewritten to generate empty chromosomes and use mutate() on each of them?
        #current approach struggles where knapsack weight capacity is too low and there are many items
        #as possibly all chromosomes end up over the weight limit.
        for i in range(size):
            genes = [0,1]
            chromosome = []
            for j in range(item_amount):
                chromosome.append(random.choice(genes))
            population.append(chromosome)
        
        return population

    def fitness_checker(chromosome):
        """Finds the value of a chromosome's solution, returns 0 if over weight"""
        weight = 0
        value = 0

        for i in range(item_amount-1):
            if chromosome[i] == 1:
                weight += item_weights[i]
                value += item_values[i]
        if weight <= knapsack_weight:
            return value
        return 0
    
    def tournament_selector(population):
        """Picks the fitter of two randomly selected chromosomes"""
        #selects two random, unique chromosome indeces
        chosen_indeces = []
        while len(chosen_indeces) < 2:#technically implementation has O(infinity) time complexity, should be refactored
            random_index = random.randint(0,population_size-1)
            if random_index in chosen_indeces:
                continue
            else:
                chosen_indeces.append(random_index)
        
        
        chromosome1 = population[chosen_indeces[0]]
        chromosome2 = population[chosen_indeces[1]]

        #returns fittest of selected chromosomes
        if fitness_checker(chromosome1) < fitness_checker(chromosome2):
            return chromosome2
        else:
            return chromosome1
    
    def crossover(parent1, parent2):
        """Creates two new chromosomes by splitting two parent chromosomes"""
        crossover_point = random.randint(0,item_amount-1)
        child1 = parent1[0:crossover_point] + parent2[crossover_point:]
        child2 = parent2[0:crossover_point] + parent1[crossover_point:]

        return child1, child2
    
    def mutate(chromosome):
        """Creates a new chromosome, where each gene has a chance to be swapped"""
        for i in range(item_amount):
            if random.random() < mutation_chance:
                if chromosome[i] == 1:
                    chromosome[i] = 0
                else:
                    chromosome[i] = 1
        return chromosome
    
    def get_best_chromosome(population):
        """Finds the fittest chromosome from the population"""
        fitness_values = []

        for chromosome in population:
            fitness_values.append(fitness_checker(chromosome))
        
        max_value = max(fitness_values)
        best_chromosome = fitness_values.index(max_value)
        return population[best_chromosome]
    
    def get_lightest_item_index():
        """Finds which item has the lowest weight"""
        temp_weights = item_weights
        weight_indeces = argsort(temp_weights).tolist()#inefficient, but used rarely
        return weight_indeces[0]
    
    population = create_population(population, population_size)
    best_chromosome_of_generation = [0] * item_amount
    best_chromosome_ever_found = [0] * item_amount

    #main loop to iterate on generations
    for j in range(generations):
        best_chromosome_ever_found = best_chromosome_ever_found.copy()
        new_population = []

        #mutate population
        for i in range(population_size):
            population[i] = mutate(population[i])

        #finds fit parent chromosomes for reproduction
        parents = []
        for i in range(int(population_size/2)):
            parents.append(tournament_selector(population))
        
        #generates portion of new population through crossover
        children = []
        for i in range(int(len(parents)/2)):
            if parents[i] == parents[i+1]:
                break

            child1, child2 = crossover(parents[i], parents[i+1])
            children.append(child1)
            children.append(child2)
        
        for child in children:
            new_population.append(child)

        #generates rest of new population randomly from old, mutated population
        for i in range(population_size-len(children)):
            new_population.append(population[i])

        best_chromosome_of_generation = get_best_chromosome(population)

        #ensures at least one chromosome has some fitness, to allow evolutionary development
        if fitness_checker(best_chromosome_of_generation) == 0:
            new_population = population[:-1]
            minimum_chromosome = [0] * item_amount
            minimum_chromosome[get_lightest_item_index()] = 1

            new_population.append(minimum_chromosome)
            best_chromosome_of_generation = minimum_chromosome



        highest_value_of_generation = fitness_checker(best_chromosome_of_generation)

        if highest_value_of_generation > fitness_checker(best_chromosome_ever_found):
            best_chromosome_ever_found = best_chromosome_of_generation

        #records highest values to help track algorithm progress
        highest_values.append(fitness_checker(best_chromosome_of_generation))

        #confirms new population
        population = new_population[:-1]
        #adds the fittest found chromosome to the population 
        #to ensure the fittest chromosomes don't die out
        population.append(best_chromosome_ever_found)
        

    end = datetime.now()
    time_difference = (end - start).total_seconds()
    return best_chromosome_ever_found, highest_values, time_difference