class Brewery:
    def __init__(self, data):
        for key, value in data.items():
            setattr(self, key, value)

    def __str__(self):
        return (f"Brewery ID: {getattr(self, 'id', 'brak')}\n"
                f"Name: {getattr(self, 'name', 'brak')}\n"
                f"Type: {getattr(self, 'brewery_type', 'brak')}\n"
                f"Street: {getattr(self, 'street', 'brak')}\n"
                f"City: {getattr(self, 'city', 'brak')}\n"
                f"State: {getattr(self, 'state', 'brak')}\n"
                f"Postal Code: {getattr(self, 'postal_code', 'brak')}\n"
                f"Country: {getattr(self, 'country', 'brak')}\n"
                f"Phone: {getattr(self, 'phone', 'brak')}\n"
                f"Website: {getattr(self, 'website_url', 'brak')}\n")
