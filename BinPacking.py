import random

def fitness(array, binMaxCapacity):
    numBins = 0
    binCapacity = 0

    for i in array:
        binCapacity += i
        if(binCapacity > binMaxCapacity):
            numBins += 1
            binCapacity = i

    return numBins

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

def crossover(parent1, parent2):
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
    return [child1, child2]

# Return the weight of a [weight, frequency] list for sorting
def weight_frequency_sort(e):
    return e[0]

# Check if a given permutation contains the correct frequency of each item weight
def check_correctness(frequencies, items):
    for i in frequencies:
        actual = 0
        expected = i[1]
        for j in items:
            if i[0] == j:
                actual += 1
        if actual != expected:
            print("Expected {} '{}'s, found {}".format(expected, i[0], actual))
            return False
    return True

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

    for i in range(population):
        if check_correctness(task["items"], solutions[i]) == False:
            print("Incorrect solution found: solution {} for task {}".format(i, task["name"]))
            return
    print("All solutions for task {} are correct".format(task["name"]))

    mutants = []
    mutantCount = 0
    for i in range(population):
        # create mutant
        mutants.append(mutate(solutions[i]))
        if check_correctness(task["items"], mutants[i]) == False:
            print("Incorrect mutant generated: mutant {} for task {}".format(i, task["name"]))
            return
        if (mutants[i] == solutions[i]) == False:
            print("Mutant created from solution {}".format(i))
            mutantCount += 1
    print("Correctly generated a mutant population for task {}, with {} solutions mutated in at least one position".format(task["name"], mutantCount))

# Read in bin data
bin_data = open("./Binpacking.txt", "r")
offset = 17
tasks = 4

# List of task templates filled with task data
task_list = []

# GA hyperparameters
population = 20

mutation_rate = 0.005

crossover_rate = 0.5

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
        "item_count": 0
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
    # Print task summary
    print("Total items: {}\nTotal weight: {}\nItems: {}\n".format(item_sum, weight_sum, task_t["items"]))

    # Add task to list of tasks
    task_list.append(task_t)

# No more data to read from file; close file
bin_data.close()

# Iterate through each task and find a solution
for i in task_list:
    print("Finding solution for task {}...".format(i["name"]))
    solve(i)
