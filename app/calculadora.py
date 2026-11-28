from dataclasses import dataclass
from datetime import date, datetime
from typing import Callable
from zoneinfo import ZoneInfo

from app import menu

UMBRAL_DESCUENTO = 50_000
CODIGO_CUPON = "CAFE10"
DESCUENTO_CUPON = 10_000
MAXIMO_POR_PRODUCTO = 10
CAFE_DE_LA_CASA = "CAFE_CASA"
MARTES = 1  # date.weekday(): lunes = 0, martes = 1


class PedidoInvalido(Exception):
    pass


@dataclass(frozen=True)
class Item:
    codigo: str
    cantidad: int


@dataclass(frozen=True)
class Resumen:
    subtotal: int
    descuento: int
    total: int


def hoy_en_bogota() -> date:
    return datetime.now(ZoneInfo("America/Bogota")).date()


class CalculadoraPedido:
    def __init__(self, hoy: Callable[[], date] = hoy_en_bogota):
        self.hoy = hoy

    def calcular(self, items: list[Item], cupon: str | None = None) -> Resumen:
        if not items:
            raise PedidoInvalido("El pedido no tiene productos")
        es_martes = self.hoy().weekday() == MARTES
        subtotal = 0
        cantidades: dict[str, int] = {}
        for item in items:
            if item.cantidad < 1:
                raise PedidoInvalido(f"Cantidad inválida para {item.codigo}")
            producto = menu.buscar(item.codigo)
            if producto is None:
                raise PedidoInvalido(f"No existe el producto {item.codigo}")
            acumulado = cantidades.get(item.codigo, 0) + item.cantidad
            if acumulado > MAXIMO_POR_PRODUCTO:
                raise PedidoInvalido(
                    f"Máximo {MAXIMO_POR_PRODUCTO} unidades de {item.codigo}"
                )
            cantidades[item.codigo] = acumulado
            subtotal += self._precio_del_dia(producto, es_martes) * item.cantidad
        descuento = subtotal // 10 if subtotal >= UMBRAL_DESCUENTO else 0
        if cupon is not None:
            if cupon != CODIGO_CUPON:
                raise PedidoInvalido("Cupón inválido")
            descuento += min(DESCUENTO_CUPON, subtotal - descuento)
        return Resumen(subtotal, descuento, subtotal - descuento)

    @staticmethod
    def _precio_del_dia(producto: menu.Producto, es_martes: bool) -> int:
        if es_martes and producto.codigo == CAFE_DE_LA_CASA:
            return producto.precio // 2
        return producto.precio
