from typing import Tuple, Optional, Any, Union, List
from colorama import Fore, Style, init

from file import load_data
from service import (
    initialize_users,
    new_register,
    list_records,
    search_record,
    update_record,
    delete_record,
    create_user,
)
from integration import generar_registros_falsos

init()

def show_main_menu() -> None:
    """
    Imprime el menú principal de la aplicación.
    """
    print(Fore.BLUE + "\n" + "=" * 40 + Style.RESET_ALL)
    print(Fore.LIGHTCYAN_EX + "       SISTEMA DE GESTIÓN DE USUARIOS" + Style.RESET_ALL)
    print("=" * 40)
    print("  1. Crear usuario")
    print("  2. Listar usuarios")
    print("  3. Buscar usuario")
    print("  4. Actualizar usuario")
    print("  5. Eliminar usuario")
    print("  6. Generar registros falsos (Faker)")
    print("  0. Salir")
    print(Fore.BLUE + "=" * 40 + Style.RESET_ALL)


def prompt_new_user() -> Tuple[str, str, str, str, str]:
    """
    Solicita los datos para crear un nuevo usuario.

    Returns:
        Tuple[str, str, str, str, str]: Tupla con id, name, email, age, status.
    """
    print("\n-- Nuevo usuario --")
    return (
        input("ID:      ").strip(),
        input("Nombre:  ").strip(),
        input("Correo:  ").strip(),
        input("Edad:    ").strip(),
        input("Estado (Activo/Inactivo): ").strip(),
    )


def prompt_search() -> Tuple[str, str]:
    """
    Solicita los criterios de búsqueda.

    Returns:
        Tuple[str, str]: Tupla con el campo y el valor a buscar.
    """
    print("\n-- Buscar usuario --")
    print("Campos disponibles: id, name, email, age, status")
    field = input("Campo a buscar: ").strip().lower()
    value = input("Valor:          ").strip()
    return field, value


def prompt_update() -> Tuple[str, Optional[str], Optional[str], Optional[str], Optional[str]]:
    """
    Solicita el ID y los campos a actualizar (deja en blanco para omitir).

    Returns:
        Tuple[str, Optional[str], ...]: ID seguido de nombre, email, edad, estado opcionales.
    """
    print("\n-- Actualizar usuario --")
    print("Deja en blanco los campos que no quieras modificar.")
    id_input = input("ID del usuario a actualizar: ").strip()
    name = input("Nuevo nombre  (Enter para omitir): ").strip() or None
    email = input("Nuevo correo  (Enter para omitir): ").strip() or None
    age = input("Nueva edad    (Enter para omitir): ").strip() or None
    status = input("Nuevo estado  (Enter para omitir): ").strip() or None
    return id_input, name, email, age, status


def prompt_delete() -> str:
    """
    Solicita el ID del usuario a eliminar.

    Returns:
        str: ID ingresado.
    """
    print("\n-- Eliminar usuario --")
    return input("ID del usuario a eliminar: ").strip()


def print_result(success: bool, message_or_list: Union[str, List[str], Any]) -> None:
    """
    Imprime el resultado de una operación CRUD de forma uniforme.

    Args:
        success (bool): Si la operación fue exitosa o no.
        message_or_list (Union[str, List[str], Any]): Mensaje de error o lista de resultados.
    """
    if success:
        if isinstance(message_or_list, list):
            for line in message_or_list:
                print(" •", line)
        else:
            print(f"\nOK: {message_or_list}")
    else:
        print(f"\nError: {message_or_list}")


def run_menu() -> None:
    """
    Bucle principal de la interfaz de consola.
    Se inicializa la data, se muestra el menú y se procesa el Input del usuario delegando la ejecución a Service.
    """
    loaded_records = load_data()
    initialize_users(loaded_records)

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
            break

        if option == "1":
            id_in, name, email, age, status = prompt_new_user()
            ok, msg = new_register(id_in, name, email, age, status)
            print_result(ok, msg)
            
        elif option == "2":
            print("\n-- Usuarios registrados --")
            result = list_records()
            if not result:
                print("No hay usuarios registrados aún.")
            else:
                print_result(True, result)

        elif option == "3":
            field, value = prompt_search()
            ok, result_search = search_record(field, value)
            print_result(ok, result_search)

        elif option == "4":
            id_in, name, email, age, status = prompt_update()
            ok, msg = update_record(id_in, name, email, age, status)
            print_result(ok, msg)

        elif option == "5":
            id_in = prompt_delete()
            ok, msg = delete_record(id_in)
            print_result(ok, msg)

        elif option == "6":
            print("\n-- Generar registros falsos (Faker) --")
            creados, errores = generar_registros_falsos(10)
            print(f"\n✅ Se generaron {creados} registros falsos exitosamente.")
            if errores:
                print(f"⚠️  {len(errores)} registro(s) no se pudieron crear:")
                for err in errores:
                    print(f"   • {err}")
            print("\n-- Usuarios actualizados --")
            print_result(True, list_records())

        elif option == "0":
            print("\n¡Hasta luego!")
            break

        else:
            print("\nOpción no válida. Intenta de nuevo.")