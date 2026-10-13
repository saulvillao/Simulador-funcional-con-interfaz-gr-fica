"""Capa lógica: reglas del dominio.

Todo lo que hay en este módulo es PURO: no imprime, no lee archivos, no toca
widgets y no muta nada. Cada función recibe datos y devuelve datos nuevos.
"""

from dataclasses import replace
from functools import reduce
from typing import Callable

from modelos import Entidad, EstadoJuego

CURACION_POCION = 15
MULTIPLICADOR_CRITICO = 1.75
ESPERA_ESPECIAL = 3


# ---------------------------------------------------------------------------
# Estado inicial
# ---------------------------------------------------------------------------
def estado_inicial() -> EstadoJuego:
    """Función pura: siempre devuelve el mismo estado de arranque."""
    return EstadoJuego(
        jugador=Entidad(
            nombre="Guerrero Funcional",
            tipo="HEROE",
            hp=100,
            max_hp=100,
            ataque=25,
            defensa=10,
            nivel=1,
        ),
        enemigo=Entidad(
            nombre="Bug Monstruoso",
            tipo="ENEMIGO",
            hp=80,
            max_hp=80,
            ataque=20,
            defensa=8,
            nivel=1,
        ),
        historial=(
            "¡Comienza el combate en la Arena Funcional!",
            "Sistema inicializado con inmutabilidad y Dataclasses.",
        ),
    )


# ---------------------------------------------------------------------------
# Funciones puras básicas
# ---------------------------------------------------------------------------
def calcular_danio_puro(atacante: Entidad, defensor: Entidad) -> int:
    """Pura: mismo atacante y defensor -> mismo daño, sin efectos externos."""
    danio_base = atacante.ataque - (defensor.defensa // 2)
    return max(1, danio_base)


def actualizar_hp(entidad: Entidad, nuevo_hp: int) -> Entidad:
    """Pura: devuelve una Entidad NUEVA con el HP acotado entre 0 y max_hp."""
    hp_acotado = max(0, min(nuevo_hp, entidad.max_hp))
    return replace(entidad, hp=hp_acotado)


def agregar_evento(estado: EstadoJuego, mensaje: str) -> EstadoJuego:
    """Pura: devuelve un estado con una tupla de historial nueva (no append)."""
    return replace(estado, historial=estado.historial + (mensaje,))


def reducir_espera(estado: EstadoJuego) -> EstadoJuego:
    """Pura: baja en uno el contador de la habilidad especial (mínimo 0)."""
    return replace(
        estado, espera_especial=max(0, estado.espera_especial - 1)
    )


def generar_reporte_historial(historial: tuple[str, ...]) -> str:
    """Pura: convierte el historial en texto usando map + reduce.

    - `map` recibe una lambda y le da formato de viñeta a cada línea.
    - `reduce` recibe otra lambda y acumula las líneas en un solo texto.
    """
    if not historial:
        return "Sin acciones registradas."
    lineas = map(lambda linea: f"• {linea}", historial)
    return reduce(lambda acumulado, linea: f"{acumulado}\n{linea}", lineas)


# ---------------------------------------------------------------------------
# Enfoque funcional vs. imperativo (evidencia ejecutable en
# comparacion_imperativo_vs_funcional.py). Resumen:
#
#   Imperativo (NO usado):            Funcional (usado arriba):
#     texto = ""                        lineas = map(lambda l: f"• {l}", h)
#     for linea in historial:           reduce(lambda a, l: f"{a}\n{l}", lineas)
#         texto += f"• {linea}\n"
#
# El imperativo muta la variable `texto` en cada vuelta del bucle; el funcional
# no modifica nada: transforma la tupla y produce un resultado nuevo.
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Closure: función de orden superior que DEVUELVE otra función
# ---------------------------------------------------------------------------
def crear_multiplicador_danio(
    factor: float,
) -> Callable[[Entidad, Entidad], int]:
    """Fábrica de cálculos de daño configurados con un multiplicador.

    `calcular` es un closure: recuerda `factor` del ámbito léxico de la función
    externa aunque ésta ya haya terminado de ejecutarse.
    """

    def calcular(atacante: Entidad, defensor: Entidad) -> int:
        danio_base = atacante.ataque - defensor.defensa
        return max(2, int(danio_base * factor))

    return calcular


# El closure se crea UNA vez con su factor y se reutiliza.
calcular_danio_critico = crear_multiplicador_danio(MULTIPLICADOR_CRITICO)


# ---------------------------------------------------------------------------
# Pattern matching
# ---------------------------------------------------------------------------
def accion_disponible(accion: str, estado: EstadoJuego) -> bool:
    """Pura: indica si el jugador puede usar la acción en este estado."""
    match accion:
        case "ATACAR_BASICO" | "CURAR":
            return True
        case "HABILIDAD_ESPECIAL":
            return estado.espera_especial == 0
        case _:
            return False


def determinar_resultado(estado: EstadoJuego) -> str:
    """Pura: usa match sobre una tupla (hp jugador, hp enemigo) con guardas."""
    match (estado.jugador.hp, estado.enemigo.hp):
        case (_, hp_enemigo) if hp_enemigo <= 0:
            return "VICTORIA"
        case (hp_jugador, _) if hp_jugador <= 0:
            return "DERROTA"
        case _:
            return "EN_CURSO"


def registrar_resultado(estado: EstadoJuego) -> EstadoJuego:
    """Pura: si la partida terminó, agrega el evento final al historial."""
    match determinar_resultado(estado):
        case "VICTORIA":
            return agregar_evento(
                estado, f"¡Victoria! {estado.enemigo.nombre} ha sido derrotado."
            )
        case "DERROTA":
            return agregar_evento(
                estado, f"Derrota... {estado.jugador.nombre} ha caído."
            )
        case _:
            return estado


def procesar_accion_juego(accion: str, estado: EstadoJuego) -> EstadoJuego:
    """Pura: aplica UNA acción y devuelve un EstadoJuego nuevo."""
    match accion:
        case "ATACAR_BASICO":
            danio = calcular_danio_puro(estado.jugador, estado.enemigo)
            enemigo = actualizar_hp(estado.enemigo, estado.enemigo.hp - danio)
            return agregar_evento(
                replace(estado, enemigo=enemigo),
                f"{estado.jugador.nombre} atacó a {enemigo.nombre} causando"
                f" {danio} de daño.",
            )

        case "CURAR":
            jugador = actualizar_hp(
                estado.jugador, estado.jugador.hp + CURACION_POCION
            )
            return agregar_evento(
                replace(estado, jugador=jugador),
                f"{estado.jugador.nombre} usó poción y recuperó"
                f" {CURACION_POCION} HP.",
            )

        case "HABILIDAD_ESPECIAL":
            # Se usa el closure creado arriba con el factor 1.75.
            danio = calcular_danio_critico(estado.jugador, estado.enemigo)
            enemigo = actualizar_hp(estado.enemigo, estado.enemigo.hp - danio)
            return agregar_evento(
                replace(
                    estado, enemigo=enemigo, espera_especial=ESPERA_ESPECIAL
                ),
                f"¡Habilidad Crítica! {estado.jugador.nombre} golpeó a"
                f" {enemigo.nombre} por {danio} de daño.",
            )

        case "TURNO_ENEMIGO":
            if estado.enemigo.hp <= 0:
                return estado
            danio = calcular_danio_puro(estado.enemigo, estado.jugador)
            jugador = actualizar_hp(estado.jugador, estado.jugador.hp - danio)
            return agregar_evento(
                replace(estado, jugador=jugador),
                f"{estado.enemigo.nombre} contraatacó a {jugador.nombre}"
                f" causando {danio} de daño.",
            )

        case _:
            return estado


def resolver_turno(accion: str, estado: EstadoJuego) -> EstadoJuego:
    """Pura: resuelve un turno completo (jugador + enemigo + fin de partida).

    Esta función concentra las decisiones del dominio para que el callback del
    botón solo tenga que llamarla y refrescar la pantalla.
    """
    if determinar_resultado(estado) != "EN_CURSO":
        return estado
    if not accion_disponible(accion, estado):
        return estado

    tras_jugador = procesar_accion_juego(accion, reducir_espera(estado))
    tras_enemigo = procesar_accion_juego("TURNO_ENEMIGO", tras_jugador)
    return registrar_resultado(tras_enemigo)


# ---------------------------------------------------------------------------
# Por qué NO conviene usar lambda aquí:
# `procesar_accion_juego` y `resolver_turno` necesitan varias líneas, un
# `match/case` con varias ramas, variables intermedias (danio, enemigo) y
# docstring. Una lambda solo admite UNA expresión: no permite `match`, ni
# asignaciones, ni `if` con bloques. Forzarlo en una lambda sería ilegible y
# no se podría documentar ni probar. Las lambdas se reservan para
# transformaciones de una línea (el `map` y el `reduce` de arriba, y los
# callbacks de los botones).
# ---------------------------------------------------------------------------
