from datetime import date

import pytest
from fastapi.testclient import TestClient

from app.main import app, calculadora

cliente = TestClient(app)


def test_calcula_el_total_de_un_pedido():
    respuesta = cliente.post("/api/pedidos/total", json=[
        {"codigo": "TINTO", "cantidad": 2},
        {"codigo": "PANDEBONO", "cantidad": 1},
    ])

    assert respuesta.status_code == 200
    assert respuesta.json()["total"] == 9500


def test_pedido_vacio_responde_400():
    respuesta = cliente.post("/api/pedidos/total", json=[])

    assert respuesta.status_code == 400
    assert respuesta.json() == {"detail": "El pedido no tiene productos"}


def test_api_aplica_la_promocion_del_martes(monkeypatch):
    monkeypatch.setattr(calculadora, "hoy", lambda: date(2026, 11, 3))
    respuesta = cliente.post("/api/pedidos/total", json=[
        {"codigo": "CAFE_CASA", "cantidad": 1},
    ])

    assert respuesta.status_code == 200
    assert respuesta.json() == {"subtotal": 16_000, "descuento": 0, "total": 16_000}


def test_api_conserva_el_precio_si_el_pedido_cruza_la_medianoche(monkeypatch):
    fechas = iter([date(2026, 11, 2), date(2026, 11, 3)])
    monkeypatch.setattr(calculadora, "hoy", lambda: next(fechas))
    respuesta = cliente.post("/api/pedidos/total", json=[
        {"codigo": "CAFE_CASA", "cantidad": 1},
        {"codigo": "CAFE_CASA", "cantidad": 1},
    ])

    assert respuesta.status_code == 200
    assert respuesta.json() == {"subtotal": 64_000, "descuento": 6_400, "total": 57_600}


def test_api_aplica_cafe10_despues_de_la_promocion_y_r3(monkeypatch):
    monkeypatch.setattr(calculadora, "hoy", lambda: date(2026, 11, 3))
    respuesta = cliente.post("/api/pedidos/total", params={"cupon": "CAFE10"}, json=[
        {"codigo": "CAFE_CASA", "cantidad": 2},
        {"codigo": "TINTO", "cantidad": 6},
    ])

    assert respuesta.status_code == 200
    assert respuesta.json() == {"subtotal": 50_000, "descuento": 15_000, "total": 35_000}


def test_api_no_deja_total_negativo_con_el_cupon():
    respuesta = cliente.post("/api/pedidos/total", params={"cupon": "CAFE10"}, json=[
        {"codigo": "TINTO", "cantidad": 2},
        {"codigo": "PANDEBONO", "cantidad": 1},
    ])

    assert respuesta.status_code == 200
    assert respuesta.json() == {"subtotal": 9_500, "descuento": 9_500, "total": 0}


def test_api_rechaza_un_cupon_desconocido():
    respuesta = cliente.post("/api/pedidos/total", params={"cupon": "ABC"}, json=[
        {"codigo": "TINTO", "cantidad": 2},
    ])

    assert respuesta.status_code == 400
    assert respuesta.json() == {"detail": "Cupón inválido"}


def test_api_acepta_diez_unidades_repartidas_en_lineas():
    respuesta = cliente.post("/api/pedidos/total", json=[
        {"codigo": "TINTO", "cantidad": 6},
        {"codigo": "TINTO", "cantidad": 4},
    ])

    assert respuesta.status_code == 200
    assert respuesta.json() == {"subtotal": 30_000, "descuento": 0, "total": 30_000}


@pytest.mark.parametrize("cantidades", [(11,), (6, 5)])
def test_api_rechaza_mas_de_diez_unidades_por_producto(cantidades):
    respuesta = cliente.post("/api/pedidos/total", json=[
        {"codigo": "TINTO", "cantidad": cantidad} for cantidad in cantidades
    ])

    assert respuesta.status_code == 400
    assert respuesta.json() == {"detail": "Máximo 10 unidades de TINTO"}
