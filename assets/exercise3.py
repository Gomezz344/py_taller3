# Ejercicio 3: Menú interactivo con manejo de múltiples excepciones

def dividir(a: float, b: float) -> float:
    if b == 0:
        raise ZeroDivisionError("No se puede dividir entre cero.")
    return a / b


def primera_linea(ruta: str) -> str:
    with open(ruta, "r", encoding="utf-8") as f:
        return f.readline().strip()


def mostrar_menu():
    print("\n===== MENÚ =====")
    print("1. Dividir dos números")
    print("2. Abrir archivo y ver primera línea")
    print("3. Salir")
    print("================")


def ejecutar_opcion(opcion: str) -> bool:
    if opcion == "1":
        a = float(input("  Numerador: "))
        b = float(input("  Denominador: "))
        resultado = dividir(a, b)
        print(f"  Resultado: {resultado:.4f}")

    elif opcion == "2":
        ruta = input("  Ruta del archivo: ")
        linea = primera_linea(ruta)
        print(f"  Primera línea: {linea}")

    elif opcion == "3":
        print("👋 Hasta luego.")
        return False  # señal para salir del bucle

    else:
        print("⚠️  Opción no válida. Elige 1, 2 o 3.")

    return True  # continuar en el menú


# Bucle principal: se repite hasta que el usuario elija salir
continuar = True
while continuar:
    mostrar_menu()
    opcion = input("Selecciona una opción: ").strip()
    try:
        continuar = ejecutar_opcion(opcion)
    except ValueError:
        print("❌ Error: asegúrate de ingresar números válidos.")
    except ZeroDivisionError as e:
        print(f"❌ Error de división: {e}")
    except FileNotFoundError as e:
        print(f"❌ Archivo no encontrado: {e}")
    except Exception as e:
        # Captura cualquier error no previsto para que el programa no se caiga
        print(f"❌ Error inesperado: {type(e).__name__}: {e}")
