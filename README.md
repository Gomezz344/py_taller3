## 📘 Título y Descripción

**Sistema de Gestión de Usuarios** — Aplicación de consola en Python que permite
crear, listar, buscar, actualizar y eliminar usuarios, con persistencia en archivo JSON.
Incluye generación automática de registros falsos usando la librería **Faker**.

---

## 🗂️ Estructura del proyecto

```bash
gestion-info/
├─ README.md
├─ requirements.txt
├─ .gitignore
├─ data/
│  └─ registros.json              # datos persistidos (se genera automáticamente)
└─ src/
      ├─ main.py                  # punto de entrada
      ├─ menu.py                  # interfaz de consola (UI)
      ├─ service.py               # lógica (CRUD)
      ├─ file.py                  # persistencia (leer/guardar)
      ├─ validate.py              # validaciones y helpers
      └─ integration.py           # generación con Faker + pruebas de integración
```

---

## ▶️ Instalación

1. **Clonar el repositorio:**

```bash
git clone <url-del-repositorio>
cd gestion-info
```

2. **Instalar dependencias:**

```bash
pip install -r requirements.txt
```

> Las dependencias incluyen `faker` (generación de datos falsos) y `colorama` (colores en consola).

3. **Ejecutar la aplicación:**

```bash
cd src
python main.py
```

---

## 🚀 Funcionalidades

| Opción | Descripción |
|--------|-------------|
| 1      | **Crear usuario** — Registra un nuevo usuario con ID, nombre, correo, edad y estado |
| 2      | **Listar usuarios** — Muestra todos los usuarios ordenados alfabéticamente |
| 3      | **Buscar usuario** — Búsqueda parcial por cualquier campo (id, name, email, age, status) |
| 4      | **Actualizar usuario** — Modifica campos individuales de un usuario existente |
| 5      | **Eliminar usuario** — Borra un usuario por su ID |
| 6      | **Generar registros falsos (Faker)** — Crea 10 usuarios aleatorios con datos realistas en español |
| 0      | **Salir** — Guarda los datos y cierra la aplicación |

---

## 🔧 Uso de `*args` y `**kwargs`

En el archivo `integration.py` se usan `*args` y `**kwargs` para crear funciones genéricas
de generación de datos:

### `crear_registro(**kwargs)`

Construye un diccionario de usuario. Acepta campos arbitrarios como argumentos con nombre;
los campos que no se proporcionen se generan automáticamente con Faker.

```python
# Genera un registro completamente aleatorio
registro = crear_registro()

# Genera un registro con estado fijo, el resto aleatorio
registro = crear_registro(status="Activo")

# Genera un registro con valores específicos
registro = crear_registro(name="Ana López", age="30")
```

### `generar_registros_falsos(*args, **kwargs)`

Genera y registra N usuarios falsos en el sistema.
- `*args`: el primer argumento posicional indica la cantidad de registros (por defecto 10).
- `**kwargs`: campos fijos que se aplican a todos los registros generados.

```python
# Genera 10 registros completamente aleatorios (por defecto)
creados, errores = generar_registros_falsos()

# Genera 5 registros, todos con estado "Activo"
creados, errores = generar_registros_falsos(5, status="Activo")
```

---

## 🧪 Pruebas de integración

Ejecutar las pruebas automatizadas:

```bash
cd src
python integration.py
```

Verifica las 5 operaciones CRUD y la persistencia en archivo.

---

## Créditos/Autores
Emmanuel Gómez Vélez

Proyecto desarrollado como taller académico.
