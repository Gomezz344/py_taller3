from file import load_data, save_data
from service import create_user, list_users, initialize_users, get_users_data


def show_menu():
    print("\n" + "=" * 40)
    print("       SISTEMA DE GESTIÓN DE USUARIOS")
    print("=" * 40)
    print("  1. Crear usuario")
    print("  2. Listar usuarios")
    print("  0. Salir")
    print("=" * 40)


def request_user():
    print("\n-- Nuevo usuario --")
    id_input = input("ID: ").strip()
    name_input = input("Nombre: ").strip()
    email_input = input("Correo: ").strip()
    age_input = input("Edad: ").strip()
    status_input = input("Estado: ").strip()

    success, message = create_user(id_input, name_input, email_input, age_input, status_input)

    if success:
        print(f"\nOK: {message}")
    else:
        print(f"\nError: {message}")


def show_users():
    print("\n-- Usuarios registrados --")
    summary = list_users()

    if not summary:
        print("No hay usuarios registrados aún.")
    else:
        for line in summary:
            print(" •", line)


def main():
    loaded_records = load_data()
    initialize_users(loaded_records)

    if not loaded_records:
        create_user("1", "Usuario Demo", "demo@correo.com", "20", "Activo")

    print("Sistema listo")
    show_users()

    while True:
        show_menu()

        try:
            option = input("Elige una opción: ").strip()
        except KeyboardInterrupt:
            print("\n\nPrograma interrumpido. ¡Hasta luego!")
            save_data(get_users_data())
            break

        if option == "1":
            request_user()
        elif option == "2":
            show_users()
        elif option == "0":
            save_data(get_users_data())
            print("\n¡Hasta luego!")
            break
        else:
            print("\nOpcion no valida. Intenta de nuevo.")


if __name__ == "__main__":
    main()