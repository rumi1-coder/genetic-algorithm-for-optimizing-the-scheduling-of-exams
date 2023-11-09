import random

# Define the parameters of the problem
N = 10  # number of courses
K = 3  # number of exam halls
time_slots = 5  # number of available time slots per day
hours_per_day = 3  # number of hours each exam hall can be used per day
conflicting_pairs = [(0, 1), (2, 3)]  # pairs of courses with conflicting students


def fitness(schedule):
    # Calculate the fitness of a schedule by counting the number of conflicts
    conflicts = 0
    for pair in conflicting_pairs:
        if schedule[pair[0]] == schedule[pair[1]]:
            conflicts += 1
    return 1 / (conflicts + 1)


def crossover(parent1, parent2):
    # Perform one-point crossover between two parents
    crossover_point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2


def mutate(schedule, mutation_rate):
    # Mutate a schedule by flipping bits with a certain probability
    for i in range(len(schedule)):
        if random.random() < mutation_rate:
            schedule[i] = 1 - schedule[i]
    return schedule


def genetic_algorithm(population_size, mutation_rate, generations):
    # Initialize a random population of schedules
    population = []
    for i in range(population_size):
        schedule = [random.randint(0, time_slots - 1) for j in range(N)]
        population.append(schedule)

    # Evolve the population for a certain number of generations
    for i in range(generations):
        # Evaluate the fitness of each schedule
        fitness_scores = [fitness(schedule) for schedule in population]

        # Select parents for crossover using tournament selection
        parents = []
        for j in range(population_size):
            tournament = random.sample(range(population_size), K)
            tournament_fitnesses = [fitness_scores[k] for k in tournament]
            winner = tournament[tournament_fitnesses.index(max(tournament_fitnesses))]
            parents.append(population[winner])

        # Perform crossover and mutation to create a new generation of schedules
        children = []
        for j in range(population_size // 2):
            parent1 = parents[j]
            parent2 = parents[j + 1]
            child1, child2 = crossover(parent1, parent2)
            child1 = mutate(child1, mutation_rate)
            child2 = mutate(child2, mutation_rate)
            children.append(child1)
            children.append(child2)

        # Replace the old population with the new generation
        population = children

    # Find the best schedule in the final population
    fitness_scores = [fitness(schedule) for schedule in population]
    best_schedule = population[fitness_scores.index(max(fitness_scores))]

    return best_schedule


# Example usage of the genetic_algorithm function
best_schedule = genetic_algorithm(population_size=100, mutation_rate=0.01, generations=100)
print(best_schedule)
