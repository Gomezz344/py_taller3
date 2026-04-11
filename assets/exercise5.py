# Ejercicio 5: Validador de contraseñas — refactorizado con pruebas unitarias

MIN_LONGITUD = 8


# Cada regla en su propia función: fácil de leer, modificar y probar por separado
def tiene_longitud_minima(password: str) -> bool:
    return len(password) >= MIN_LONGITUD

def tiene_numero(password: str) -> bool:
    return any(c.isdigit() for c in password)

def tiene_mayuscula(password: str) -> bool:
    return any(c.isupper() for c in password)

def no_tiene_espacios(password: str) -> bool:
    return " " not in password


def validar_password(password: str) -> tuple[bool, list[str]]:
    """Valida la contraseña y retorna (es_valida, lista de errores encontrados)."""
    errores = []

    if not tiene_longitud_minima(password):
        errores.append(f"Debe tener al menos {MIN_LONGITUD} caracteres.")
    if not tiene_numero(password):
        errores.append("Debe contener al menos un número.")
    if not tiene_mayuscula(password):
        errores.append("Debe contener al menos una mayúscula.")
    if not no_tiene_espacios(password):
        errores.append("No debe contener espacios.")

    return len(errores) == 0, errores


def correr_pruebas():
    # Casos: (contraseña, resultado esperado, descripción)
    casos = [
        ("Hola1234",       True,  "válida — cumple todas las reglas"),
        ("hola1234",       False, "inválida — sin mayúscula"),
        ("HOLA1234",       True,  "válida — tiene mayúscula y número"),
        ("Holaaaa8",       True,  "válida — 8 chars exactos"),
        ("Ho 1234A",       False, "inválida — contiene espacio"),
        ("H1a",            False, "inválida — muy corta"),
        ("SuperSegura99!", True,  "válida — con caracteres especiales"),
        ("sinmayus1",      False, "inválida — sin mayúscula"),
        ("SinNumero!",     False, "inválida — sin dígito"),
    ]

    print("═" * 50)
    print("  PRUEBAS UNITARIAS — validar_password()")
    print("═" * 50)
    aprobadas = 0
    for password, esperado, desc in casos:
        es_valida, errores = validar_password(password)
        paso = es_valida == esperado
        aprobadas += paso
        print(f"{'✅ PASS' if paso else '❌ FAIL'} | '{password}' → {desc}")
        for e in errores:
            print(f"         ↳ {e}")
    print("═" * 50)
    print(f"  Resultado: {aprobadas}/{len(casos)} pruebas aprobadas")
    print("═" * 50)


def main():
    correr_pruebas()
    print()
    password = input("Ingresa tu contraseña para validar: ")
    es_valida, errores = validar_password(password)
    if es_valida:
        print("✅ Contraseña válida.")
    else:
        print("❌ Contraseña inválida:")
        for error in errores:
            print(f"   • {error}")


if __name__ == "__main__":
    main()
