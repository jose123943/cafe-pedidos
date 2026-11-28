from datetime import UTC, date, datetime

import pytest

from app import calculadora as modulo_calculadora
from app.calculadora import CalculadoraPedido, Item, PedidoInvalido, Resumen

# Día fijo: lunes 2 de noviembre de 2026.
# Así la prueba da el mismo resultado cualquier día que se ejecute.
LUNES = date(2026, 11, 2)
calculadora = CalculadoraPedido(hoy=lambda: LUNES)


def test_suma_precio_por_cantidad():  # R1
    r = calculadora.calcular([Item("TINTO", 2), Item("PANDEBONO", 1)])

    assert r.subtotal == 9_500
    assert r.descuento == 0
    assert r.total == 9_500


def test_pedido_vacio_es_invalido():  # R2
    with pytest.raises(PedidoInvalido, match="no tiene productos"):
        calculadora.calcular([])


def test_cantidad_cero_es_invalida():  # R2
    with pytest.raises(PedidoInvalido):
        calculadora.calcular([Item("TINTO", 0)])


def test_producto_inexistente_es_invalido():
    with pytest.raises(PedidoInvalido, match="TE_VERDE"):
        calculadora.calcular([Item("TE_VERDE", 1)])


def test_justo_en_el_umbral_hay_descuento():  # R3: 50.000 exactos
    r = calculadora.calcular([
        Item("CAFE_CASA", 1),   # 32.000
        Item("CAPUCHINO", 2),   # 15.000
        Item("TINTO", 1),       #  3.000
    ])

    assert r.subtotal == 50_000
    assert r.descuento == 5_000
    assert r.total == 45_000


def test_poco_antes_del_umbral_no_hay_descuento():  # R3: 49.500
    r = calculadora.calcular([
        Item("CAFE_CASA", 1),   # 32.000
        Item("PANDEBONO", 5),   # 17.500
    ])

    assert r.subtotal == 49_500
    assert r.descuento == 0


def test_cafe10_se_acumula_despues_del_descuento_r3():
    resumen = calculadora.calcular([
        Item("CAFE_CASA", 1),
        Item("CAPUCHINO", 2),
        Item("TINTO", 1),
    ], cupon="CAFE10")

    assert resumen.subtotal == 50_000
    assert resumen.descuento == 15_000
    assert resumen.total == 35_000


@pytest.mark.parametrize(("items", "subtotal"), [
    ([Item("TINTO", 2), Item("PANDEBONO", 1)], 9_500),
    ([Item("TINTO", 1), Item("PANDEBONO", 2)], 10_000),
])
def test_cafe10_no_descuenta_mas_que_el_valor_del_pedido(items, subtotal):
    resumen = calculadora.calcular(items, cupon="CAFE10")

    assert resumen.subtotal == subtotal
    assert resumen.descuento == subtotal
    assert resumen.total == 0


@pytest.mark.parametrize("cupon", ["ABC", ""])
def test_un_cupon_desconocido_es_invalido(cupon):
    with pytest.raises(PedidoInvalido, match="^Cupón inválido$"):
        calculadora.calcular([Item("TINTO", 2)], cupon=cupon)


def test_el_pedido_sin_cupon_conserva_su_total():
    resumen = calculadora.calcular([Item("TINTO", 2)], cupon=None)

    assert resumen.subtotal == 6_000
    assert resumen.descuento == 0
    assert resumen.total == 6_000


# --- Parte 5: HU-R4 ---
MARTES = date(2026, 11, 3)
calculadora_martes = CalculadoraPedido(hoy=lambda: MARTES)


def test_el_martes_el_cafe_de_la_casa_cuesta_la_mitad():  # R4
    r = calculadora_martes.calcular([Item("CAFE_CASA", 1)])
    assert r.subtotal == 16_000


def test_el_martes_los_demas_productos_no_cambian():  # R4
    r = calculadora_martes.calcular([Item("TINTO", 2)])
    assert r.subtotal == 6_000


def test_el_lunes_el_cafe_de_la_casa_tiene_precio_normal():  # R4
    r = calculadora.calcular([Item("CAFE_CASA", 1)])
    assert r.subtotal == 32_000


def test_el_descuento_r3_se_calcula_sobre_el_precio_del_martes():  # R3 + R4
    r = calculadora_martes.calcular([Item("CAFE_CASA", 2)])
    assert r.subtotal == 32_000   # 2 x 16.000
    assert r.descuento == 0       # ya no llega a 50.000


def test_el_umbral_r3_se_alcanza_con_el_subtotal_promocional():
    resumen = calculadora_martes.calcular([Item("CAFE_CASA", 2), Item("TINTO", 6)])

    assert resumen == Resumen(subtotal=50_000, descuento=5_000, total=45_000)


def test_la_promocion_usa_el_dia_de_bogota_cuando_en_utc_es_martes(monkeypatch):
    class FechaFija(datetime):
        @classmethod
        def now(cls, tz=None):
            martes_utc = datetime(2026, 11, 3, 2, tzinfo=UTC)
            return martes_utc.astimezone(tz or UTC)

    monkeypatch.setattr(modulo_calculadora, "datetime", FechaFija)

    assert CalculadoraPedido().calcular([Item("CAFE_CASA", 1)]).subtotal == 32_000


def test_todas_las_lineas_usan_el_mismo_dia_si_el_pedido_cruza_la_medianoche():
    fechas = iter([LUNES, MARTES])
    calculadora_medianoche = CalculadoraPedido(hoy=lambda: next(fechas))

    resumen = calculadora_medianoche.calcular([
        Item("CAFE_CASA", 1),
        Item("CAFE_CASA", 1),
    ])

    assert resumen == Resumen(subtotal=64_000, descuento=6_400, total=57_600)
