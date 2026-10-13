"""Capa visual: Tkinter + ttkbootstrap.

Este módulo contiene los EFECTOS SECUNDARIOS (widgets y consola). Toda decisión
del dominio se delega en `logica.py`: los callbacks solo llaman a funciones
puras y luego refrescan la pantalla.
"""

import tkinter as tk

import ttkbootstrap as ttk

from logica import (
    accion_disponible,
    determinar_resultado,
    estado_inicial,
    generar_reporte_historial,
    resolver_turno,
)

# (clave de acción, texto del botón, estilo)
ACCIONES_UI = (
    ("ATACAR_BASICO", "Atacar Básico", "outline-success"),
    ("CURAR", "Usar Poción (Curar)", "outline-info"),
    ("HABILIDAD_ESPECIAL", "Habilidad Especial (Closure)", "outline-warning"),
)

# resultado -> (mensaje para el usuario, estilo del aviso)
AVISOS_RESULTADO = {
    "EN_CURSO": ("¡Elige tu próxima acción!", "inverse-secondary"),
    "VICTORIA": ("🏆 ¡Victoria! Derrotaste al enemigo.", "inverse-success"),
    "DERROTA": ("💀 Derrota. El enemigo te venció.", "inverse-danger"),
}


# Función IMPURA 1: escribe en la consola (efecto secundario de E/S).
def registrar_log_externo(mensaje: str) -> None:
    print(f"[LOG EXTERNO - EFECTO SECUNDARIO]: {mensaje}")


class ArenaFuncionalApp:

    def __init__(self, root: ttk.Window):
        self.root = root
        self.root.title("Simulador Funcional - Arena de Combate")
        self.root.geometry("850x720")

        # Única referencia que cambia: apunta al estado inmutable vigente.
        self.estado = estado_inicial()
        self.botones: dict[str, ttk.Button] = {}

        self._construir_interfaz()
        self.actualizar_vista()

    def _construir_interfaz(self) -> None:
        titulo = ttk.Label(
            self.root,
            text="⚔️ Simulador Funcional con Interfaz Gráfica",
            font=("Helvetica", 16, "bold"),
            bootstyle="inverse-primary",
        )
        titulo.pack(fill=tk.X, padx=10, pady=10, ipady=5)

        self.lbl_aviso = ttk.Label(
            self.root,
            text="",
            font=("Helvetica", 12, "bold"),
            anchor=tk.CENTER,
            bootstyle="inverse-secondary",
        )
        self.lbl_aviso.pack(fill=tk.X, padx=10, pady=(0, 5), ipady=4)

        panel_stats = ttk.Frame(self.root)
        panel_stats.pack(fill=tk.X, padx=10, pady=5)

        jugador, enemigo = self.estado.jugador, self.estado.enemigo

        frm_jugador = ttk.Labelframe(
            panel_stats, text=" Héroe ", bootstyle="success", padding=15
        )
        frm_jugador.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5)
        self.lbl_jugador_info = ttk.Label(
            frm_jugador, text="", font=("Courier", 11)
        )
        self.lbl_jugador_info.pack(anchor=tk.W)
        self.pb_jugador = ttk.Meter(
            frm_jugador,
            subtext="HP Jugador",
            bootstyle="success",
            amounttotal=jugador.max_hp,
            metertype="full",
            interactive=False,
            textfont=("Helvetica", 12),
            metersize=130,
        )
        self.pb_jugador.pack(pady=5)

        frm_enemigo = ttk.Labelframe(
            panel_stats, text=" Enemigo ", bootstyle="danger", padding=15
        )
        frm_enemigo.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=5)
        self.lbl_enemigo_info = ttk.Label(
            frm_enemigo, text="", font=("Courier", 11)
        )
        self.lbl_enemigo_info.pack(anchor=tk.W)
        self.pb_enemigo = ttk.Meter(
            frm_enemigo,
            subtext="HP Enemigo",
            bootstyle="danger",
            amounttotal=enemigo.max_hp,
            metertype="full",
            interactive=False,
            textfont=("Helvetica", 12),
            metersize=130,
        )
        self.pb_enemigo.pack(pady=5)

        panel_acciones = ttk.Labelframe(
            self.root, text=" Acciones Funcionales ", padding=15
        )
        panel_acciones.pack(fill=tk.X, padx=15, pady=10)

        for accion, texto, estilo in ACCIONES_UI:
            # `a=accion` fija el valor de cada vuelta; sin eso, todas las
            # lambdas verían la última acción del bucle (late binding).
            boton = ttk.Button(
                panel_acciones,
                text=texto,
                bootstyle=estilo,
                command=lambda a=accion: self.ejecutar_turno(a),
            )
            boton.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
            self.botones[accion] = boton

        ttk.Button(
            panel_acciones,
            text="Nueva partida",
            bootstyle="secondary",
            command=self.nueva_partida,
        ).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        panel_historial = ttk.Labelframe(
            self.root, text=" Historial de Eventos (map + reduce) ", padding=10
        )
        panel_historial.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        self.txt_historial = tk.Text(
            panel_historial, height=8, font=("Consolas", 10), state=tk.DISABLED
        )
        self.txt_historial.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(
            panel_historial, orient="vertical", command=self.txt_historial.yview
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.txt_historial.config(yscrollcommand=scrollbar.set)

    # Función IMPURA 2: modifica widgets de la pantalla (efecto secundario).
    # Solo LEE el estado y las funciones puras; no decide nada del dominio.
    def actualizar_vista(self) -> None:
        j = self.estado.jugador
        e = self.estado.enemigo
        resultado = determinar_resultado(self.estado)

        self.lbl_jugador_info.config(
            text=f"Nombre: {j.nombre}\nNivel: {j.nivel}\n"
            f"Ataque: {j.ataque} | Defensa: {j.defensa}"
        )
        self.lbl_enemigo_info.config(
            text=f"Nombre: {e.nombre}\nNivel: {e.nivel}\n"
            f"Ataque: {e.ataque} | Defensa: {e.defensa}"
        )

        self.pb_jugador.configure(amountused=j.hp)
        self.pb_enemigo.configure(amountused=e.hp)

        mensaje, estilo = AVISOS_RESULTADO[resultado]
        self.lbl_aviso.configure(text=mensaje, bootstyle=estilo)

        # Habilitar o deshabilitar botones según la lógica pura.
        for accion, boton in self.botones.items():
            disponible = (
                resultado == "EN_CURSO"
                and accion_disponible(accion, self.estado)
            )
            boton.configure(state=tk.NORMAL if disponible else tk.DISABLED)

        espera = self.estado.espera_especial
        texto_especial = "Habilidad Especial (Closure)"
        if espera > 0:
            texto_especial += f" - recarga: {espera}"
        self.botones["HABILIDAD_ESPECIAL"].configure(text=texto_especial)

        reporte_texto = generar_reporte_historial(self.estado.historial)
        self.txt_historial.config(state=tk.NORMAL)
        self.txt_historial.delete("1.0", tk.END)
        self.txt_historial.insert(tk.END, reporte_texto)
        self.txt_historial.see(tk.END)
        self.txt_historial.config(state=tk.DISABLED)

    # Callback delgado: llama a la lógica pura, reasigna el estado y refresca.
    def ejecutar_turno(self, accion: str) -> None:
        self.estado = resolver_turno(accion, self.estado)
        registrar_log_externo(f"Acción ejecutada: {accion}")
        if determinar_resultado(self.estado) != "EN_CURSO":
            registrar_log_externo(
                f"Partida terminada: {determinar_resultado(self.estado)}"
            )
        self.actualizar_vista()

    def nueva_partida(self) -> None:
        self.estado = estado_inicial()
        registrar_log_externo("Nueva partida iniciada")
        self.actualizar_vista()
