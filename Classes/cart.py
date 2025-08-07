# cart.py

class ShoppingCart:
    """
    Manages the items selected by the customer.
    This class handles the logic of adding items and calculating subtotals.
    """
    def __init__(self):
        # Stores {'item_name': {'item_object': Item, 'quantity_in_cart': int}}
        self.items = {}

    def add_item(self, item_object, quantity):
        """
        Adds a specified quantity of an item to the cart.
        """
        if item_object.name in self.items:
            self.items[item_object.name]['quantity_in_cart'] += quantity
        else:
            self.items[item_object.name] = {'item_object': item_object, 'quantity_in_cart': quantity}

    def calculate_subtotal(self):
        """
        Calculates the total cost of items in the cart before delivery charges.
        """
        subtotal = 0
        for item_name, details in self.items.items():
            item_obj = details['item_object']
            quantity_in_cart = details['quantity_in_cart']
            subtotal += item_obj.price * quantity_in_cart
        return subtotal
