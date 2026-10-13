"""Punto de entrada: crea la ventana y arranca la aplicación."""

import ttkbootstrap as ttk

from interfaz import ArenaFuncionalApp


def main() -> None:
    app = ttk.Window(themename="superhero")
    ArenaFuncionalApp(app)
    app.mainloop()


if __name__ == "__main__":
    main()
