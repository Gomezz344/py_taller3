from validate import (
    validate_id,
    validate_name,
    validate_email,
    validate_age,
    validate_status,
)

users = []
registered_ids = set()


def initialize_users(initial_data):
    users.clear()
    registered_ids.clear()

    for item in initial_data:
        if not isinstance(item, dict):
            continue
        user_id = item.get("id")
        if isinstance(user_id, int):
            users.append(item)
            registered_ids.add(user_id)


def create_user(id, name, email, age, status):
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


def list_users():
    if not users:
        return []

    summary = []
    for u in users:
        line = f"[{u['id']}] {u['name']} | {u['email']} | Edad: {u['age']} | Estado: {u['status']}"
        summary.append(line)

    return summary


def get_users_data():
    return users