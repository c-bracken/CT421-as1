def fitness(array, binMaxCapacity):
    numBins = 0
    binCapacity = 0

    for i in array:
        binCapacity += i
        if(binCapacity > binMaxCapacity):
            numBins += 1
            binCapacity = i

    return numBins