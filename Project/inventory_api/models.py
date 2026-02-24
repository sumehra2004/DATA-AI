class Product:
    def __init__(self, name, price, stock):
        self.__name = name
        self.__price = price
        self.__stock = stock

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_stock(self):
        return self.__stock

    def set_stock(self, value):
        if value < 0:
            raise ValueError("Stock cannot be negative")
        self.__stock = value

    def to_dict(self):
        return {
            "type": self.__class__.__name__,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock
        }


class Electronics(Product):
    pass


class Grocery(Product):
    pass
