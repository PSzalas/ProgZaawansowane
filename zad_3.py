class Property:
    def __init__(self, area, rooms, price, address):
        self.area = area
        self.rooms = rooms
        self.price = price
        self.address = address

    def __str__(self):
        return (f"Adres nieruchomości: {self.address}\n"
                f"Powierzchnia: {self.area} m2, Liczba pokoi: {self.rooms}, Cena: {self.price} PLN")


class House(Property):
    def __init__(self, area, rooms, price, address, plot):
        super().__init__(area, rooms, price, address)
        self.plot = plot

    def __str__(self):
        return (f"{Property.__str__(self)}\n"
                f"Powierzchnia działki: {self.plot} m2")


class Flat(Property):
    def __init__(self, area, rooms, price, address, floor):
        super().__init__(area, rooms, price, address)
        self.floor = floor

    def __str__(self):
        return (f"{Property.__str__(self)}\n"
                f"Piętro: {self.floor}")


house = House(200, 5, 300000, "Słowackiego 12", 500)
flat = Flat(75, 3, 150000, "Mickiewicza 13/30", 4)

print(house)
print()
print(flat)