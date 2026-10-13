# Simulador Funcional con Interfaz Gráfica — Arena Funcional

Actividad integradora de Programación Funcional (Unidades 1 y 2).
Requiere **Python 3.10 o superior** (por `match/case`) y Tkinter.

## Cómo ejecutarlo

```bash
pip install -r requirements.txt
python main.py                                   # abre la aplicación
python pruebas.py                                # pruebas de la lógica (sin interfaz)
python comparacion_imperativo_vs_funcional.py    # evidencia imperativo vs. funcional
```

## Estructura (una capa por archivo)

| Archivo | Capa | Contenido |
|---|---|---|
| `modelos.py` | Datos / estado | `Entidad` y `EstadoJuego` (dataclass congeladas) |
| `logica.py` | Lógica (todo puro) | cálculo de daño, `match/case`, closure, `map` + `reduce`, `resolver_turno` |
| `interfaz.py` | Visual (efectos secundarios) | Tkinter + ttkbootstrap, `actualizar_vista`, `registrar_log_externo` |
| `main.py` | Arranque | crea la ventana |
| `pruebas.py` | Pruebas | verifica pureza, inmutabilidad, closure y fin de partida |
| `comparacion_imperativo_vs_funcional.py` | Evidencia Unidad 1 | mismo reporte hecho con bucle y con `map` + `reduce` |
| `analisis-funcional.md` | Entregable | documento de análisis |
| `bitacora-ia.md` | Entregable | bitácora de uso de IA |

## Cómo se juega
Elige una acción: atacar, usar poción o habilidad especial (tiene recarga de 3 turnos). Después de cada acción el enemigo contraataca. La partida termina cuando uno de los dos llega a 0 HP; "Nueva partida" reinicia el combate.
