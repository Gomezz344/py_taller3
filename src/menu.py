def show_main_menu():
    print("\n" + "=" * 40)
    print("       SISTEMA DE GESTIÓN DE USUARIOS")
    print("=" * 40)
    print("  1. Crear usuario")
    print("  2. Listar usuarios")
    print("  3. Buscar usuario")
    print("  4. Actualizar usuario")
    print("  5. Eliminar usuario")
    print("  0. Salir")
    print("=" * 40)


def prompt_new_user():
    """Solicita los datos para crear un nuevo usuario."""
    print("\n-- Nuevo usuario --")
    return (
        input("ID:      ").strip(),
        input("Nombre:  ").strip(),
        input("Correo:  ").strip(),
        input("Edad:    ").strip(),
        input("Estado (Activo/Inactivo): ").strip(),
    )


def prompt_search():
    """Solicita los criterios de búsqueda."""
    print("\n-- Buscar usuario --")
    print("Campos disponibles: id, name, email, age, status")
    field = input("Campo a buscar: ").strip().lower()
    value = input("Valor:          ").strip()
    return field, value


def prompt_update():
    """Solicita el ID y los campos a actualizar (deja en blanco para omitir)."""
    print("\n-- Actualizar usuario --")
    print("Deja en blanco los campos que no quieras modificar.")
    id_input = input("ID del usuario a actualizar: ").strip()
    name  = input("Nuevo nombre  (Enter para omitir): ").strip() or None
    email = input("Nuevo correo  (Enter para omitir): ").strip() or None
    age   = input("Nueva edad    (Enter para omitir): ").strip() or None
    status = input("Nuevo estado  (Enter para omitir): ").strip() or None
    return id_input, name, email, age, status


def prompt_delete():
    """Solicita el ID del usuario a eliminar."""
    print("\n-- Eliminar usuario --")
    return input("ID del usuario a eliminar: ").strip()


def print_result(success, message_or_list):
    """Imprime el resultado de una operación CRUD de forma uniforme."""
    if success:
        if isinstance(message_or_list, list):
            for line in message_or_list:
                print(" •", line)
        else:
            print(f"\nOK: {message_or_list}")
    else:
        print(f"\nError: {message_or_list}")