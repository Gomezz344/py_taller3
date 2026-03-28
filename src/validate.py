import re


def validate_id(user_id, existing_ids):
    try:
        user_id = int(user_id)
        if user_id <= 0:
            return False, "El ID debe ser un número entero positivo."
        if user_id in existing_ids:
            return False, f"El ID {user_id} ya existe. Usa uno diferente."
        return True, user_id
    except ValueError:
        return False, "El ID debe ser un número entero."


def validate_name(name):
    name = name.strip()
    if not name:
        return False, "El nombre no puede estar vacío."
    if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', name):
        return False, "El nombre solo puede contener letras y espacios."
    return True, name


def validate_email(email):
    email = email.strip().lower()
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
    if not re.match(pattern, email):
        return False, "El correo no tiene un formato válido. Ejemplo: usuario@correo.com"
    return True, email


def validate_age(age):
    try:
        age = int(age)
        if age < 1 or age > 100:
            return False, "La edad debe estar entre 1 y 100 años."
        return True, age
    except ValueError:
        return False, "La edad debe ser un número entero."


def validate_status(status):
    if status == "Activo":
        return True, status
    else:
        return False, "Inactivo"