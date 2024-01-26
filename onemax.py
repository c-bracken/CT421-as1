import random

population = 20
length = 30
# should be population / 4
elites = 5
strlist = []
fitnesses = []

crossover_rate = 0.6
mutation_rate = 0.1

def calculate_fitnesses(strings):
    for i in range(population):
        fitnesses[i] = calc_fitness(strings[i])

def calc_fitness(string):
    fit = 0
    for i in range(length):
        if string[i] == "1":
            fit += 1
    return fit

def fitness_avg():
    fit_total = 0
    for i in fitnesses:
        fit_total += i
    return fit_total / population

def mutate(string):
    for i in range(length):
        if random.random() < mutation_rate:
            if string[i] == "1":
                string = string[:i] + "0" + string[(i + 1):]
            else:
                string = string[:i] + "1" + string[(i + 1):]
    return string

def crossover(parent1, parent2):
    child1 = parent1
    child2 = parent2
    pivot = 0
    if random.random() < crossover_rate:
        pivot = random.randrange(1, length - 1)
        child1 = parent1[:pivot] + parent2[pivot:]
        child2 = parent2[:pivot] + parent1[pivot:]
    return [child1, child2]

def fitness_sort(strings):
    mockpop = list(range(population))
    for i in range(population):
        mockpop[i] = [mockpop[i], fitnesses[i]]
    mockpop.sort(key=fitsort)
    return mockpop

def fitsort(e):
    return e[1]

def generate_new_pop(strings):
    newpop = []
    elite_strs = fitness_sort(strings)[-elites:]
    for i in range(elites):
        elite_strs[i] = strings[elite_strs[i][0]]
    for i in range(elites):
        newpop += crossover(elite_strs[i], elite_strs[(i + 1) % elites])
        newpop += crossover(elite_strs[i], elite_strs[(i + 2) % elites])
    print(newpop)
    for i in range(population):
        newpop[i] = mutate(newpop[i])
    calculate_fitnesses(newpop)
    return newpop

for i in range(population):
    bitstr = ""
    for j in range(length):
        char = random.randint(0, 1)
        bitstr += "{}".format(char)
    strlist.append(bitstr)
    
    fitnesses.append(0)
calculate_fitnesses(strlist)

averages = open("onemax_averages.csv", "w")
averages.write("generation,average\n")

generations = 0
while True:
    strlist = generate_new_pop(strlist)
    generations += 1
    metrics = [generations, fitness_avg()]
    averages.write("{},{}\n".format(metrics[0], metrics[1]))
    print("generation:\t{}".format(metrics[0]))
    print("fitness average:\t{}".format(metrics[1]))
    champ = fitness_sort(strlist)[-1]
    if champ[1] == length:
        print("FREAK FOUND: INDEX {}, FREAK CODE {}".format(champ[0], strlist[champ[0]]))
        break
    else:
        print("NOT DONE")
averages.close()