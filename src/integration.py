"""
integration.py — Pruebas de integración para el módulo CRUD (m3-crud)

Ejecutar directamente:  python integration.py
No requiere entrada del usuario. Verifica que las 5 funciones CRUD
funcionen correctamente y que los cambios se reflejen en el archivo.
"""

import os
import json
from file import load_data, save_data, FILE_PATH
from service import (
    initialize_users,
    get_users_data,
    new_register,
    list_records,
    search_record,
    update_record,
    delete_record,
)

PASS = "✅ PASS"
FAIL = "❌ FAIL"


def banner(title):
    print(f"\n{'─' * 45}")
    print(f"  {title}")
    print(f"{'─' * 45}")


def check(label, condition):
    status = PASS if condition else FAIL
    print(f"  {status}  {label}")
    return condition


def setup():
    """Limpia el archivo de datos y reinicia el estado en memoria."""
    os.makedirs("data", exist_ok=True)
    save_data([])
    initialize_users([])


def test_create():
    banner("CREATE — new_register()")

    ok, msg = new_register("10", "Ana García", "ana@correo.com", "28", "Activo")
    check("Crear usuario válido retorna True", ok)
    check("Mensaje contiene el nombre", "Ana García" in msg)

    ok2, msg2 = new_register("10", "Otro", "otro@correo.com", "30", "Activo")
    check("ID duplicado retorna False", not ok2)

    ok3, msg3 = new_register("abc", "Pedro", "pedro@correo.com", "25", "Activo")
    check("ID no numérico retorna False", not ok3)

    ok4, msg4 = new_register("11", "", "x@correo.com", "20", "Activo")
    check("Nombre vacío retorna False", not ok4)

    ok5, msg5 = new_register("12", "Luis", "correo-invalido", "20", "Activo")
    check("Email inválido retorna False", not ok5)

    ok6, msg6 = new_register("13", "Marta", "marta@correo.com", "200", "Activo")
    check("Edad fuera de rango retorna False", not ok6)

    ok7, msg7 = new_register("14", "Carlos", "carlos@correo.com", "35", "inactivo")
    check("Estado 'inactivo' (minúscula) normalizado a 'Inactivo'", ok7)


def test_list():
    banner("LIST — list_records()")

    result = list_records()
    check("Retorna lista no vacía", len(result) > 0)
    check("Elementos son strings", all(isinstance(r, str) for r in result))

    # Verificar que esta ordenado alfabeticamente
    names_in_result = [r.split("]")[1].split("|")[0].strip() for r in result]
    check("Lista ordenada alfabéticamente (lambda)", names_in_result == sorted(names_in_result, key=str.lower))


def test_search():
    banner("SEARCH — search_record()")

    ok, results = search_record("name", "Ana")
    check("Búsqueda por nombre existente retorna True", ok)
    check("Resultado contiene 'Ana'", any("Ana" in r for r in results))

    ok2, _ = search_record("name", "ZZZ_inexistente")
    check("Búsqueda sin resultados retorna False", not ok2)

    ok3, _ = search_record("campo_falso", "valor")
    check("Campo inválido retorna False", not ok3)

    ok4, results4 = search_record("status", "Activo")
    check("Búsqueda por status funciona", ok4 and len(results4) > 0)


def test_update():
    banner("UPDATE — update_record()")

    ok, msg = update_record("10", name="Ana López")
    check("Actualizar nombre retorna True", ok)
    check("Mensaje confirma actualización", "actualizado" in msg.lower())

    # Verificar que el cambio se refleja en la lista
    records = list_records()
    check("Cambio reflejado en list_records()", any("Ana López" in r for r in records))

    ok2, _ = update_record("999")
    check("ID inexistente retorna False", not ok2)

    ok3, _ = update_record("10", email="no-es-un-email")
    check("Email inválido en update retorna False", not ok3)

    ok4, _ = update_record("10")
    check("Update sin campos retorna False", not ok4)


def test_delete():
    banner("DELETE — delete_record()")

    ok, msg = delete_record("10")
    check("Eliminar usuario existente retorna True", ok)
    check("Mensaje confirma eliminación", "eliminado" in msg.lower())

    # Verificar que ya no aparece en la lista
    records = list_records()
    check("Eliminado no aparece en list_records()", not any("[10]" in r for r in records))

    ok2, _ = delete_record("10")
    check("Eliminar ID ya borrado retorna False", not ok2)

    ok3, _ = delete_record("abc")
    check("ID no numérico en delete retorna False", not ok3)


def test_persistence():
    banner("PERSISTENCIA — reflejo en archivo")

    save_data(get_users_data())
    loaded = load_data()
    in_memory = get_users_data()

    check("Datos en archivo coinciden con memoria", loaded == in_memory)
    check("Archivo contiene lista JSON", isinstance(loaded, list))

    if loaded:
        check("Cada registro tiene los campos requeridos",
              all({"id", "name", "email", "age", "status"}.issubset(r.keys()) for r in loaded))


def run_all():
    print("\n" + "=" * 45)
    print("  INTEGRACIÓN CRUD — m3-crud")
    print("=" * 45)

    setup()
    test_create()
    test_list()
    test_search()
    test_update()
    test_delete()
    test_persistence()

    print(f"\n{'=' * 45}")
    print("  Integración completada.")
    print(f"{'=' * 45}\n")


if __name__ == "__main__":
    run_all()