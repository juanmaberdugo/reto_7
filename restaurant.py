from collections import deque, namedtuple
import json

class MenuItem:

    MenuItemInfo = namedtuple("MenuItemInfo", ["name", "price"])
    
    def __init__(self, name, price, category):
        self.name = name
        self.price = price
        self.category = category

    def calculate_price(self, quantity=1):
        return self.price * quantity

    def get_details(self):
        return f"{self.name}: COP {self.price}"


class Beverage(MenuItem):
    def __init__(self, name, price, size, is_carbonated):
        super().__init__(name, price, "Beverage")
        self.__size = size
        self.__is_carbonated = "Si" if is_carbonated else "No"

    def get_size(self):
        return self.__size

    def set_size(self, size):
        self.__size = size

    def get_is_carbonated(self):
        return self.__is_carbonated

    def set_is_carbonated(self, is_carbonated):
        self.__is_carbonated = "Sí" if is_carbonated else "No"

    def get_details(self):
        return (
            f"{super().get_details()}, Tamaño: {self.get_size()}ml, "
            f"Carbonatada: {self.get_is_carbonated()}"
        )

class Beverage(MenuItem):
    def __init__(self, name, price, portion_size, has_sauces):
        super().__init__(name, price, "Appetizer")
        self.__portion_size = portion_size
        self.__has_sauces = "Si" if has_sauces else "No"

    def get_portion_size(self):
        return self.__portion_size

    def set_portion_size(self, portion_size):
        self.__portion_size = portion_size

    def get_has_sauces(self):
        return self.__has_sauces

    def set_has_sauces(self, has_sauces):
        self.__has_sauces = "Si" if has_sauces else "No"

    def get_details(self):
        return (
            f"{super().get_details()}, Porcion: {self.get_portion_size()}, "
            f"Con salsas: {self.get_has_sauces()}"
        )


class Appetizer(MenuItem):
    def __init__(self, name, price, portion_size, has_sauces):
        super().__init__(name, price, "Appetizer")
        self.__portion_size = portion_size
        self.__has_sauces = "Si" if has_sauces else "No"

    def get_details(self):
        return f"{super().get_details()}, Porcion: {self.__portion_size}, Con salsas: {self.__has_sauces}"

class MainCourse(MenuItem):
    def __init__(self, name, price, origin, cooking_time):
        super().__init__(name, price, "MainCourse")
        self.__origin = origin
        self.__cooking_time = cooking_time

    def get_origin(self):
        return self.__origin

    def set_origin(self, origin):
        self.__origin = origin

    def get_cooking_time(self):
        return self.__cooking_time

    def set_cooking_time(self, cooking_time):
        self.__cooking_time = cooking_time

    def get_details(self):
        return (
            f"{super().get_details()}, Origen: {self.get_origin()}, "
            f"Tiempo de preparacion: {self.get_cooking_time()} min"
        )


class Order:
    def __init__(self):
        self.items = []
        self.has_main_course = False

    def add_item(self, menu_item, quantity=1):
        self.items.append((menu_item, quantity))
        if menu_item.category == "MainCourse":
            self.has_main_course = True

    def calculate_total(self):
            total = 0
            for item, quantity in self.items:
                if self.has_main_course and item.category == "Beverage":
                    total += item.calculate_price(quantity) * 0.8
                else:
                    total += item.calculate_price(quantity)
            return total

    def get_order_details(self):
        receipt = "Detalles de la Orden:\n"
        for item, quantity in self.items:
            receipt += (
                f"{item.get_details()} x{quantity}: COP {item.calculate_price(quantity)}\n"
            )
        receipt += f"Total: COP {self.calculate_total()}"
        return receipt


class PayThem:
    def __init__(self):
        self.__monto = 0

    def set_monto(self, monto):
        if monto < 0:
            print("El monto no puede ser negativo.")
        self.__monto = monto

    def get_monto(self):
        return self.__monto

    def pagar_con_tarjeta(self, numero, cvv):
        if len(numero) < 4:
            print("El número de tarjeta debe tener al menos 4 dígitos.")
        print(f"Pagando COP {self.__monto} con tarjeta {numero[-4:]}")

    def pagar_en_efectivo(self, monto_entregado):
        if monto_entregado < self.__monto:
            print(f"Fondos insuficientes. Faltan COP {self.__monto - monto_entregado} para completar el pago.")
        else:
            cambio = monto_entregado - self.__monto
            print(f"Pago realizado en efectivo. Cambio: COP {cambio}")


class OrderFIFO:
    def __init__(self):
        self.queue = deque()
    
    def add_order(self, order):
        self.queue.append(order)
    
    def process_order(self):
        if self.queue:
            return self.queue.popleft()
        else:
            print("No hay órdenes pendientes.")
            return None

class JsonManager:
    def __init__(self, filename="menu.json"):
        self.filename = filename
        self.menu = self.load_menu()
    
    def load_menu(self):
        try:
            with open(self.filename, "r") as file:
                menu_data = json.load(file)
                for category in ["Beverage", "Appetizer", "MainCourse"]:
                    if category not in menu_data:
                        menu_data[category] = []
                return menu_data
        except (FileNotFoundError, json.JSONDecodeError):
            return {"Beverage": [], "Appetizer": [], "MainCourse": []}
    
    def save_menu(self):
        with open(self.filename, "w") as file:
            json.dump(self.menu, file, indent=4)
    
    def add_item(self, item):
        category = item.category
        item_info = MenuItem.MenuItemInfo(item.name, item.price)
        item_dict = item_info._asdict()
        
        if item_dict not in self.menu[category]:
            self.menu[category].append(item_dict)
            self.save_menu()
        else:
            print("El elemento ya existe en el menú.")
    
    def update_item(self, category, name, new_price):
        if category in self.menu:
            for item in self.menu[category]:
                if item["name"] == name:
                    item["price"] = new_price
                    self.save_menu()
                    print(f"Elemento {name} actualizado en la categoría {category}.")
                    return
            print("El elemento no existe en el menú.")
        else:
            print("Categoría no válida.")
    
    def delete_item(self, category, name):
        if category in self.menu:
            for item in self.menu[category]:
                if item["name"] == name:
                    self.menu[category].remove(item)
                    self.save_menu()
                    print(f"Elemento {name} eliminado de la categoría {category}.")
                    return
            print("El elemento no existe en el menú.")
        else:
            print("Categoría no válida.")

if __name__ == "__main__":
    menu_manager = JsonManager()
    
    menu_manager.add_item(Beverage("Jugo de Naranja", 5000.00, 300, False))
    menu_manager.add_item(MainCourse("Pizza", 15000.00, "Italia", 20))
    
    menu_manager.update_item("Beverage", "Jugo de Naranja", 5500.00)
    menu_manager.delete_item("MainCourse", "Jugo de Naranja")
    
    print("Menú actualizado en 'menu.json'")

    order1 = Order()
    order1.add_item(Beverage("Coca Cola", 3000.00, 500, True), 2)
    
    order2 = Order()
    order2.add_item(MainCourse("Hamburguesa", 12000.00, "EE.UU", 15), 1)
    
    order_queue = OrderFIFO()
    order_queue.add_order(order1)
    order_queue.add_order(order2)
    
    print("\nProcesando órdenes:")
    processed_order = order_queue.process_order()
    if processed_order:
        print(processed_order.get_order_details())
    
    processed_order = order_queue.process_order()
    if processed_order:
        print(processed_order.get_order_details())
