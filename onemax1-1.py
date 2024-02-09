import random

# Number of individuals in the population
population = 20
# Length of each string
length = 30
# Number of elite individuals to be in each generation
elites = 5
# List to store population strings
popList = []
# List to store fitnesses with corresponding strong
fitnessList = []

# GA hyperparameters
crossover_rate = 0.6
mutation_rate = 0.1

# Calculates fitness for every string in population
def calculate_fitnesses(strings):
    for i in range(population):
        fitnessList[i] = calc_fitness(strings[i])

# Calculates fitness of individual strings
def calc_fitness(string):
    fit = 0
    for i in range(length):
        if string[i] == "1":
            fit += 1
    return fit

# Average fitness of a population
def fitness_avg():
    fit_total = 0
    for i in fitnessList:
        fit_total += i
    return fit_total / population

# Performs mutations in a string
def mutate(string):
    for i in range(length):
        if random.random() < mutation_rate:
            if string[i] == "1":
                string = string[:i] + "0" + string[(i + 1):]
            else:
                string = string[:i] + "1" + string[(i + 1):]
    return string

# Performs crossover between two parent strings
# Returns two child strings
def crossover(parent1, parent2):
    child1 = parent1
    child2 = parent2
    pivot = 0
    if random.random() < crossover_rate:
        pivot = random.randrange(1, length - 1)
        # Head of parent1, tail of parent 2
        child1 = parent1[:pivot] + parent2[pivot:]
        # Head of parent2, tail of parent 1
        child2 = parent2[:pivot] + parent1[pivot:]
    return [child1, child2]

# Sort population by fitness
def fitness_sort(strings):
    mockpop = list(range(population))
    for i in range(population):
        mockpop[i] = [mockpop[i], fitnessList[i ]]
    mockpop.sort(key=fitsort)
    return mockpop

# Return fitness value to sort by
def fitsort(e):
    return e[1]

# Generate new population from elite individuals
# Performs crossover, mutation
def generate_new_pop(strings):
    newpop = []
    elite_strs = fitness_sort(strings)[int(-elites):]
    for i in range(elites):
        elite_strs[i] = strings[elite_strs[i][0]]
    for i in range(elites):
        newpop += crossover(elite_strs[i], elite_strs[(i + 1) % elites])
        newpop += crossover(elite_strs[i], elite_strs[(i + 2) % elites])
    for i in range(population):
        newpop[i] = mutate(newpop[i])
    calculate_fitnesses(newpop)
    return newpop

# Generates starting population
for i in range(population):
    bitstr = ""
    for j in range(length):
        char = random.randint(0, 1)
        bitstr += "{}".format(char)
    popList.append(bitstr)
    
    fitnessList.append(0)

calculate_fitnesses(popList)
averages = open("onemax_averages_1.csv", "w")
averages.write("generation,average\n")

# Write metrics for first generation
generations = 0
metrics = [generations, fitness_avg()]
averages.write("{},{}\n".format(metrics[0], metrics[1]))
print("generation:\t{}".format(metrics[0]))
print("fitness average:\t{}".format(metrics[1]))

# Writes information about each generation
while True:
    popList = generate_new_pop(popList)
    generations += 1
    metrics = [generations, fitness_avg()]
    averages.write("{},{}\n".format(metrics[0], metrics[1]))
    print("generation:\t{}".format(metrics[0]))
    print("fitness average:\t{}".format(metrics[1]))
    # Best performing string in the population
    champ = fitness_sort(popList)[-1]
    if champ[1] == length:
        print("STRING FOUND: INDEX {}, STRING CODE {}".format(champ[0], popList[champ[0]]))
        break
    else:
        print("NOT DONE")

averages.close()