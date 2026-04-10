import sys
import os
import pytest

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

from service import (
    new_register,
    list_records,
    search_record,
    update_record,
    delete_record,
    initialize_users,
    get_users_data
)
from file import save_data, load_data


@pytest.fixture(autouse=True)
def reset():
    """Reinicia el estado en memoria y archivo antes de cada prueba."""
    os.makedirs("data", exist_ok=True)
    save_data([])
    initialize_users([])
    yield
    save_data([])
    initialize_users([])


# ── CREATE ──────────────────────────────────────────
def test_crear_usuario_valido():
    ok, msg = new_register("1", "Ana García", "ana@correo.com", "28", "Activo")
    assert ok
    assert "Ana García" in msg

def test_id_duplicado_retorna_false():
    new_register("1", "Ana", "ana@correo.com", "28", "Activo")
    ok, _ = new_register("1", "Otro", "otro@correo.com", "30", "Activo")
    assert not ok

def test_email_invalido_retorna_false():
    ok, _ = new_register("2", "Luis", "no-es-email", "25", "Activo")
    assert not ok

def test_edad_fuera_de_rango_retorna_false():
    ok, _ = new_register("3", "Marta", "marta@correo.com", "200", "Activo")
    assert not ok


# ── UPDATE ──────────────────────────────────────────
def test_actualizar_campo_existente():
    new_register("4", "Carlos", "carlos@correo.com", "35", "Activo")
    ok, msg = update_record("4", name="Carlos López")
    assert ok
    assert "actualizada" in msg.lower() or "actualizado" in msg.lower()

def test_actualizar_campo_inexistente_retorna_falso():
    ok, _ = update_record("999", name="Fake")
    assert not ok


# ── DELETE ──────────────────────────────────────────
def test_eliminar_usuario_existente():
    new_register("5", "Pedro", "pedro@correo.com", "40", "Inactivo")
    ok, msg = delete_record("5")
    assert ok
    assert "eliminado" in msg.lower()

def test_eliminar_usuario_inexistente_retorna_falso():
    ok, _ = delete_record("999")
    assert not ok


# ── SEARCH ──────────────────────────────────────────
def test_busqueda_por_nombre_existente():
    new_register("6", "Laura", "laura@correo.com", "22", "Activo")
    ok, results = search_record("name", "Laura")
    assert ok
    assert isinstance(results, list)
    assert any("Laura" in str(r) for r in results)

def test_busqueda_por_campo_invalido_retorna_falso():
    new_register("7", "Juan", "juan@correo.com", "30", "Activo")
    ok, _ = search_record("invalid_field", "Juan")
    assert not ok


# ── PERSISTENCIA ────────────────────────────────────
def test_datos_guardados_coinciden_con_memoria():
    new_register("8", "Rosa", "rosa@correo.com", "31", "Activo")
    # new_register hace un guardado automático, así que esto ya debería estar persistido
    assert load_data() == get_users_data()
