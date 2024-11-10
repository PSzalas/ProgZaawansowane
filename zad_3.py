def printEven(listOfNumbers):
    even = [number for number in listOfNumbers if number % 2 == 0]
    print("Even:", even)


list = list(range(1, 11))
printEven(list)
