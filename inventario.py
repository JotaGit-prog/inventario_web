
# Sistema básico de inventario

productos = []

def registrar_producto():
    print("\n--- Registrar producto ---")

    nombre = input("Nombre del producto: ").strip()

    if not nombre:
        print("El nombre no puede estar vacío.")
        return

    try:
        cantidad = int(input("Cantidad disponible: "))
        precio = float(input("Precio unitario: ").replace(",", "."))

        if cantidad < 0 or precio < 0:
            print("La cantidad y el precio no pueden ser negativos.")
            return

    except ValueError:
        print("Ingresa una cantidad y un precio válidos.")
        return

    producto = {
        "nombre": nombre,
        "cantidad": cantidad,
        "precio": precio
    }

    productos.append(producto)
    print("Producto registrado correctamente.")


def consultar_inventario():
    print("\n--- Inventario actual ---")

    if not productos:
        print("Todavía no hay productos registrados.")
        return

    for producto in productos:
        print(
            f"Producto: {producto['nombre']} | "
            f"Cantidad: {producto['cantidad']} | "
            f"Precio: ${producto['precio']:.2f}"
        )


def menu():
    while True:
        print("\n===== SISTEMA DE INVENTARIO =====")
        print("1. Registrar producto")
        print("2. Consultar inventario")
        print("3. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            registrar_producto()
        elif opcion == "2":
            consultar_inventario()
        elif opcion == "3":
            print("Programa finalizado.")
            break
        else:
            print("Opción no válida. Intenta nuevamente.")


if __name__ == "__main__":
    menu()