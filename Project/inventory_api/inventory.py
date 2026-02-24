import json
from datetime import datetime
from functools import wraps

from models import Electronics, Grocery


def log_action(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with open("actions.log", "a") as f:
            f.write(f"{datetime.now()} -> {func.__name__}\n")
        return func(*args, **kwargs)
    return wrapper


class InventoryIterator:
    def __init__(self, products):
        self._products = products
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self._products):
            product = self._products[self._index]
            self._index += 1
            return product
        raise StopIteration


class Inventory:
    def __init__(self, file_name="inventory.json"):
        self.file_name = file_name
        self.products = []
        self.load()

    def __iter__(self):
        return InventoryIterator(self.products)

    def save(self):
        with open(self.file_name, "w") as f:
            json.dump([p.to_dict() for p in self.products], f, indent=4)

    def load(self):
        try:
            with open(self.file_name, "r") as f:
                data = json.load(f)
                for item in data:
                    if item["type"] == "Electronics":
                        p = Electronics(item["name"], item["price"], item["stock"])
                    else:
                        p = Grocery(item["name"], item["price"], item["stock"])
                    self.products.append(p)
        except FileNotFoundError:
            self.products = []

    @log_action
    def add_product(self, product):
        self.products.append(product)
        self.save()

    @log_action
    def remove_product(self, name):
        self.products = [p for p in self.products if p.get_name() != name]
        self.save()

    @log_action
    def update_stock(self, name, stock):
        for p in self.products:
            if p.get_name() == name:
                p.set_stock(stock)
        self.save()

    def search_product(self, name):
        for p in self.products:
            if name.lower() in p.get_name().lower():
                return p
        return None
