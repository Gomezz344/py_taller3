import re
from typing import Any, Tuple, Union, Set

VALID_STATUSES: Set[str] = {"Activo", "Inactivo"}


def validate_id(user_id: Any, existing_ids: Set[int]) -> Tuple[bool, Union[int, str]]:
    """
    Verifica que el ID sea un número entero positivo y no esté duplicado.

    Args:
        user_id (Any): ID a validar, puede ser int o string.
        existing_ids (Set[int]): Conjunto de IDs ya registrados.

    Returns:
        Tuple[bool, Union[int, str]]: Tupla con (es_valido, id_como_entero_o_mensaje_error).
    """
    try:
        parsed_id = int(user_id)
        if parsed_id <= 0:
            return False, "El ID debe ser un número entero positivo."
        if parsed_id in existing_ids:
            return False, f"El ID {parsed_id} ya existe. Usa uno diferente."
        return True, parsed_id
    except (ValueError, TypeError):
        return False, "El ID debe ser un número entero."


def validate_name(name: str) -> Tuple[bool, str]:
    """
    Verifica que el nombre no esté vacío y contenga solo letras y espacios.

    Args:
        name (str): Nombre a validar.

    Returns:
        Tuple[bool, str]: Tupla con (es_valido, nombre_limpio_o_mensaje_error).
    """
    name = str(name).strip()
    if not name:
        return False, "El nombre no puede estar vacío."
    if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', name):
        return False, "El nombre solo puede contener letras y espacios."
    return True, name


def validate_email(email: str) -> Tuple[bool, str]:
    """
    Verifica que el correo tenga formato válido.

    Args:
        email (str): Correo a validar.

    Returns:
        Tuple[bool, str]: Tupla con (es_valido, correo_limpio_o_mensaje_error).
    """
    email = str(email).strip().lower()
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
    if not re.match(pattern, email):
        return False, "El correo no tiene un formato válido. Ejemplo: usuario@correo.com"
    return True, email


def validate_age(age: Any) -> Tuple[bool, Union[int, str]]:
    """
    Verifica que la edad sea un entero entre 1 y 100.

    Args:
        age (Any): Edad a validar (str o int).

    Returns:
        Tuple[bool, Union[int, str]]: Tupla con (es_valido, edad_entera_o_mensaje_error).
    """
    try:
        parsed_age = int(age)
        if parsed_age < 1 or parsed_age > 100:
            return False, "La edad debe estar entre 1 y 100 años."
        return True, parsed_age
    except (ValueError, TypeError):
        return False, "La edad debe ser un número entero."


def validate_status(status: Any) -> Tuple[bool, str]:
    """
    Verifica que el estado sea 'Activo' o 'Inactivo'.

    Args:
        status (Any): Estado a validar.

    Returns:
        Tuple[bool, str]: Tupla con (es_valido, estado_normalizado_o_mensaje_error).
    """
    status = str(status).strip().capitalize() if isinstance(status, str) else ""
    for valid in VALID_STATUSES:
        if status.lower() == valid.lower():
            return True, valid
    return False, f"Estado no válido. Usa: {', '.join(sorted(VALID_STATUSES))}."