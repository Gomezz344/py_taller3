# Ejercicio 6: Refactor de procesamiento de ventas
# Separar lógica de cálculo, lógica de lista e impresión (I/O)

# ── Datos de prueba ───────────────────────────────────────────────────────────
ventas = [
    {"status": "ok",  "price": 100, "qty": 5,  "customer": "regular"},
    {"status": "ok",  "price": 50,  "qty": 10, "customer": "regular"},
    {"status": "ok",  "price": 200, "qty": 10, "customer": "vip"},
    {"status": "bad", "price": 99,  "qty": 1,  "customer": "regular"},  # inválida
    {"status": "bad", "price": 30,  "qty": 3,  "customer": "vip"},      # inválida
]


def calculate_discount(qty: int, customer: str) -> float:
    """
    Retorna el porcentaje de descuento como decimal.
    - qty >= 10      → 10% (0.10)
    - customer "vip" → +5% adicional (0.05)
    """
    discount = 0.0

    if qty >= 10:
        discount = 0.10

    if customer == "vip":
        discount += 0.05      # suma sobre el descuento anterior, no lo reemplaza

    return discount


# ── 2. Calcula el total de UNA venta ─────────────────────────────────────────
def calculate_sale_total(sale: dict) -> float:
    """
    Recibe una venta (dict) y retorna su subtotal con descuento aplicado.
    No imprime nada, no valida status — solo calcula.
    """
    price    = sale["price"]
    qty      = sale["qty"]
    customer = sale["customer"]

    subtotal = price * qty                        # precio bruto sin descuento
    discount = calculate_discount(qty, customer)  # delega el cálculo del descuento

    return subtotal - (subtotal * discount)       # precio final con descuento


# ── 3. Suma todas las ventas válidas ──────────────────────────────────────────
def calculate_total(sales: list[dict]) -> float:
    """
    Recorre la lista de ventas, ignora las que no son 'ok'
    y retorna la suma total de las válidas.
    """
    total = 0.0

    for sale in sales:
        if sale["status"] == "ok":
            total += calculate_sale_total(sale)   # acumula solo las válidas

    return total


# ── 4. Muestra las ventas inválidas (solo I/O, sin cálculos) ──────────────────
def report_invalid_sales(sales: list[dict]) -> None:
    """Imprime las ventas con status diferente a 'ok'. No calcula nada."""

    invalidas = [sale for sale in sales if sale["status"] != "ok"]

    if not invalidas:
        print("✅ No hay ventas inválidas.")
        return

    print(f"⚠️  Ventas inválidas encontradas: {len(invalidas)}")
    for sale in invalidas:
        print(f"   ❌ {sale}")


# ── 5. Comparador de decimales ────────────────────────────────────────────────
def valores_iguales(a: float, b: float) -> bool:
    # 0.10 + 0.05 en Python da 0.15000000000000002 (error de punto flotante)
    # redondear a 10 decimales soluciona la comparación
    return round(a, 10) == round(b, 10)


# ── 6. Pruebas unitarias (patrón AAA) ─────────────────────────────────────────
def correr_pruebas():
    print("═" * 50)
    print("  PRUEBAS UNITARIAS")
    print("═" * 50)

    # Arrange: preparar los datos de entrada de cada caso
    venta_simple   = {"status": "ok", "price": 100, "qty": 5,  "customer": "regular"}
    venta_cantidad = {"status": "ok", "price": 100, "qty": 10, "customer": "regular"}
    venta_vip      = {"status": "ok", "price": 100, "qty": 10, "customer": "vip"}
    venta_vip_poco = {"status": "ok", "price": 50,  "qty": 5,  "customer": "vip"}

    # (resultado_real, valor_esperado, descripcion del caso)
    casos = [
        (calculate_sale_total(venta_simple),   500.0, "sin descuento: 100×5 = 500"),
        (calculate_sale_total(venta_cantidad), 900.0, "10% descuento: 1000 - 100 = 900"),
        (calculate_sale_total(venta_vip),      850.0, "15% descuento: 1000 - 150 = 850"),
        (calculate_sale_total(venta_vip_poco), 237.5, "5% vip: 250 - 12.5 = 237.5"),
        (calculate_discount(5,  "regular"),    0.0,   "sin descuento"),
        (calculate_discount(10, "regular"),    0.10,  "solo descuento por cantidad"),
        (calculate_discount(5,  "vip"),        0.05,  "solo descuento vip"),
        (calculate_discount(10, "vip"),        0.15,  "cantidad + vip = 15%"),
    ]

    aprobadas = 0
    for resultado, esperado, desc in casos:
        # Assert: compara lo que dio la función con lo que esperábamos
        paso = valores_iguales(resultado, esperado)
        aprobadas += paso
        print(f"{'✅ PASS' if paso else '❌ FAIL'} | {desc}")
        if not paso:
            print(f"         ↳ esperado: {esperado}, obtenido: {resultado}")

    print("═" * 50)
    print(f"  Resultado: {aprobadas}/{len(casos)} pruebas aprobadas")
    print("═" * 50)


# ── Programa principal ────────────────────────────────────────────────────────
correr_pruebas()
print()
report_invalid_sales(ventas)
print()
print(f"💰 TOTAL DE VENTAS VÁLIDAS: ${calculate_total(ventas):.2f}")
