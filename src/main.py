from file import load_data, save_data
from service import (
    initialize_users,
    get_users_data,
    new_register,
    list_records,
    search_record,
    update_record,
    delete_record,
    create_user,          # alias — usado solo en demo inicial
)
from menu import (
    show_main_menu,
    prompt_new_user,
    prompt_search,
    prompt_update,
    prompt_delete,
    print_result,
)


def main():
    # Cargar datos persistidos e inicializar en memoria
    loaded_records = load_data()
    initialize_users(loaded_records)

    # Crear usuario demo si la base está vacía
    if not loaded_records:
        create_user("1", "Usuario Demo", "demo@correo.com", "20", "Activo")

    print("Sistema listo")
    print_result(True, list_records())

    while True:
        show_main_menu()

        try:
            option = input("Elige una opción: ").strip()
        except KeyboardInterrupt:
            print("\n\nPrograma interrumpido. ¡Hasta luego!")
            save_data(get_users_data())
            break

        if option == "1":
            args = prompt_new_user()
            ok, msg = new_register(*args)
            print_result(ok, msg)
            if ok:
                save_data(get_users_data())

        elif option == "2":
            print("\n-- Usuarios registrados --")
            result = list_records()
            if not result:
                print("No hay usuarios registrados aún.")
            else:
                print_result(True, result)

        elif option == "3":
            field, value = prompt_search()
            ok, result = search_record(field, value)
            print_result(ok, result)

        elif option == "4":
            id_input, name, email, age, status = prompt_update()
            ok, msg = update_record(id_input, name, email, age, status)
            print_result(ok, msg)
            if ok:
                save_data(get_users_data())

        elif option == "5":
            id_input = prompt_delete()
            ok, msg = delete_record(id_input)
            print_result(ok, msg)
            if ok:
                save_data(get_users_data())

        elif option == "0":
            save_data(get_users_data())
            print("\n¡Hasta luego!")
            break

        else:
            print("\nOpción no válida. Intenta de nuevo.")


if __name__ == "__main__":
    main()