# main.py

import sys
# Import all necessary classes
from Classes.store import Store
from Classes.cart import ShoppingCart
from Classes.customer import Customer

def display_menu(store):
    """
    Displays the available items, their quantities, and prices.
    """
    print("\n--- Available Items ---")
    print("{:<15} {:<10} {:<10}".format("Item", "Price (Rs)", "Quantity"))
    print("-" * 35)
    for item in store.get_inventory_items():
        print(f"{item.name.capitalize():<15} {item.price:<10.2f} {item.quantity:<10}")
    print("-" * 35)


def get_customer_order(store, cart):
    """
    Allows the customer to select items and quantities, handling stock checks.
    """
    while True:
        item_name_input = input("Enter item name (or 'done' to finish): ").strip().lower()
        if item_name_input == 'done':
            break

        item_obj = store.get_item(item_name_input)
        if item_obj is None:
            print(f"'{item_name_input}' is not a valid item. Please try again.")
            continue

        if not item_obj.is_in_stock():
            print(f"Sorry, '{item_obj.name.capitalize()}' is currently out of stock.")
            continue

        try:
            quantity_requested = int(input(f"Enter quantity for {item_obj.name.capitalize()}: "))
            if quantity_requested <= 0:
                print("Quantity must be a positive number. Please try again.")
                continue
        except ValueError:
            print("Invalid quantity. Please enter a number.")
            continue

        if quantity_requested > item_obj.quantity:
            print(f"Sorry, only {item_obj.quantity} units of '{item_obj.name.capitalize()}' are available.")
            confirm = input("Would you like to purchase the available quantity? (yes/no): ").strip().lower()
            if confirm == 'yes':
                quantity_to_add = item_obj.quantity
            else:
                print("Item not added to cart.")
                continue
        else:
            quantity_to_add = quantity_requested

        # Update inventory and add to cart
        if item_obj.reduce_quantity(quantity_to_add):
            cart.add_item(item_obj, quantity_to_add)
            print(f"{quantity_to_add} x {item_obj.name.capitalize()} added to your cart.")
        else:
            print(f"Failed to add item to cart. Please check available quantity.")


def get_customer_details():
    """
    Collects customer's name, address, and delivery distance from input.
    """
    print("\n--- Customer Details ---")
    name = input("Enter your full name: ").strip()
    address = input("Enter your delivery address: ").strip()
    while True:
        try:
            distance_str = input("Enter delivery distance from store in km: ").strip()
            distance = float(distance_str)
            if distance < 0:
                print("Distance cannot be negative. Please enter a valid distance.")
                continue
            break
        except ValueError:
            print("Invalid distance. Please enter a number.")
    return Customer(name, address, distance)


def generate_bill(cart, customer, delivery_charge):
    """
    Displays the final bill with purchased items, customer details, and total cost.
    """
    print("\n" + "=" * 40)
    print("         --- FINAL BILL ---")
    print("=" * 40)

    print("\nCustomer Details:")
    print(f"Name: {customer.name}")
    print(f"Address: {customer.address}")
    print(f"Delivery Distance: {customer.distance:.1f} km")

    print("\nItems Purchased:")
    print("{:<15} {:<10} {:<10}".format("Item", "Quantity", "Cost (Rs)"))
    print("-" * 35)

    subtotal = cart.calculate_subtotal()
    if not cart.items:
        print("No items purchased.")
    else:
        for item_name, details in cart.items.items():
            item_obj = details['item_object']
            quantity_in_cart = details['quantity_in_cart']
            item_cost = item_obj.price * quantity_in_cart
            print(f"{item_obj.name.capitalize():<15} {quantity_in_cart:<10} {item_cost:<10.2f}")
    print("-" * 35)

    print(f"Subtotal: {subtotal:.2f} Rs")

    if delivery_charge is not None:
        print(f"Delivery Charge: {delivery_charge:.2f} Rs")
        total_bill = subtotal + delivery_charge
    else:
        print("Delivery: Not Available for this distance.")
        total_bill = subtotal

    print("=" * 35)
    print(f"Total Amount: {total_bill:.2f} Rs")
    print("=" * 40)
    print("\nThank you for shopping with us!")


def main():
    """
    Main function to run the shopping cart application.
    """
    store = Store()
    cart = ShoppingCart()

    print("Welcome to our Online Store!")

    display_menu(store)
    get_customer_order(store, cart)

    if not cart.items:
        print("\nNo items were added to the cart. Exiting.")
        sys.exit()

    customer = get_customer_details()
    delivery_cost = store.calculate_delivery_charge(customer.distance)

    generate_bill(cart, customer, delivery_cost)


if __name__ == "__main__":
    main()
