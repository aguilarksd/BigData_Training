# customer.py

class Customer:
    """
    Represents a customer with their details. This is a data container class.
    """
    def __init__(self, name="", address="", distance=0.0):
        self.name = name
        self.address = address
        self.distance = distance