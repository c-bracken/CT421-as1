import random
import math

# Read in bin data
bin_data = open("./Binpacking.txt", "r")
offset = 17
tasks = 4

# List of task templates filled with task data
task_list = []

# GA hyperparameters
population = 20
mutation_rate = 0.3
crossover_rate = 0.2
cycles = 1000
elites = 5

fitnessList = list(range(population))

# Calculate the fitness of a solution
def fitness(array, binMaxCapacity):
    numBins = 0
    binCapacity = 0

    for i in array:
        binCapacity += i
        if(binCapacity > binMaxCapacity):
            numBins += 1
            binCapacity = i

    return numBins

# Generate fitnesses for a population
def gen_fitnesses(popList, task):
    fitnessList = []
    for i in range(population):
        fitnessList.append([popList[i], fitness(popList[i], task["bin_capacity"])])
    return fitnessList

# Sort by fitness
def fitness_sort(popList):
    mockpop = list(range(population))
    for i in range(population):
        mockpop[i] = [popList[i], fitnessList[i]]
    mockpop.sort(key=fitsort)
    return mockpop

# Return fitness value to sort by
def fitsort(e):
    return e[1]

# Mutate a solution
def mutate(solution):
    # Create a copy of the solution to mutate
    mutation = solution.copy()
    for i in range(len(mutation)):
        if random.random() < mutation_rate:
            # Choose position to swap with
            new_position = random.randint(0, len(mutation) - 1)
            # Swap elements
            mutation[i], mutation[new_position] = mutation[new_position], mutation[i]
    return mutation

# Calculate the weights and their given frequencies present in a solution
def calculate_weights(solution):
    sortedWeights = solution.copy()
    sortedWeights.sort(reverse=True)
    current = sortedWeights[0]
    weights = [[current, 1]]
    weightIndex = 0
    for i in range(1, len(solution)):
        if sortedWeights[i] == current:
            weights[weightIndex][1] += 1
        else:
            weightIndex += 1
            current = sortedWeights[i]
            weights.append([sortedWeights[i], 1])
    return weights

# Given a solution and the correct number of weights, return 2 lists of the weights that are in excess and the weights that there are fewer of in the solution
def calculate_weight_diff(source, weights):
    weightsDiff = []
    weightsIndex = 0
    for i in range(len(source)):
        if weightsIndex == len(weights) or source[i][0] > weights[weightsIndex][0]:
            weightsDiff.append([source[i][0], source[i][1]])
        else:
            weightsDiff.append([source[i][0], source[i][1] - weights[weightsIndex][1]])
            weightsIndex += 1

    diff1 = [] # excess
    diff2 = [] # lack
    for i in weightsDiff:
        if i[1] < 0:
            for j in range(-i[1]):
                diff1.append(i[0])
        elif i[1] > 0:
            for j in range(i[1]):
                diff2.append(i[0])
    return diff1, diff2

# Given a solution with a known excess and lack of specific weights, insert the lacking weights back into the solution where there is an excess weight
def correct_weights(solution, excess, lack):
    corrected = solution.copy()
    for i in range(len(excess)):
        for j in range(len(solution)):
            if corrected[j] == excess[i]:
                corrected[j] = lack[i]
                break
    return corrected

# Check if a given solution contains the correct frequency of each item weight
def check_correctness(source, target):
    weights = calculate_weights(target)
    return weights == source

# Perform crossover on two solutions
def crossover(parent1, parent2, task):
    # List manipulation
    child1 = parent1
    child2 = parent2
    pivot = 0
    if random.random() < crossover_rate:
        pivot = random.randint(1, len(parent1) - 1)
        # Head of parent1, tail of parent 2
        child1 = parent1[:pivot] + parent2[pivot:]
        # Head of parent2, tail of parent 1
        child2 = parent2[:pivot] + parent1[pivot:]
    newPop = list(range(2))
    newPop[0], newPop[1] = crossover_correction(child1, child2, task)
    return newPop

# Return the weight of a [weight, frequency] list for sorting
def weight_frequency_sort(e):
    return e[0]

# Given a solution, return the excess and lack of weights
def crossover_correction(cross1, cross2, task):
    w = calculate_weights(cross1)
    excess, lack = calculate_weight_diff(task["items"], w)
    cross1corrected = correct_weights(cross1, excess, lack)
    cross2corrected = correct_weights(cross2, lack, excess)
    return cross1corrected, cross2corrected

# Generate new population from elite individuals
def generate_new_pop(popList, task):
    newpop = []
    elite_strs = fitness_sort(popList)
    elite_strs = elite_strs[int(-elites):]
    for i in range(elites):
        elite_strs[i] = popList[elite_strs[i][1]]
    for i in range(elites):
        newpop += crossover(elite_strs[i], elite_strs[(i + 1) % elites], task)
        newpop += crossover(elite_strs[i], elite_strs[(i + 2) % elites], task)
    for i in range(population):
        newpop[i] = mutate(newpop[i])
    gen_fitnesses(newpop, task)
    return newpop

# Find a solution for the given task
def solve(task):
    solutions = []
    # Generate "default" permutation of item weights
    available_items = task["items"].copy()
    default_perm = []
    for i in available_items:
        for j in range(i[1]):
            default_perm.append(i[0])
    # Generate random starting population of permutations of the weights
    for i in range(population):
        # Set current permutation to a list of 0s
        perm = []
        for j in range(task["item_count"]):
            perm.append(0)
        max_valid_index = task["item_count"] - 1
        # Iterate through "default" permutation, inserting in random indecies
        # If a weight already exists in that index, try the next index
        # Similar to hash table construction
        for j in default_perm:
            index = 0
            if max_valid_index != 0:
                index = random.randint(0, max_valid_index)
            for k in range(task["item_count"]):
                curr_index = (index + k) % task["item_count"]
                if perm[curr_index] == 0:
                    perm[curr_index] = j
                    break
        solutions.append(perm)

    # Error correcting code for verifying population generation, mutation and correction function properly
    # Commented out as it modifies the population
   
    # # Test population generation
    # for i in range(population):
        # if check_correctness(task["items"], solutions[i]) == False:
            # print("Incorrect solution found: solution {} for task {}\n{}".format(i, task["name"], solutions[i]))
            # return
    # print("All solutions for task {} are correct".format(task["name"]))
    #
    # # Test mutation code
    # mutants = []
    # mutantCount = 0
    # for i in range(population):
    #     # create mutant
    #     mutants.append(mutate(solutions[i]))
    #     if check_correctness(task["items"], mutants[i]) == False:
    #
    #         print("Incorrect mutant generated: mutant {} for task {}\n".format(i, task["name"], mutants[i]))
    #         return
    #     if (mutants[i] == solutions[i]) == False:
    #         mutantCount += 1
    # print("Correctly generated a mutant population for task {}, with {} solutions mutated in at least one position".format(task["name"], mutantCount))
    #
    # # Test calculate_weight_diff code
    # for i in range(population):
    #     solnExcess, solnLack = calculate_weight_diff(task["items"], calculate_weights(solutions[i]))
    #     if not (solnExcess == [] and solnLack == []):
    #         print("Incorrect weight differences calculated: solution {} for task {}".format(i, task["name"]))
    #         return
    # print("Correctly calculated weight differences as zero for task {}".format(task["name"]))

    # Open file to write fitness data to
    task_file = open("{}.csv".format(task["name"]), "w")
    task_file.write("generation,fitness\n")

    solution_fitnesses = gen_fitnesses(solutions, task)
    total = 0
    for i in solution_fitnesses:
        total += i[1]
    average = total / population
    task_file.write("0,{}\n".format(average))
    
    for i in range(cycles):
        # Perform crossover, mutation, and error correction
        solutions = generate_new_pop(solutions, task)
        for j in range(population):
            if check_correctness(task["items"], solutions[j]) == False:
                print("Incorrect solution found: solution {} for task {}\n{}".format(j, task["name"], solutions[j]))
                return
        solution_fitnesses = gen_fitnesses(solutions, task)
        total = 0
        for j in solution_fitnesses:
            total += j[1]
        average = total / population
        task_file.write("{},{}\n".format(i + 1, average))

        # Loops until a solution is found
        for j in range(population):
            if solution_fitnesses[j][1] == task["target"]:
                print("Solution found for task {} in {} generations: solution {}\n{}".format(task["name"], i, j, solution_fitnesses[j][0]))
                return
        #print("Average fitness: {}".format(average))
    task_file.close()

# Skip text at the start
for i in range(offset):
    bin_data.readline()

# Read data for each bin-packing task
for i in range(tasks):
    # Task dict for storing task information
    task_t = {
        "name": "task_name",
        "bin_capacity": 0,
        "items": [],
        "item_count": 0,
        "target": 0
    }

    # Read task information, strip whitespace
    name = bin_data.readline().rstrip()
    print("Task: {}".format(name))
    weights = int(bin_data.readline().strip())
    print("Weights: {}".format(weights))
    capacity = int(bin_data.readline().strip())
    print("Bin capacity: {}".format(capacity))
    task_t.update({"name": name, "bin_capacity": capacity})

    # Read in weights and frequencies
    item_sum = 0
    weight_sum = 0
    different_weights = 0
    for j in range(weights):
        [weight, count] = bin_data.readline().rstrip().split()
        weight = int(weight)
        count = int(count)
        item_sum += count
        weight_sum += weight * count
        task_t["items"].append([weight, count])
    task_t["item_count"] = item_sum
    task_t["target"] = math.ceil(weight_sum / capacity)
    # Print task summary
    print("Total items: {}\nTotal weight: {}\nOptimal number of bins: {}\nItems: {}\n".format(item_sum, weight_sum, task_t["target"], task_t["items"]))

    # Add task to list of tasks
    task_list.append(task_t)

# No more data to read from file; close file
bin_data.close()

# Iterate through each task and find a solution
for i in task_list:
    print("Finding solution for task {}...".format(i["name"]))
    solve(i)
