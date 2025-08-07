# models/store.py
# Note: You'll need to import Item from the same directory here.
from .item import Item


class Store:
    """
    Manages the store's inventory and related business rules.
    """

    def __init__(self):
        # Initialize inventory with Item objects
        self.inventory = {
            'apple': Item('apple', 20.00, 50),
            'banana': Item('banana', 5.00, 100),
            'milk': Item('milk', 60.00, 20),
            'bread': Item('bread', 40.00, 30),
            'eggs': Item('eggs', 10.00, 120),
            'chicken': Item('chicken', 150.00, 10),
            'rice': Item('rice', 80.00, 25)
        }

    def get_inventory_items(self):
        """
        Returns a list of all item objects in the inventory.
        """
        return list(self.inventory.values())

    def get_item(self, item_name):
        """
        Returns an Item object by name, or None if not found.
        """
        return self.inventory.get(item_name)

    def calculate_delivery_charge(self, distance):
        """
        Calculates delivery charges based on distance.
        Returns the charge or None if delivery is not available.
        """
        if 0 <= distance <= 15:
            return 50
        elif 15 < distance <= 30:
            return 100
        else:
            return None  # No delivery available
