"""Evidencia del enfoque imperativo vs. funcional (Unidad 1).

Genera el mismo reporte de historial de dos maneras y comprueba que el
resultado es idéntico. Ejecutar con: python comparacion_imperativo_vs_funcional.py
"""

from logica import generar_reporte_historial

HISTORIAL = (
    "Comienza el combate.",
    "El héroe atacó al enemigo.",
    "El enemigo contraatacó.",
)


def reporte_imperativo(historial: tuple[str, ...]) -> str:
    """Imperativo: una variable acumuladora que se MUTA dentro de un bucle."""
    texto = ""
    for linea in historial:
        if texto:
            texto += "\n"
        texto += f"• {linea}"
    return texto or "Sin acciones registradas."


if __name__ == "__main__":
    imperativo = reporte_imperativo(HISTORIAL)
    funcional = generar_reporte_historial(HISTORIAL)

    print("--- Imperativo (bucle + variable mutable) ---")
    print(imperativo)
    print("\n--- Funcional (map + reduce, sin mutar nada) ---")
    print(funcional)

    assert imperativo == funcional
    print("\nAmbos enfoques producen exactamente el mismo resultado.")
