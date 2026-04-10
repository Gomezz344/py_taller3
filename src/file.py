import json
import os
from typing import List, Dict, Any

FILE_PATH = "data/registros.json"


def load_data() -> List[Dict[str, Any]]:
    """
    Lee los datos persistidos desde el archivo JSON de la base de datos.
    Crea el directorio 'data' si no existe.

    Returns:
        List[Dict[str, Any]]: Lista de diccionarios con la información de usuarios.
                              Retorna lista vacía si hay un error o el archivo no existe.
    """
    os.makedirs("data", exist_ok=True)
    try:
        with open(FILE_PATH, "r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
            print("Advertencia: el contenido JSON no es una lista. Se usará lista vacía.")
            return []
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("Advertencia: el archivo de datos está dañado. Se usará lista vacía.")
        return []
    except OSError as error:
        print(f"Advertencia: no se pudo leer el archivo de datos ({error}).")
        return []


def save_data(data: List[Dict[str, Any]]) -> None:
    """
    Guarda la lista de datos en el archivo JSON.
    Crea el directorio 'data' si no existe.

    Args:
        data (List[Dict[str, Any]]): Lista de diccionarios con información de usuarios.
    """
    os.makedirs("data", exist_ok=True)
    try:
        with open(FILE_PATH, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    except OSError as error:
        print(f"Error al guardar datos en archivo: {error}")