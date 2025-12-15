from dotenv import load_dotenv
import customtkinter as ctk
import psycopg2
from tkinter import messagebox
import os

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class GestionColegios(ctk.CTk):

    def __init__(self):
        super().__init__()
        load_dotenv()

        self.colegio_id_actual = None
        self.colegios_cache = []

        self.conectar_bd()
        self.configurar_ventana()

        self.crear_panel_izquierdo()
        self.crear_panel_derecho()
        self.crear_barra_inferior()

        self.listar_colegios()

    # --------------------------------------------------
    # CONFIGURACIÓN
    # --------------------------------------------------

    def configurar_ventana(self):
        self.title("Gestión de Colegios")
        self.geometry("700x600")

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
        frame = ctk.CTkFrame(self.main_frame, width=320)
        frame.pack(side="left", fill="y", padx=(0, 15))

        ctk.CTkLabel(
            frame, text="NUEVO / EDITAR COLEGIO",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=10)

        self.nombre_entry = ctk.CTkEntry(frame, placeholder_text="Nombre del colegio")
        self.nombre_entry.pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            frame, text="Guardar Colegio",
            command=self.guardar_colegio
        ).pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            frame, text="Eliminar Colegio",
            command=self.eliminar_colegio
        ).pack(fill="x", padx=10, pady=5)

    # --------------------------------------------------
    # PANEL DERECHO
    # --------------------------------------------------

    def crear_panel_derecho(self):
        frame = ctk.CTkFrame(self.main_frame)
        frame.pack(side="right", fill="both", expand=True)

        ctk.CTkLabel(
            frame, text="BUSCAR COLEGIO",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=10)

        self.busqueda_entry = ctk.CTkEntry(
            frame, placeholder_text="Código o nombre"
        )
        self.busqueda_entry.pack(fill="x", padx=10, pady=5)
        self.busqueda_entry.bind("<KeyRelease>", lambda e: self.buscar_colegio())

        self.lista = ctk.CTkTextbox(frame)
        self.lista.pack(fill="both", expand=True, padx=10, pady=5)
        self.lista.configure(state="disabled")
        self.lista.bind("<ButtonRelease-1>", self.seleccionar_colegio)

        self.total_label = ctk.CTkLabel(frame, text="Total colegios: 0")
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
    # FUNCIONES BD
    # --------------------------------------------------

    def guardar_colegio(self):
        nombre = self.nombre_entry.get().strip()

        if not nombre:
            messagebox.showwarning("Error", "El nombre es obligatorio")
            return

        cur = self.conn.cursor()

        try:
            if self.colegio_id_actual is None:
                cur.execute(
                    "INSERT INTO colegio (nombre) VALUES (%s)",
                    (nombre,)
                )
            else:
                cur.execute(
                    "UPDATE colegio SET nombre=%s WHERE id_colegio=%s",
                    (nombre, self.colegio_id_actual)
                )

            self.conn.commit()
            messagebox.showinfo("Éxito", "Colegio guardado correctamente")
            self.limpiar_campos()
            self.listar_colegios()

        except Exception as e:
            self.conn.rollback()
            messagebox.showerror("Error", str(e))
        finally:
            cur.close()

    def eliminar_colegio(self):
        if self.colegio_id_actual is None:
            messagebox.showwarning("Error", "Seleccione un colegio")
            return

        cur = self.conn.cursor()
        try:
            cur.execute(
                "DELETE FROM colegio WHERE id_colegio=%s",
                (self.colegio_id_actual,)
            )
            self.conn.commit()
            messagebox.showinfo("Eliminado", "Colegio eliminado")
            self.limpiar_campos()
            self.listar_colegios()
        except Exception as e:
            self.conn.rollback()
            messagebox.showerror("Error", str(e))
        finally:
            cur.close()

    def buscar_colegio(self):
        texto = self.busqueda_entry.get().strip()

        cur = self.conn.cursor()

        if texto.isdigit():
            cur.execute(
                "SELECT * FROM colegio WHERE id_colegio=%s",
                (int(texto),)
            )
        else:
            cur.execute(
                "SELECT * FROM colegio WHERE nombre ILIKE %s",
                (f"%{texto}%",)
            )

        colegios = cur.fetchall()
        cur.close()
        self.mostrar_colegios(colegios)

    def listar_colegios(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM colegio ORDER BY nombre")
        colegios = cur.fetchall()
        cur.close()
        self.mostrar_colegios(colegios)

    # --------------------------------------------------
    # UTILIDADES
    # --------------------------------------------------

    def mostrar_colegios(self, colegios):
        self.lista.configure(state="normal")
        self.lista.delete("1.0", "end")

        for c in colegios:
            self.lista.insert("end", f"{c[0]} - {c[1]}\n")

        self.lista.configure(state="disabled")
        self.total_label.configure(text=f"Total colegios: {len(colegios)}")
        self.colegios_cache = colegios

    def seleccionar_colegio(self, event):
        try:
            index = self.lista.index(f"@{event.x},{event.y}")
            linea = int(index.split(".")[0]) - 1
            colegio = self.colegios_cache[linea]

            self.colegio_id_actual = colegio[0]
            self.nombre_entry.delete(0, "end")
            self.nombre_entry.insert(0, colegio[1])
        except:
            pass

    def limpiar_campos(self):
        self.colegio_id_actual = None
        self.nombre_entry.delete(0, "end")

if __name__ == "__main__":
    app = GestionColegios()
    app.mainloop()