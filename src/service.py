from validate import (
    validate_id,
    validate_name,
    validate_email,
    validate_age,
    validate_status,
)

users = []
registered_ids = set()

# Inicialización

def initialize_users(initial_data):
    """Carga la lista de usuarios desde los datos persistidos."""
    users.clear()
    registered_ids.clear()

    for item in initial_data:
        if not isinstance(item, dict):
            continue
        user_id = item.get("id")
        if isinstance(user_id, int):
            users.append(item)
            registered_ids.add(user_id)


def get_users_data():
    """Retorna la lista interna de usuarios (para persistir)."""
    return users

# CREATE

def new_register(id, name, email, age, status):
    """
    Crea y registra un nuevo usuario tras validar todos los campos.
    Retorna (True, mensaje) si tuvo éxito, o (False, error) si no.
    """
    ok, id_val = validate_id(id, registered_ids)
    if not ok:
        return False, id_val

    ok, name_val = validate_name(name)
    if not ok:
        return False, name_val

    ok, email_val = validate_email(email)
    if not ok:
        return False, email_val

    ok, age_val = validate_age(age)
    if not ok:
        return False, age_val

    ok, status_val = validate_status(status)
    if not ok:
        return False, status_val

    new_user = {
        "id": id_val,
        "name": name_val,
        "email": email_val,
        "age": age_val,
        "status": status_val,
    }

    users.append(new_user)
    registered_ids.add(id_val)

    return True, f"Usuario '{name_val}' creado exitosamente."


# Alias para compatibilidad con main.py existente
def create_user(id, name, email, age, status):
    return new_register(id, name, email, age, status)


# READ — listar

def list_records():
    """
    Retorna todos los usuarios ordenados por nombre (usando lambda).
    Retorna lista vacía si no hay registros.
    """
    if not users:
        return []

    # Lambda para ordenar alfabéticamente por nombre (case-insensitive)
    sorted_users = sorted(users, key=lambda u: u["name"].lower())

    summary = [
        f"[{u['id']}] {u['name']} | {u['email']} | Edad: {u['age']} | Estado: {u['status']}"
        for u in sorted_users
    ]
    return summary


# Alias para compatibilidad con main.py existente
def list_users():
    return list_records()

# READ — buscar

def search_record(field, value):
    """
    Busca usuarios por campo y valor (búsqueda parcial, case-insensitive).
    Campos válidos: id, name, email, age, status.
    Retorna (True, lista_de_resultados) o (False, mensaje_de_error).

    Usa list comprehension para filtrar.
    """
    valid_fields = {"id", "name", "email", "age", "status"}

    if field not in valid_fields:
        return False, f"Campo '{field}' no válido. Usa: {', '.join(sorted(valid_fields))}."

    value_str = str(value).strip().lower()

    if not value_str:
        return False, "El valor de búsqueda no puede estar vacío."

    # List comprehension: filtra usuarios donde el campo coincida parcialmente
    results = [
        u for u in users
        if value_str in str(u.get(field, "")).lower()
    ]

    if not results:
        return False, f"No se encontraron usuarios con {field}='{value}'."

    summary = [
        f"[{u['id']}] {u['name']} | {u['email']} | Edad: {u['age']} | Estado: {u['status']}"
        for u in results
    ]
    return True, summary


# UPDATE

def update_record(id, name=None, email=None, age=None, status=None):
    try:
        target_id = int(id)
    except (ValueError, TypeError):
        return False, "El ID debe ser un número entero."

    if target_id not in registered_ids:
        return False, f"No existe ningún usuario con ID {target_id}."

    # Buscar el usuario usando next + lambda (uso real de lambda)
    user = next((u for u in users if u["id"] == target_id), None)

    if user is None:
        return False, f"No existe ningún usuario con ID {target_id}."

    updated_fields = []

    if name is not None:
        ok, name_val = validate_name(name)
        if not ok:
            return False, name_val
        user["name"] = name_val
        updated_fields.append("name")

    if email is not None:
        ok, email_val = validate_email(email)
        if not ok:
            return False, email_val
        user["email"] = email_val
        updated_fields.append("email")

    if age is not None:
        ok, age_val = validate_age(age)
        if not ok:
            return False, age_val
        user["age"] = age_val
        updated_fields.append("age")

    if status is not None:
        ok, status_val = validate_status(status)
        if not ok:
            return False, status_val
        user["status"] = status_val
        updated_fields.append("status")

    if not updated_fields:
        return False, "No se proporcionó ningún campo para actualizar."

    fields_str = ", ".join(updated_fields)
    return True, f"Usuario ID {target_id} actualizado correctamente ({fields_str})."



# DELETE

def delete_record(id):
    try:
        target_id = int(id)
    except (ValueError, TypeError):
        return False, "El ID debe ser un número entero."

    if target_id not in registered_ids:
        return False, f"No existe ningún usuario con ID {target_id}."

    # Guardar nombre antes de eliminar (para el mensaje de confirmación)
    deleted_user = next((u for u in users if u["id"] == target_id), None)
    deleted_name = deleted_user["name"] if deleted_user else "Desconocido"

    # List comprehension: reconstruye la lista excluyendo el registro eliminado
    remaining = [u for u in users if u["id"] != target_id]

    users.clear()
    users.extend(remaining)
    registered_ids.discard(target_id)

    return True, f"Usuario '{deleted_name}' (ID {target_id}) eliminado exitosamente."