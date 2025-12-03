
class Product:
    def __init__(self, name, qty):
        self.name = name
        self.qty = qty



class Inventory(Product):
    def __init__(self):
        
        super().__init__("", 0)
        self.products = {}  

  
    def add_product(self):
        name = input("Enter product name: ").strip()
        try:
            qty = int(input("Enter quantity: "))
        except ValueError:
            print("Invalid quantity!")
            return

        if name in self.products:
            self.products[name].qty += qty
        else:
            self.products[name] = Product(name, qty)
        print(f"Product '{name}' added/updated successfully!")

  
    def update_stock(self):
        name = input("Enter product name to update: ").strip()
        if name not in self.products:
            print(f"Product '{name}' does not exist!")
            return
        try:
            qty = int(input("Enter new quantity: "))
        except ValueError:
            print("Invalid quantity!")
            return
        self.products[name].qty = qty
        print(f"Product '{name}' stock updated to {qty}!")

    
    def show_products(self):
        if not self.products:
            print("No products in inventory!")
            return
        print("\nAll Products:")
        for product in self.products.values():
            print(f"{product.name}: {product.qty}")
        print()

    def low_inventory(self):
        low_items = [p for p in self.products.values() if p.qty < 5]
        if not low_items:
            print("No low inventory products!")
            return
        print("\nLow Inventory Products (<5):")
        for product in low_items:
            print(f"{product.name}: {product.qty}")
        print()


# Main program
def main():
    inventory = Inventory()  

    while True:
        print("=== Inventory Menu ===")
        print("1. Add Product")
        print("2. Update Stock")
        print("3. Show All Products")
        print("4. Show Low Inventory")
        print("5. Exit")

        choice = input("Select an option: ").strip()

        if choice == "1":
            inventory.add_product()
        elif choice == "2":
            inventory.update_stock()
        elif choice == "3":
            inventory.show_products()
        elif choice == "4":
            inventory.low_inventory()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid option!\n")


if __name__ == "__main__":
    main()