
import sqlite3


# Crear o abrir la base de datos
conexion = sqlite3.connect("inventario.db")
cursor = conexion.cursor()

# Crear la tabla si todavía no existe
cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        cantidad INTEGER NOT NULL CHECK(cantidad >= 0),
        precio REAL NOT NULL CHECK(precio >= 0)
    )
""")

conexion.commit()


def registrar_producto():
    print("\n--- REGISTRAR PRODUCTO ---")

    nombre = input("Nombre del producto: ").strip()

    if not nombre:
        print("El nombre es obligatorio.")
        return

    try:
        cantidad = int(input("Cantidad inicial: "))
        precio = float(input("Precio unitario: ").replace(",", "."))

        if cantidad < 0 or precio < 0:
            print("La cantidad y el precio no pueden ser negativos.")
            return

    except ValueError:
        print("Ingresa una cantidad y un precio válidos.")
        return

    cursor.execute(
        """
        INSERT INTO productos (nombre, cantidad, precio)
        VALUES (?, ?, ?)
        """,
        (nombre, cantidad, precio)
    )

    conexion.commit()
    print("Producto registrado correctamente.")


def consultar_inventario():
    print("\n--- INVENTARIO ACTUAL ---")

    cursor.execute(
        "SELECT id, nombre, cantidad, precio FROM productos ORDER BY id"
    )
    productos = cursor.fetchall()

    if not productos:
        print("No hay productos registrados.")
        return

    for producto in productos:
        id_producto, nombre, cantidad, precio = producto

        print(
            f"ID: {id_producto} | "
            f"Producto: {nombre} | "
            f"Cantidad: {cantidad} | "
            f"Precio: ${precio:,.2f}"
        )


def actualizar_existencias():
    print("\n--- ACTUALIZAR EXISTENCIAS ---")

    try:
        id_producto = int(input("ID del producto: "))
        cambio = int(input("Cambio de cantidad (+/-): "))

        cursor.execute(
            "SELECT nombre, cantidad FROM productos WHERE id = ?",
            (id_producto,)
        )
        producto = cursor.fetchone()

        if producto is None:
            print("No existe un producto con ese ID.")
            return

        nombre, cantidad_actual = producto
        nueva_cantidad = cantidad_actual + cambio

        if nueva_cantidad < 0:
            print("No hay existencias suficientes.")
            return

        cursor.execute(
            "UPDATE productos SET cantidad = ? WHERE id = ?",
            (nueva_cantidad, id_producto)
        )
        conexion.commit()

        print(f"Producto: {nombre}")
        print(f"Cantidad anterior: {cantidad_actual}")
        print(f"Nueva cantidad: {nueva_cantidad}")

    except ValueError:
        print("Debes ingresar números enteros válidos.")
        


def eliminar_producto():
    print("\n--- ELIMINAR PRODUCTO ---")

    try:
        id_producto = int(input("ID del producto que deseas eliminar: "))
    except ValueError:
        print("Ingresa un ID válido.")
        return

    cursor.execute(
        "SELECT nombre FROM productos WHERE id = ?",
        (id_producto,)
    )
    producto = cursor.fetchone()

    if producto is None:
        print("No existe un producto con ese ID.")
        return

    confirmacion = input(
        f"¿Seguro que deseas eliminar '{producto[0]}'? (s/n): "
    ).strip().lower()

    if confirmacion == "s":
        cursor.execute(
            "DELETE FROM productos WHERE id = ?",
            (id_producto,)
        )
        conexion.commit()
        print("Producto eliminado correctamente.")
    else:
        print("Operación cancelada.")
        

def cerrar_programa():
    conexion.close()
    print("Base de datos cerrada. ¡Hasta pronto!")



def menu():
    while True:
        print("\n===== SISTEMA DE INVENTARIO =====")
        print("1. Registrar producto")
        print("2. Consultar inventario")
        print("3. Actualizar existencias")
        print("4. Eliminar producto")
        print("5. Salir")

        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            registrar_producto()
        elif opcion == "2":
            consultar_inventario()
        elif opcion == "3":
            actualizar_existencias()
        elif opcion == "4":
            eliminar_producto()
        elif opcion == "5":
            cerrar_programa()
            break
        else:
            print("Opción no válida. Intenta nuevamente.")
       


if __name__ == "__main__":
    try:
        menu()
    finally:
        if conexion:
            conexion.close()