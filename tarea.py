
import json
import os

class Item:
    def __init__(self, item_id, name, stock, cost):
        # Inicializa los atributos del item
        self.item_id = item_id  # Identificador único del item
        self.name = name  # Nombre del item
        self.stock = stock  # Cantidad disponible en inventario
        self.cost = cost  # Precio del item

    def __repr__(self):
        # Devuelve una representación en texto del item
        return f"ID: {self.item_id}, Nombre: {self.name}, Stock: {self.stock}, Precio: ${self.cost}"


class Inventory:
    def __init__(self, file_name='inventory.json'):
        # Inicializa el inventario como un diccionario y el archivo JSON para almacenamiento
        self.items = {}  # Diccionario para almacenar items
        self.file_name = file_name  # Archivo donde se guarda el inventario
        self.load_inventory()  # Carga los items desde el archivo

    def load_inventory(self):
        # Carga los items desde un archivo JSON
        try:
            if os.path.exists(self.file_name):
                with open(self.file_name, 'r') as file:
                    self.items = json.load(file)
                print("Inventario cargado exitosamente desde el archivo.")
            else:
                print(f"Archivo '{self.file_name}' no encontrado. Se creará uno nuevo al guardar.")
        except FileNotFoundError:
            print("Error: Archivo de inventario no encontrado.")
        except json.JSONDecodeError:
            print("Error: Problema al leer el archivo de inventario. Verifique el formato JSON.")

    def save_inventory(self):
        # Guarda los items en un archivo JSON
        try:
            with open(self.file_name, 'w') as file:
                json.dump(self.items, file, indent=4)
            print("Inventario guardado exitosamente en el archivo.")
        except Exception as e:
            print(f"Error al guardar el inventario: {e}")

    def add_item(self, item):
        # Añade un nuevo item al inventario
        if item.item_id in self.items:
            print("Error: Ya existe un item con ese ID.")
        else:
            self.items[item.item_id] = item.__dict__
            print("Item añadido exitosamente.")
            self.save_inventory()  # Guarda el inventario después de añadir el item

    def remove_item(self, item_id):
        # Elimina un item del inventario por su ID
        if item_id in self.items:
            del self.items[item_id]
            print(f"Item {item_id} eliminado exitosamente.")
            self.save_inventory()  # Guarda el inventario después de eliminar el item
        else:
            print("Error: Item no encontrado.")

    def update_item(self, item_id, stock=None, cost=None):
        # Actualiza el stock o el precio de un item por su ID
        if item_id in self.items:
            if stock is not None:
                self.items[item_id]['stock'] = stock
            if cost is not None:
                self.items[item_id]['cost'] = cost
            print(f"Item {item_id} actualizado exitosamente.")
            self.save_inventory()  # Guarda el inventario después de actualizar el item
        else:
            print("Error: Item no encontrado.")

    def search_item(self, name):
        # Busca items por nombre
        results = [Item(item_id, details['name'], details['stock'], details['cost'])
                   for item_id, details in self.items.items()
                   if name.lower() in details['name'].lower()]
        if results:
            for item in results:
                print(item)
        else:
            print("No se encontraron items con ese nombre.")

    def display_inventory(self):
        # Muestra todos los items en el inventario
        if self.items:
            for item_id, details in self.items.items():
                item = Item(item_id, details['name'], details['stock'], details['cost'])
                print(item)
        else:
            print("El inventario está vacío.")


def menu():
    # Inicializa el inventario con el archivo JSON
    inventory = Inventory()

    while True:
        print("\nSistema de Gestión de Inventarios")
        print("1. Añadir nuevo item")
        print("2. Eliminar item por ID")
        print("3. Actualizar stock o precio de un item")
        print("4. Buscar item(s) por nombre")
        print("5. Mostrar todos los items")
        print("6. Guardar y Salir")

        choice = input("Seleccione una opción: ")

        if choice == '1':
            item_id = input("Ingrese el ID del item: ")
            name = input("Ingrese el nombre del item: ")
            stock = int(input("Ingrese la cantidad en stock: "))
            cost = float(input("Ingrese el precio: "))
            item = Item(item_id, name, stock, cost)
            inventory.add_item(item)

        elif choice == '2':
            item_id = input("Ingrese el ID del item a eliminar: ")
            inventory.remove_item(item_id)

        elif choice == '3':
            item_id = input("Ingrese el ID del item a actualizar: ")
            stock = input("Ingrese el nuevo stock (o presione Enter para no cambiarlo): ")
            cost = input("Ingrese el nuevo precio (o presione Enter para no cambiarlo): ")
            stock = int(stock) if stock else None
            cost = float(cost) if cost else None
            inventory.update_item(item_id, stock, cost)

        elif choice == '4':
            name = input("Ingrese el nombre del item a buscar: ")
            inventory.search_item(name)

        elif choice == '5':
            inventory.display_inventory()

        elif choice == '6':
            inventory.save_inventory()
            print("Inventario guardado. Saliendo del sistema...")
            break

        else:
            print("Opción no válida. Intente de nuevo.")


# Ejecuta el menú si se ejecuta como script principal
if __name__ == "__main__":
    menu()
