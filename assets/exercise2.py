# Ejercicio 2: Abrir un archivo, contar sus líneas y cerrarlo siempre

def contar_lineas(ruta: str) -> int:
    archivo = None
    try:
        archivo = open(ruta, "r", encoding="utf-8")
    except FileNotFoundError:
        print(f"❌ El archivo '{ruta}' no existe.")
        return -1
    except PermissionError:
        print(f"❌ Sin permisos para leer '{ruta}'.")
        return -1
    else:
        # Solo se ejecuta si el archivo se abrió sin errores
        lineas = archivo.readlines()
        total = len(lineas)
        print(f"✅ Archivo leído correctamente. Total de líneas: {total}")
        return total
    finally:
        # Siempre se ejecuta: cierra el archivo y muestra mensaje final
        if archivo:
            archivo.close()
            print("🔒 Archivo cerrado.")
        print("🏁 Operación finalizada.")


ruta = input("Ingresa la ruta del archivo: ")
contar_lineas(ruta)
