import os
import subprocess
import sys

RUTA_ASSETS = r"C:\Users\sebas\OneDrive\Desktop\py_taller3\assets"

EJERCICIOS = {
    "1": "exercise1.py",
    "2": "exercise2.py",
    "3": "exercise3.py",
    "4": "exercise4.py",
    "5": "exercise5.py",
    "6": "exercise6.py",
}


def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")


def mostrar_menu():
    print("=" * 35)
    print("        MENU DE EJERCICIOS")
    print("=" * 35)
    for num, archivo in EJERCICIOS.items():
        ruta = os.path.join(RUTA_ASSETS, archivo)
        estado = "" if os.path.exists(ruta) else " (no encontrado)"
        print(f"  [{num}] {archivo}{estado}")
    print("  [0] Salir")
    print("=" * 35)


def ejecutar_ejercicio(numero):
    archivo = EJERCICIOS.get(numero)
    if not archivo:
        print("Opcion invalida.")
        return

    ruta = os.path.join(RUTA_ASSETS, archivo)

    if not os.path.exists(ruta):
        print(f"\nError: no se encontro '{ruta}'")
        input("\nPresiona Enter para volver al menu...")
        return

    limpiar_pantalla()
    print(f"--- Ejecutando {archivo} ---\n")

    try:
        subprocess.run([sys.executable, ruta], check=True)
    except subprocess.CalledProcessError as e:
        print(f"\nEl ejercicio termino con error (codigo {e.returncode}).")
    except KeyboardInterrupt:
        print("\nEjecucion interrumpida.")

    input("\nPresiona Enter para volver al menu...")


def main():
    while True:
        limpiar_pantalla()
        mostrar_menu()
        opcion = input("\nElige una opcion: ").strip()

        if opcion == "0":
            limpiar_pantalla()
            print("Hasta luego.")
            break
        elif opcion in EJERCICIOS:
            ejecutar_ejercicio(opcion)
        else:
            input("Opcion no valida. Presiona Enter para continuar...")


if __name__ == "__main__":
    main()