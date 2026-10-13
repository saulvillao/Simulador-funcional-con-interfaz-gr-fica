"""Pruebas de la capa lógica (no requieren interfaz gráfica).

Ejecutar con: python pruebas.py
"""

from dataclasses import FrozenInstanceError, replace

from logica import (
    actualizar_hp,
    calcular_danio_puro,
    crear_multiplicador_danio,
    determinar_resultado,
    estado_inicial,
    generar_reporte_historial,
    resolver_turno,
)


def probar_inmutabilidad() -> None:
    estado = estado_inicial()
    try:
        estado.jugador.hp = 0  # type: ignore[misc]
    except FrozenInstanceError:
        pass
    else:
        raise AssertionError("La dataclass debería ser inmutable")

    copia = estado
    resolver_turno("ATACAR_BASICO", estado)
    assert estado == copia, "resolver_turno no debe mutar el estado original"


def probar_funciones_puras() -> None:
    estado = estado_inicial()
    assert calcular_danio_puro(estado.jugador, estado.enemigo) == 21
    assert calcular_danio_puro(estado.enemigo, estado.jugador) == 15
    assert actualizar_hp(estado.jugador, 500).hp == estado.jugador.max_hp
    assert actualizar_hp(estado.jugador, -5).hp == 0
    assert generar_reporte_historial(()) == "Sin acciones registradas."
    assert generar_reporte_historial(("a", "b")) == "• a\n• b"


def probar_closure() -> None:
    estado = estado_inicial()
    doble = crear_multiplicador_danio(2.0)
    critico = crear_multiplicador_danio(1.75)
    assert doble(estado.jugador, estado.enemigo) == 34
    assert critico(estado.jugador, estado.enemigo) == 29


def probar_turno_basico() -> None:
    nuevo = resolver_turno("ATACAR_BASICO", estado_inicial())
    assert nuevo.enemigo.hp == 59
    assert nuevo.jugador.hp == 85
    assert len(nuevo.historial) == 4


def probar_habilidad_especial_y_espera() -> None:
    estado = resolver_turno("HABILIDAD_ESPECIAL", estado_inicial())
    assert estado.enemigo.hp == 51
    assert estado.espera_especial == 3

    # Mientras está en espera, el turno no se consume.
    assert resolver_turno("HABILIDAD_ESPECIAL", estado) == estado

    for esperado in (2, 1, 0):
        estado = resolver_turno("CURAR", estado)
        assert estado.espera_especial == esperado

    estado = resolver_turno("HABILIDAD_ESPECIAL", estado)
    assert estado.espera_especial == 3


def probar_fin_de_partida() -> None:
    base = estado_inicial()

    casi_ganado = replace(base, enemigo=replace(base.enemigo, hp=1))
    victoria = resolver_turno("ATACAR_BASICO", casi_ganado)
    assert determinar_resultado(victoria) == "VICTORIA"
    assert victoria.historial[-1].startswith("¡Victoria!")
    assert victoria.jugador.hp == base.jugador.hp  # el enemigo muerto no ataca
    assert resolver_turno("CURAR", victoria) == victoria

    casi_perdido = replace(base, jugador=replace(base.jugador, hp=1))
    derrota = resolver_turno("ATACAR_BASICO", casi_perdido)
    assert determinar_resultado(derrota) == "DERROTA"
    assert derrota.historial[-1].startswith("Derrota")
    assert resolver_turno("ATACAR_BASICO", derrota) == derrota


if __name__ == "__main__":
    pruebas = (
        probar_inmutabilidad,
        probar_funciones_puras,
        probar_closure,
        probar_turno_basico,
        probar_habilidad_especial_y_espera,
        probar_fin_de_partida,
    )
    for prueba in pruebas:
        prueba()
        print(f"OK  {prueba.__name__}")
    print("Todas las pruebas pasaron.")
