from typing import List, Tuple, Dict, Any, Optional
from validate import (
    validate_id,
    validate_name,
    validate_email,
    validate_age,
    validate_status,
)
from file import save_data

users: List[Dict[str, Any]] = []
registered_ids: set = set()

def initialize_users(initial_data: List[Dict[str, Any]]) -> None:
    """
    Carga la lista de usuarios desde los datos persistidos en memoria.

    Args:
        initial_data (List[Dict[str, Any]]): Lista de usuarios obtenida del archivo.
    """
    users.clear()
    registered_ids.clear()

    for item in initial_data:
        if not isinstance(item, dict):
            continue
        user_id = item.get("id")
        if isinstance(user_id, int):
            users.append(item)
            registered_ids.add(user_id)


def get_users_data() -> List[Dict[str, Any]]:
    """
    Retorna la lista interna de usuarios.

    Returns:
        List[Dict[str, Any]]: Copia o referencia a la lista de usuarios en memoria.
    """
    return users


def new_register(id: Any, name: str, email: str, age: Any, status: str) -> Tuple[bool, str]:
    """
    Crea y registra un nuevo usuario tras validar todos los campos.
    Guarda automáticamente en disco si tiene éxito.

    Args:
        id (Any): ID del usuario.
        name (str): Nombre del usuario.
        email (str): Correo electrónico.
        age (Any): Edad.
        status (str): Estado (Activo/Inactivo).

    Returns:
        Tuple[bool, str]: Tupla con éxito y mensaje de resultado.
    """
    ok, id_val = validate_id(id, registered_ids)
    if not ok:
        return False, str(id_val)

    ok, name_val = validate_name(name)
    if not ok:
        return False, str(name_val)

    ok, email_val = validate_email(email)
    if not ok:
        return False, str(email_val)

    ok, age_val = validate_age(age)
    if not ok:
        return False, str(age_val)

    ok, status_val = validate_status(status)
    if not ok:
        return False, str(status_val)

    new_user = {
        "id": id_val,
        "name": name_val,
        "email": email_val,
        "age": age_val,
        "status": status_val,
    }

    users.append(new_user)
    registered_ids.add(id_val)
    
    save_data(users)

    return True, f"Usuario '{name_val}' creado exitosamente."


def create_user(id: Any, name: str, email: str, age: Any, status: str) -> Tuple[bool, str]:
    """Alias para new_register. Mantenido por compatibilidad."""
    return new_register(id, name, email, age, status)


def list_records() -> List[str]:
    """
    Retorna todos los usuarios ordenados por nombre.
    
    Returns:
        List[str]: Lista de cadenas formateadas con el resumen de usuarios.
    """
    if not users:
        return []

    sorted_users = sorted(users, key=lambda u: str(u.get("name", "")).lower())

    summary = [
        f"[{u.get('id')}] {u.get('name')} | {u.get('email')} | Edad: {u.get('age')} | Estado: {u.get('status')}"
        for u in sorted_users
    ]
    return summary


def list_users() -> List[str]:
    """Alias para list_records. Mantenido por compatibilidad."""
    return list_records()


def search_record(field: str, value: str) -> Tuple[bool, Any]:
    """
    Busca usuarios por campo y valor (búsqueda parcial, sin importar mayúsculas).

    Args:
        field (str): Campo de búsqueda (ej. id, name, email).
        value (str): Valor a buscar.

    Returns:
        Tuple[bool, Any]: Éxito, y una lista de resultados formateados o un mensaje de error.
    """
    valid_fields = {"id", "name", "email", "age", "status"}

    if field not in valid_fields:
        return False, f"Campo '{field}' no válido. Usa: {', '.join(sorted(valid_fields))}."

    value_str = str(value).strip().lower()

    if not value_str:
        return False, "El valor de búsqueda no puede estar vacío."

    results = [
        u for u in users
        if value_str in str(u.get(field, "")).lower()
    ]

    if not results:
        return False, f"No se encontraron usuarios con {field}='{value}'."

    summary = [
        f"[{u.get('id')}] {u.get('name')} | {u.get('email')} | Edad: {u.get('age')} | Estado: {u.get('status')}"
        for u in results
    ]
    return True, summary


def update_record(id: Any, name: Optional[str] = None, email: Optional[str] = None, age: Optional[Any] = None, status: Optional[str] = None) -> Tuple[bool, str]:
    """
    Actualiza campos específicos de un usuario existente.
    Guarda automáticamente si hay cambios.

    Args:
        id (Any): ID del usuario.
        name (Optional[str], optional): Nuevo nombre. Defaults to None.
        email (Optional[str], optional): Nuevo email. Defaults to None.
        age (Optional[Any], optional): Nueva edad. Defaults to None.
        status (Optional[str], optional): Nuevo status. Defaults to None.

    Returns:
        Tuple[bool, str]: Tupla con éxito y el mensaje descriptivo.
    """
    try:
        target_id = int(id)
    except (ValueError, TypeError):
        return False, "El ID debe ser un número entero."

    if target_id not in registered_ids:
        return False, f"No existe ningún usuario con ID {target_id}."

    user = next((u for u in users if u.get("id") == target_id), None)

    if user is None:
        return False, f"No existe ningún usuario con ID {target_id}."

    updated_fields = []

    if name is not None:
        ok, name_val = validate_name(name)
        if not ok:
            return False, str(name_val)
        user["name"] = name_val
        updated_fields.append("name")

    if email is not None:
        ok, email_val = validate_email(email)
        if not ok:
            return False, str(email_val)
        user["email"] = email_val
        updated_fields.append("email")

    if age is not None:
        ok, age_val = validate_age(age)
        if not ok:
            return False, str(age_val)
        user["age"] = age_val
        updated_fields.append("age")

    if status is not None:
        ok, status_val = validate_status(status)
        if not ok:
            return False, str(status_val)
        user["status"] = status_val
        updated_fields.append("status")

    if not updated_fields:
        return False, "No se proporcionó ningún campo para actualizar."

    fields_str = ", ".join(updated_fields)
    save_data(users)
    return True, f"Usuario ID {target_id} actualizado correctamente ({fields_str})."


def delete_record(id: Any) -> Tuple[bool, str]:
    """
    Elimina un usuario por su ID y guarda cambios en disco.

    Args:
        id (Any): ID entero (o valor convertible a entero) del usuario.

    Returns:
        Tuple[bool, str]: Tupla con éxito y mensaje de resultado.
    """
    try:
        target_id = int(id)
    except (ValueError, TypeError):
        return False, "El ID debe ser un número entero."

    if target_id not in registered_ids:
        return False, f"No existe ningún usuario con ID {target_id}."

    deleted_user = next((u for u in users if u.get("id") == target_id), None)
    deleted_name = deleted_user.get("name") if deleted_user else "Desconocido"

    remaining = [u for u in users if u.get("id") != target_id]

    users.clear()
    users.extend(remaining)
    registered_ids.discard(target_id)
    
    save_data(users)

    return True, f"Usuario '{deleted_name}' (ID {target_id}) eliminado exitosamente."