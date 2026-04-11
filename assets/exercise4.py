# Ejercicio 4: Refactor de calculadora — sin tipos mezclados ni letras "mágicas"

OPERACIONES_VALIDAS = ("suma", "resta", "multi", "divi")


def calc(a: float, b: float, op: str) -> float:
    """
    Realiza una operación aritmética entre a y b.
    Lanza ValueError si la operación no existe.
    Lanza ZeroDivisionError si se divide entre cero.
    """
    ops = {
        "suma":  lambda x, y: x + y,
        "resta": lambda x, y: x - y,
        "multi": lambda x, y: x * y,
        "divi":  lambda x, y: x / y,
    }

    if op not in ops:
        raise ValueError(f"Operación '{op}' no reconocida. Usa: {OPERACIONES_VALIDAS}")

    # Validar antes de dividir para dar un mensaje claro
    if op == "divi" and b == 0:
        raise ZeroDivisionError("No se puede dividir entre cero.")

    return ops[op](a, b)


try:
    op = input("Ingrese operación (suma, resta, multi, divi): ").strip()
    a  = float(input("Ingrese primer número: "))
    b  = float(input("Ingrese segundo número: "))
    resultado = calc(a, b, op)
    print(f"El resultado de '{op}' es: {resultado}")
except ValueError as e:
    print(f"❌ Valor inválido: {e}")
except ZeroDivisionError as e:
    print(f"❌ División por cero: {e}")
