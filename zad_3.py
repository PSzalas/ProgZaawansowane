def isEven(number: int) -> bool:
    return number % 2 == 0


number1 = 10
result = isEven(number1)

if result:
    print("Liczba parzysta")
else:
    print("Liczba nieparzysta")
