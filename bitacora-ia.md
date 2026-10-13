# Bitácora de Uso de Inteligencia Artificial

## Prompts usados
1. *"Sugiere una estructura de proyecto en Python con Tkinter y Ttk-Bootstrap para una Arena Funcional que cumpla con programación funcional estricta."*
2. *"¿Cómo puedo implementar un closure y match/case en Python aplicados a un sistema de combate por turnos?"*
3. *"Muestra un ejemplo de uso de reduce para concatenar tuplas inmutables en un historial de texto."*
4. *"Mira ese pdf (la guía de la actividad) y dime si cumple mi programa."*
5. *"Haz todas las correcciones y dame el trabajo en un zip bien hecho."*

## Fragmentos sugeridos por IA
- Estructura inicial con clases `dataclass` y una clase de `tkinter` que contiene la interfaz:

  ```python
  @dataclass(frozen=True)
  class Entidad:
      nombre: str
      hp: int
      ...
  ```
- Sintaxis de `match/case` para manejar las acciones del usuario:

  ```python
  match accion:
      case "ATACAR_BASICO": ...
      case "CURAR": ...
      case _: return estado
  ```
- Closure para el multiplicador de daño:

  ```python
  def crear_multiplicador_danio(factor):
      def calcular(atacante, defensor):
          return max(2, int((atacante.ataque - defensor.defensa) * factor))
      return calcular
  ```
- Patrón genérico de historial con lista mutable (el que se rechazó):

  ```python
  historial.append(mensaje)   # muta la lista
  ```
- Revisión final (prompts 4 y 5): la IA señaló que la lógica del turno estaba en el callback, que el fin de partida solo se imprimía en consola, que faltaba evidencia de enfoque imperativo vs. funcional y que el análisis tenía errores; luego aplicó las correcciones en módulos separados (`modelos.py`, `logica.py`, `interfaz.py`), con `pruebas.py` y `comparacion_imperativo_vs_funcional.py`.

## Qué se aceptó (y por qué)
- **Separar en capas (datos, lógica, UI) y usar `ttkbootstrap`:** cumple la restricción de diseño de la guía y da una interfaz más cuidada con poco código.
- **`@dataclass(frozen=True)`:** garantiza la inmutabilidad: intentar modificar un campo lanza un error, así que no se puede mutar el estado por accidente.
- **`match/case`:** reemplaza una cadena de `if/elif` y permite usar patrones sobre tuplas con guardas (`determinar_resultado`).
- **Closure `crear_multiplicador_danio`:** permite configurar el multiplicador sin cambiar la firma de las funciones de combate.
- **Correcciones de la segunda revisión:** cada una resuelve un punto concreto que la guía penaliza (lógica en callbacks, falta de evidencia imperativo/funcional, documentos con errores).

## Qué se modificó (y por qué)
- **Historial:** se pasó de lista mutable a tupla inmutable (`estado.historial + (mensaje,)`) con `map` + `reduce`, porque `list.append` rompe la inmutabilidad.
- **Nombres:** se ajustaron los nombres de las funciones puras e impuras para que cumplan explícitamente los requisitos de la rúbrica (≥ 3 puras, ≥ 2 impuras).
- **Lógica del turno:** `ejecutar_turno` ya no decide nada; llama a `resolver_turno`, que es pura y se puede probar sin interfaz.
- **Habilidad especial:** se le añadió una recarga de 3 turnos, porque sin ella siempre era mejor que el ataque básico.
- **Reporte del historial:** ahora todas las líneas llevan viñeta; antes la primera quedaba sin ella.

## Qué se rechazó (y por qué)
- **Historial con `list.append`:** muta el estado y contradice el principio de inmutabilidad que exige la actividad.
- **Lógica de negocio dentro de los callbacks de los botones:** la guía penaliza severamente concentrar la lógica en los eventos visuales; además, así no se podía probar.
- **Marcas `[cite: ...]` en los documentos:** eran restos del texto generado por la IA y no aportaban contenido; se eliminaron.
- **Mencionar `map` en el análisis cuando no se usaba:** era una afirmación falsa; ahora `map` sí se usa en `generar_reporte_historial` y el documento lo describe tal cual.
