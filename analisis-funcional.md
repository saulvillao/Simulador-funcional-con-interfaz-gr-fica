# Documento de Análisis Técnico: Simulador Funcional con Interfaz Gráfica

## 1. Problema que resuelve la aplicación
La aplicación modela y administra un sistema interactivo de combate por turnos (Arena Funcional). Todas las transiciones de estado, los cálculos de daño y el registro de eventos se resuelven con programación funcional (inmutabilidad, funciones puras, closures y pattern matching), y están completamente desacoplados de la capa visual de Tkinter/ttkbootstrap.

## 2. Estructuras de datos utilizadas
Se usaron **dataclasses** con `@dataclass(frozen=True)` para que los modelos sean inmutables (archivo `modelos.py`):
- `Entidad`: atributos del héroe y del enemigo (`nombre`, `tipo`, `hp`, `max_hp`, `ataque`, `defensa`, `nivel`).
- `EstadoJuego`: estado global del combate: `jugador`, `enemigo`, `historial` (tupla inmutable de cadenas) y `espera_especial` (turnos que faltan para volver a usar la habilidad especial).

## 3. Dónde se aplicó la Unidad 1
- **Funciones de orden superior (`logica.py`):**
  - `crear_multiplicador_danio(factor)` **devuelve una función**.
  - `map` y `reduce` **reciben funciones** (lambdas) como argumento dentro de `generar_reporte_historial`.
- **Pattern matching (`match/case`)**, en cuatro funciones, no solo como adorno:
  - `procesar_accion_juego`: decide qué hacer según la acción (`ATACAR_BASICO`, `CURAR`, `HABILIDAD_ESPECIAL`, `TURNO_ENEMIGO`).
  - `accion_disponible`: usa patrones alternativos (`"ATACAR_BASICO" | "CURAR"`) para saber si una acción se puede usar.
  - `determinar_resultado`: hace match sobre la tupla `(hp_jugador, hp_enemigo)` con guardas (`if hp <= 0`) para obtener `VICTORIA`, `DERROTA` o `EN_CURSO`.
  - `registrar_resultado`: según el resultado, agrega el evento final al historial.
- **Modelado de datos:** `dataclass` congeladas (`Entidad`, `EstadoJuego`).
- **Enfoque funcional vs. imperativo:** el archivo `comparacion_imperativo_vs_funcional.py` genera el mismo reporte del historial de dos formas y verifica con `assert` que el resultado es idéntico:
  - Imperativo: un bucle `for` que **muta** una variable acumuladora (`texto += ...`).
  - Funcional: `map` + `reduce`, que transforman la tupla y producen un valor nuevo sin mutar nada.

## 4. Dónde se aplicó la Unidad 2
- **Lambda:**
  - En `map(lambda linea: f"• {linea}", historial)` y `reduce(lambda acumulado, linea: ..., lineas)`.
  - En los botones: `command=lambda a=accion: self.ejecutar_turno(a)`. El `a=accion` fija el valor de cada vuelta del bucle; sin eso, todos los botones ejecutarían la última acción (*late binding*).
- **Por qué NO se usó lambda en otras partes:** `procesar_accion_juego` y `resolver_turno` necesitan `match/case`, variables intermedias y varias líneas. Una lambda solo admite una expresión, no permite `match` ni asignaciones, y no se podría documentar ni probar. Esto también está explicado en un comentario al final de `logica.py`.
- **Closure:** `crear_multiplicador_danio(factor)` (ver sección 8).
- **Inmutabilidad:** ningún objeto se modifica; cada cambio crea una copia con `dataclasses.replace` (ver sección 7).
- **Pureza y efectos secundarios:** ver secciones 5 y 6.
- **Map y Reduce:** `generar_reporte_historial` usa `map` para dar formato a cada línea y `reduce` para acumularlas en un solo texto.

## 5. Qué partes son puras y cuáles impuras
**Puras** (todo `logica.py`; no imprimen, no tocan widgets ni archivos, no mutan nada, y con los mismos argumentos devuelven lo mismo):
- `calcular_danio_puro`, `actualizar_hp`, `agregar_evento`, `reducir_espera`
- `generar_reporte_historial` (map + reduce)
- `crear_multiplicador_danio` y el closure que devuelve
- `accion_disponible`, `determinar_resultado`, `registrar_resultado`
- `procesar_accion_juego` y `resolver_turno`
- `estado_inicial`

**Impuras** (`interfaz.py`):
- `registrar_log_externo`: hace `print` en la consola.
- `actualizar_vista`: modifica widgets de la pantalla (medidores, etiquetas, botones, texto del historial).
- `ejecutar_turno` y `nueva_partida`: son callbacks que reasignan `self.estado` y llaman a las dos anteriores.

## 6. Qué efectos secundarios existen
Se concentran exclusivamente en `interfaz.py`:
- Dibujar los medidores de vida (`Meter`), las etiquetas, el aviso de victoria/derrota y el texto del historial.
- Habilitar y deshabilitar los botones de acción (por ejemplo, la habilidad especial mientras está en recarga, o todos al terminar la partida).
- Imprimir mensajes en la consola con `registrar_log_externo`.

## 7. Qué parte del estado se manejó de forma inmutable
Todo el estado del juego (`EstadoJuego` y `Entidad`) es inmutable:
- Los campos no se pueden asignar (`frozen=True`); `pruebas.py` comprueba que intentarlo lanza `FrozenInstanceError`.
- Cada acción devuelve un estado nuevo con `dataclasses.replace`.
- El historial es una tupla: `estado.historial + (mensaje,)` crea una tupla nueva, nunca se hace `append` sobre una lista.
- `pruebas.py` verifica que `resolver_turno` no altera el estado original.

El único lugar donde algo "cambia" es la referencia `self.estado` de la interfaz, que simplemente pasa a apuntar al estado nuevo devuelto por la lógica pura.

## 8. Qué closure se implementó y para qué
`crear_multiplicador_danio(factor)` (en `logica.py`) define la función interna `calcular`, que **recuerda `factor`** del ámbito léxico de la función externa aunque esta ya haya terminado. Se crea una vez con `calcular_danio_critico = crear_multiplicador_danio(1.75)` y se usa en la habilidad especial. Sirve para configurar el multiplicador de daño sin cambiar la firma `(atacante, defensor) -> int` de las funciones de combate, y permite crear otras variantes (por ejemplo, un multiplicador doble) sin duplicar código; `pruebas.py` comprueba dos factores distintos.

## 9. Qué partes sugirió la IA
- La estructura modular separando capas (datos, lógica y UI).
- La elección de componentes visuales modernos de `ttkbootstrap` (como los medidores `Meter`).
- El uso de `dataclasses` congeladas para garantizar la inmutabilidad.
- La sintaxis de `match/case` para procesar las acciones.
- En una segunda ronda, la IA revisó el proyecto contra la guía de la actividad y propuso las correcciones que se describen en la sección 10 (mover la lógica del turno a una función pura, agregar el fin de partida, separar el código en módulos, evidencia imperativo/funcional y pruebas).

## 10. Qué corrigieron o rechazaron de la IA
- **Rechazado:** la propuesta inicial de guardar el historial en una lista mutable (`list.append`), porque rompía la inmutabilidad. Se reemplazó por tuplas inmutables.
- **Rechazado:** poner lógica de negocio dentro de los callbacks de los botones.
- **Corregido tras la revisión:**
  - `ejecutar_turno` decidía si el enemigo contraatacaba y `actualizar_vista` decidía quién ganaba. Esa lógica se movió a las funciones puras `resolver_turno` y `determinar_resultado`.
  - El fin de partida solo se imprimía en consola; ahora se registra en el historial, se muestra un aviso en pantalla y se deshabilitan los botones.
  - El historial ahora lleva viñeta en todas las líneas (antes la primera quedaba sin ella).
  - Se quitaron imports sin usar, los totales de los medidores se toman de `max_hp` y el closure se crea una sola vez.
  - La habilidad especial era siempre mejor que el ataque básico; se le agregó una recarga de 3 turnos (`espera_especial`).
  - Se corrigió este documento: tenía marcas `[cite]` copiadas de la IA y mencionaba un `map` que no existía.

## 11. Qué aprendieron técnicamente
Se comprendió cómo estructurar una aplicación con interfaz gráfica en Python sin caer en malas prácticas imperativas: la lógica del dominio vive en funciones puras que reciben un estado y devuelven uno nuevo, y los efectos secundarios (pantalla y consola) quedan aislados en la capa visual. También se aprendió que:
- `match/case` sirve para más que comparar textos: permite patrones sobre tuplas con guardas.
- Un closure recuerda variables de su ámbito léxico, y una lambda dentro de un bucle necesita fijar su valor (`a=accion`) para evitar el *late binding*.
- La inmutabilidad no es copiar por copiar: permite probar la lógica sin la interfaz y asegurar que el estado anterior no cambia.
- Una función que hace `print` o modifica widgets no es pura, aunque parezca inofensiva.
