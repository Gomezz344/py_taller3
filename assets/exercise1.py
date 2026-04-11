# Ejercicio 1: Leer enteros separados por comas y calcular el promedio

def calcular_promedio(entrada: str) -> float:
    numeros = []

    for parte in entrada.split(","):
        try:
            numeros.append(int(parte.strip()))
        except ValueError:
            # Si un valor no es entero, se avisa y se omite
            print(f"  ⚠️  '{parte.strip()}' no es un entero válido, se omite.")

    # Si no quedó ningún número válido, no se puede calcular el promedio
    if len(numeros) == 0:
        raise ZeroDivisionError("No hay números válidos para calcular el promedio.")

    return sum(numeros) / len(numeros)


entrada = input("Ingresa enteros separados por comas: ")

try:
    promedio = calcular_promedio(entrada)
    print(f"Promedio: {promedio:.2f}")
except ZeroDivisionError as e:
    print(f"Error: {e}")
