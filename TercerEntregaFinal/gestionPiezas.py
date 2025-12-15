from dotenv import load_dotenv
import customtkinter as ctk
import psycopg2
from tkinter import messagebox
import os

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class gestionPiezas(ctk.CTk):

    def __init__(self):
        super().__init__()
        load_dotenv()

        self.pieza_id_actual = None
        self.piezas_cache = []
        self.colegios_cache = []

        self.conectar_bd()
        self.configurar_ventana()

        self.crear_panel_izquierdo()
        self.crear_panel_derecho()
        self.crear_barra_inferior()

        self.cargar_colegios()
        self.listar_piezas()

    # --------------------------------------------------
    # CONFIGURACIÓN
    # --------------------------------------------------

    def configurar_ventana(self):
        self.title("Piezas de Uniforme por Colegio")
        self.geometry("900x650")

        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

    def conectar_bd(self):
        try:
            self.conn = psycopg2.connect(
                host=os.getenv("DB_HOST", "localhost"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                dbname=os.getenv("DB_NAME", "ProyectoFinal")
            )
        except Exception as e:
            messagebox.showerror("Error BD", str(e))
            self.conn = None

    # --------------------------------------------------
    # PANEL IZQUIERDO
    # --------------------------------------------------

    def crear_panel_izquierdo(self):
        frame = ctk.CTkFrame(self.main_frame, width=380)
        frame.pack(side="left", fill="y", padx=(0, 15))

        ctk.CTkLabel(
            frame, text="NUEVA / EDITAR PIEZA",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=10)

        ctk.CTkLabel(frame, text="Colegio").pack(anchor="w", padx=10)
        self.colegio_option = ctk.CTkOptionMenu(frame, values=[])
        self.colegio_option.pack(fill="x", padx=10, pady=5)

        self.color_entry = ctk.CTkEntry(frame, placeholder_text="Color de la prenda")
        self.color_entry.pack(fill="x", padx=10, pady=5)

        self.bordado_check = ctk.CTkCheckBox(frame, text="Tiene bordado")
        self.bordado_check.pack(anchor="w", padx=10, pady=5)

        self.lugar_bordado_entry = ctk.CTkEntry(
            frame, placeholder_text="Lugar del bordado"
        )
        self.lugar_bordado_entry.pack(fill="x", padx=10, pady=5)

        self.color_bordes_entry = ctk.CTkEntry(
            frame, placeholder_text="Color de bordes"
        )
        self.color_bordes_entry.pack(fill="x", padx=10, pady=5)

        self.estampado_entry = ctk.CTkEntry(
            frame, placeholder_text="Estampado (si aplica)"
        )
        self.estampado_entry.pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            frame, text="Guardar Pieza",
            command=self.guardar_pieza
        ).pack(fill="x", padx=10, pady=(10, 5))

        ctk.CTkButton(
            frame, text="Eliminar Pieza",
            fg_color="#8B0000",
            hover_color="#A52A2A",
            command=self.eliminar_pieza
        ).pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            frame, text="Nueva Pieza",
            command=self.limpiar_campos
        ).pack(fill="x", padx=10, pady=(5, 10))

    # --------------------------------------------------
    # PANEL DERECHO
    # --------------------------------------------------

    def crear_panel_derecho(self):
        frame = ctk.CTkFrame(self.main_frame)
        frame.pack(side="right", fill="both", expand=True)

        ctk.CTkLabel(
            frame, text="PIEZAS REGISTRADAS",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=10)

        self.lista = ctk.CTkTextbox(frame)
        self.lista.pack(fill="both", expand=True, padx=10, pady=5)
        self.lista.configure(state="disabled")
        self.lista.bind("<ButtonRelease-1>", self.seleccionar_pieza)

        self.total_label = ctk.CTkLabel(frame, text="Total piezas: 0")
        self.total_label.pack(anchor="w", padx=10)

    # --------------------------------------------------
    # BARRA INFERIOR
    # --------------------------------------------------

    def crear_barra_inferior(self):
        bar = ctk.CTkFrame(self)
        bar.pack(fill="x")

        ctk.CTkButton(bar, text="Cerrar", command=self.destroy).pack(side="left", padx=10)
        ctk.CTkLabel(bar, text="Usuario: admin").pack(side="right", padx=10)

    # --------------------------------------------------
    # BD
    # --------------------------------------------------

    def cargar_colegios(self):
        cur = self.conn.cursor()
        cur.execute("SELECT id_colegio, nombre FROM colegio ORDER BY nombre")
        self.colegios_cache = cur.fetchall()
        cur.close()

        nombres = [f"{c[0]} - {c[1]}" for c in self.colegios_cache]
        if nombres:
            self.colegio_option.configure(values=nombres)
            self.colegio_option.set(nombres[0])

    def guardar_pieza(self):
        colegio_texto = self.colegio_option.get()
        id_colegio = int(colegio_texto.split(" - ")[0])

        color = self.color_entry.get().strip()
        bordado = self.bordado_check.get()
        lugar = self.lugar_bordado_entry.get().strip()
        color_bordes = self.color_bordes_entry.get().strip()
        estampado = self.estampado_entry.get().strip()

        if not color:
            messagebox.showwarning("Error", "El color es obligatorio")
            return

        cur = self.conn.cursor()

        try:
            if self.pieza_id_actual is None:
                cur.execute("""
                    INSERT INTO pieza_uniforme
                    (id_colegio, lugar_bordado, color_bordes, bordado, color, estampado)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (id_colegio, lugar, color_bordes, bordado, color, estampado))
            else:
                cur.execute("""
                    UPDATE pieza_uniforme
                    SET id_colegio=%s, lugar_bordado=%s, color_bordes=%s,
                        bordado=%s, color=%s, estampado=%s
                    WHERE id_pieza=%s
                """, (
                    id_colegio, lugar, color_bordes,
                    bordado, color, estampado,
                    self.pieza_id_actual
                ))

            self.conn.commit()
            messagebox.showinfo("Éxito", "Pieza guardada correctamente")
            self.limpiar_campos()
            self.listar_piezas()

        except Exception as e:
            self.conn.rollback()
            messagebox.showerror("Error", str(e))
        finally:
            cur.close()

    def eliminar_pieza(self):
        if self.pieza_id_actual is None:
            messagebox.showwarning("Error", "Seleccione una pieza")
            return

        cur = self.conn.cursor()
        try:
            cur.execute(
                "DELETE FROM pieza_uniforme WHERE id_pieza=%s",
                (self.pieza_id_actual,)
            )
            self.conn.commit()
            messagebox.showinfo("Eliminado", "Pieza eliminada")
            self.limpiar_campos()
            self.listar_piezas()
        except Exception as e:
            self.conn.rollback()
            messagebox.showerror("Error", str(e))
        finally:
            cur.close()

    def listar_piezas(self):
        cur = self.conn.cursor()
        cur.execute("""
            SELECT p.id_pieza, c.nombre, p.color, p.bordado,
                   p.lugar_bordado, p.color_bordes, p.estampado
            FROM pieza_uniforme p
            JOIN colegio c ON c.id_colegio = p.id_colegio
            ORDER BY c.nombre
        """)
        piezas = cur.fetchall()
        cur.close()
        self.mostrar_piezas(piezas)

    # --------------------------------------------------
    # UTILIDADES
    # --------------------------------------------------

    def mostrar_piezas(self, piezas):
        self.lista.configure(state="normal")
        self.lista.delete("1.0", "end")

        for p in piezas:
            self.lista.insert(
                "end",
                f"{p[0]} | {p[1]} | Color:{p[2]} | Bordado:{p[3]} | "
                f"Lugar:{p[4]} | Bordes:{p[5]} | Estampado:{p[6]}\n"
            )

        self.lista.configure(state="disabled")
        self.total_label.configure(text=f"Total piezas: {len(piezas)}")
        self.piezas_cache = piezas

    def seleccionar_pieza(self, event):
        try:
            index = self.lista.index(f"@{event.x},{event.y}")
            linea = int(index.split(".")[0]) - 1
            p = self.piezas_cache[linea]

            self.pieza_id_actual = p[0]

            self.color_entry.delete(0, "end")
            self.color_entry.insert(0, p[2])

            self.bordado_check.select() if p[3] else self.bordado_check.deselect()

            self.lugar_bordado_entry.delete(0, "end")
            self.lugar_bordado_entry.insert(0, p[4] or "")

            self.color_bordes_entry.delete(0, "end")
            self.color_bordes_entry.insert(0, p[5] or "")

            self.estampado_entry.delete(0, "end")
            self.estampado_entry.insert(0, p[6] or "")

        except:
            pass

    def limpiar_campos(self):
        self.pieza_id_actual = None
        self.color_entry.delete(0, "end")
        self.lugar_bordado_entry.delete(0, "end")
        self.color_bordes_entry.delete(0, "end")
        self.estampado_entry.delete(0, "end")
        self.bordado_check.deselect()


if __name__ == "__main__":
    app = gestionPiezas()
    app.mainloop()
