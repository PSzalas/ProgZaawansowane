def mergeListsAndPowerValues(list1: list, list2: list) -> list:
    mergedList = list(set(list1 + list2))

    resultList = [x ** 3 for x in mergedList]

    return resultList


list1 = [1, 2, 3, 4]
list2 = [3, 4, 5, 6]

result = mergeListsAndPowerValues(list1, list2)

print(result)
