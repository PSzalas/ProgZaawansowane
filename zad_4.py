def everySecondItem(items):
    everySecond = items[::2]
    print("Every second item:", everySecond)

list = list(range(1, 11))
everySecondItem(list)