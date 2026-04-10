"""
integration.py — Generación de registros falsos con Faker + pruebas de integración

Funcionalidades:
  1. Generar registros falsos usando la librería Faker (locale es_MX).
     Se expone como opción del menú principal.
  2. Pruebas de integración para el módulo CRUD.
     Ejecutar directamente:  python integration.py

Uso de *args / **kwargs:
  - crear_registro(**kwargs)  → construye un registro individual.
    Acepta campos arbitrarios; los que no se proporcionen se generan con Faker.
  - generar_registros_falsos(*args, **kwargs) → genera N registros.
    *args[0] = cantidad (por defecto 10).
    **kwargs = campos fijos que se aplican a todos los registros generados.
"""

import os
import sys
import json
import random
from faker import Faker

# Forzar UTF-8 en la consola de Windows para caracteres especiales
if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
from file import load_data, save_data, FILE_PATH
from service import (
    initialize_users,
    get_users_data,
    new_register,
    list_records,
    search_record,
    update_record,
    delete_record,
    registered_ids,
)

# ─── Configuración de Faker ───────────────────────────────────────────
fake = Faker("es_MX")

# ─── Generación de registros falsos ───────────────────────────────────


def _next_available_id():
    """Retorna el siguiente ID entero positivo que no esté en uso."""
    candidate = 1
    while candidate in registered_ids:
        candidate += 1
    return candidate


def crear_registro(**kwargs):
    """
    Construye un dict de usuario a partir de **kwargs.
    Los campos que no se proporcionen se generan automáticamente con Faker.

    Parámetros aceptados (todos opcionales):
      id     – int | str   (se auto-genera si no se envía)
      name   – str
      email  – str
      age    – int | str
      status – 'Activo' | 'Inactivo'

    Retorna: dict con las llaves {id, name, email, age, status}
    """
    user_id = kwargs.get("id", _next_available_id())
    name    = kwargs.get("name", fake.name())
    email   = kwargs.get("email", fake.email())
    age     = kwargs.get("age", random.randint(18, 65))
    status  = kwargs.get("status", random.choice(["Activo", "Inactivo"]))

    return {
        "id":     str(user_id),
        "name":   str(name),
        "email":  str(email),
        "age":    str(age),
        "status": str(status),
    }


def generar_registros_falsos(*args, **kwargs):
    """
    Genera y registra N usuarios falsos en el sistema.

    *args:
      args[0] – cantidad de registros a generar (int, por defecto 10).

    **kwargs:
      Campos fijos que se aplicarán a TODOS los registros generados.
      Ejemplo: generar_registros_falsos(5, status="Activo")
               → genera 5 usuarios, todos con estado "Activo".

    Retorna: (cantidad_creados: int, errores: list[str])
    """
    cantidad = args[0] if args else 10
    creados  = 0
    errores  = []

    for _ in range(cantidad):
        registro = crear_registro(**kwargs)

        ok, msg = new_register(
            registro["id"],
            registro["name"],
            registro["email"],
            registro["age"],
            registro["status"],
        )

        if ok:
            creados += 1
        else:
            errores.append(msg)

    return creados, errores


# ─── Pruebas de integración ──────────────────────────────────────────

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