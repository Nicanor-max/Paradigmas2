import random
import tkinter as tk


ANCHO = 600
ALTO = 600
TAMANO_CELDA = 20
VELOCIDAD_MS = 100

COLOR_FONDO = "#111827"
COLOR_SERPIENTE = "#dcdcdc"
COLOR_CABEZA = "#86efac"
COLOR_COMIDA = "#ef4444"


class JuegoViborita:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Juego de la Viborita")
        self.ventana.resizable(False, False)

        self.puntuacion_texto = tk.StringVar()
        tk.Label(
            ventana,
            textvariable=self.puntuacion_texto,
            font=("Arial", 16, "bold"),
            bg=COLOR_FONDO,
            fg="white",
            pady=8,
        ).pack(fill="x")

        self.canvas = tk.Canvas(
            ventana,
            width=ANCHO,
            height=ALTO,
            bg=COLOR_FONDO,
            highlightthickness=0,
        )
        self.canvas.pack()

        self.ventana.bind("<KeyPress>", self.cambiar_direccion)
        self.reiniciar()

    def reiniciar(self, _evento=None):
        centro_x = (ANCHO // TAMANO_CELDA // 2) * TAMANO_CELDA
        centro_y = (ALTO // TAMANO_CELDA // 2) * TAMANO_CELDA
        self.serpiente = [
            (centro_x, centro_y),
            (centro_x - TAMANO_CELDA, centro_y),
            (centro_x - TAMANO_CELDA * 2, centro_y),
        ]
        self.direccion = (TAMANO_CELDA, 0)
        self.siguiente_direccion = self.direccion
        self.puntuacion = 0
        self.terminado = False
        self.pausado = False
        self.colocar_comida()
        self.actualizar_puntuacion()
        self.dibujar()
        self.ventana.after(VELOCIDAD_MS, self.actualizar)

    def colocar_comida(self):
        casillas_libres = [
            (x, y)
            for x in range(0, ANCHO, TAMANO_CELDA)
            for y in range(0, ALTO, TAMANO_CELDA)
            if (x, y) not in self.serpiente
        ]
        self.comida = random.choice(casillas_libres) if casillas_libres else None

    def cambiar_direccion(self, evento):
        tecla = evento.keysym.lower()

        if tecla == "space" and not self.terminado:
            self.pausado = not self.pausado
            self.dibujar()
            return

        if self.terminado and tecla in ("r", "return"):
            self.reiniciar()
            return

        direcciones = {
            "up": (0, -TAMANO_CELDA),
            "w": (0, -TAMANO_CELDA),
            "down": (0, TAMANO_CELDA),
            "s": (0, TAMANO_CELDA),
            "left": (-TAMANO_CELDA, 0),
            "a": (-TAMANO_CELDA, 0),
            "right": (TAMANO_CELDA, 0),
            "d": (TAMANO_CELDA, 0),
        }

        nueva = direcciones.get(tecla)
        if nueva and nueva != (-self.direccion[0], -self.direccion[1]):
            self.siguiente_direccion = nueva

    def actualizar(self):
        if self.terminado:
            return

        if not self.pausado:
            self.direccion = self.siguiente_direccion
            cabeza_x, cabeza_y = self.serpiente[0]
            dx, dy = self.direccion
            nueva_cabeza = (cabeza_x + dx, cabeza_y + dy)

            fuera_del_tablero = not (
                0 <= nueva_cabeza[0] < ANCHO and 0 <= nueva_cabeza[1] < ALTO
            )
            comera = nueva_cabeza == self.comida
            cuerpo_a_comprobar = self.serpiente if comera else self.serpiente[:-1]

            if fuera_del_tablero or nueva_cabeza in cuerpo_a_comprobar:
                self.terminado = True
                self.dibujar()
                return

            self.serpiente.insert(0, nueva_cabeza)

            if comera:
                self.puntuacion += 1
                self.colocar_comida()
                self.actualizar_puntuacion()
                if self.comida is None:
                    self.terminado = True
            else:
                self.serpiente.pop()

            self.dibujar()

        self.ventana.after(VELOCIDAD_MS, self.actualizar)

    def actualizar_puntuacion(self):
        self.puntuacion_texto.set(
            f"Puntuación: {self.puntuacion}   |   Espacio: pausa"
        )

    def dibujar(self):
        self.canvas.delete("all")

        if self.comida is not None:
            x, y = self.comida
            margen = 3
            self.canvas.create_oval(
                x + margen,
                y + margen,
                x + TAMANO_CELDA - margen,
                y + TAMANO_CELDA - margen,
                fill=COLOR_COMIDA,
                outline="",
            )

        for indice, (x, y) in enumerate(self.serpiente):
            margen = 1
            color = COLOR_CABEZA if indice == 0 else COLOR_SERPIENTE
            self.canvas.create_rectangle(
                x + margen,
                y + margen,
                x + TAMANO_CELDA - margen,
                y + TAMANO_CELDA - margen,
                fill=color,
                outline="",
            )

        if self.pausado:
            self.mostrar_mensaje("PAUSA", "Presiona espacio para continuar")
        elif self.terminado:
            mensaje = "¡GANASTE!" if self.comida is None else "FIN DEL JUEGO"
            self.mostrar_mensaje(mensaje, "Presiona R o Enter para reiniciar")

    def mostrar_mensaje(self, titulo, subtitulo):
        self.canvas.create_rectangle(
            80, 245, ANCHO - 80, 355, fill="#000000", stipple="gray50", outline=""
        )
        self.canvas.create_text(
            ANCHO // 2,
            280,
            text=titulo,
            fill="white",
            font=("Arial", 28, "bold"),
        )
        self.canvas.create_text(
            ANCHO // 2,
            325,
            text=subtitulo,
            fill="#d1d5db",
            font=("Arial", 13),
        )


if __name__ == "__main__":
    raiz = tk.Tk()
    raiz.configure(bg=COLOR_FONDO)
    JuegoViborita(raiz)
    raiz.mainloop()
