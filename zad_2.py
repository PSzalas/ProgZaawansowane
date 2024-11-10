def numbers_function(listOfNumbers):
    for i, number in enumerate(listOfNumbers):
        listOfNumbers[i] = number*2

    return listOfNumbers


def numbers_function2(listOfNumbers):

    return [number * 2 for number in listOfNumbers]


listOfNumbers2 = [1, 2, 3, 4, 5]
listOfNumbers3 = [1, 2, 3, 4, 5]
returnedValue = numbers_function(listOfNumbers2)
returnedValue2 = numbers_function2(listOfNumbers3)
print(returnedValue)
print(returnedValue2)
