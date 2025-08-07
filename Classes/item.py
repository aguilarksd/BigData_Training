# item.py

class Item:
    """
    Represents an item available in the store.
    """
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    def is_in_stock(self):
        """
        Returns True if the item is in stock, False otherwise.
        """
        return self.quantity > 0

    def reduce_quantity(self, amount):
        """
        Reduces the item's quantity by the specified amount.
        """
        if self.quantity >= amount:
            self.quantity -= amount
            return True
        return False