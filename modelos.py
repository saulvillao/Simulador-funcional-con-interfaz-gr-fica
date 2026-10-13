"""Capa de datos: estructuras inmutables que representan el estado del juego.

Aquí NO hay lógica ni widgets, solo modelado de datos con dataclass congeladas.
Al ser `frozen=True`, cualquier intento de modificar un campo lanza un error;
para "cambiar" algo hay que crear una copia nueva con `dataclasses.replace`.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Entidad:
    nombre: str
    tipo: str  # "HEROE" o "ENEMIGO"
    hp: int
    max_hp: int
    ataque: int
    defensa: int
    nivel: int


@dataclass(frozen=True)
class EstadoJuego:
    jugador: Entidad
    enemigo: Entidad
    historial: tuple[str, ...]
    # Turnos que faltan para poder usar de nuevo la habilidad especial.
    espera_especial: int = 0
