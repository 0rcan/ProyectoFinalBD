from dotenv import load_dotenv
import customtkinter as ctk
import psycopg2
from tkinter import messagebox
import os

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class gestionProveedor(ctk.CTk):

    def __init__(self):
        super().__init__()
        load_dotenv()

        self.nit_actual = None
        self.proveedores_cache = []

        self.conectar_bd()
        self.configurar_ventana()

        self.crear_panel_izquierdo()
        self.crear_panel_derecho()
        self.crear_barra_inferior()

        self.listar_proveedores()

    # --------------------------------------------------
    # CONFIGURACIÓN
    # --------------------------------------------------

    def configurar_ventana(self):
        self.title("Gestión de Proveedores")
        self.geometry("800x600")

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
        frame = ctk.CTkFrame(self.main_frame, width=340)
        frame.pack(side="left", fill="y", padx=(0, 15))

        ctk.CTkLabel(
            frame, text="NUEVO / EDITAR PROVEEDOR",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=10)

        self.nit_entry = ctk.CTkEntry(frame, placeholder_text="NIT")
        self.nit_entry.pack(fill="x", padx=10, pady=5)

        self.nombre_entry = ctk.CTkEntry(frame, placeholder_text="Nombre proveedor")
        self.nombre_entry.pack(fill="x", padx=10, pady=5)

        self.contacto_entry = ctk.CTkEntry(frame, placeholder_text="Nombre contacto")
        self.contacto_entry.pack(fill="x", padx=10, pady=5)

        self.telefono_entry = ctk.CTkEntry(frame, placeholder_text="Teléfono")
        self.telefono_entry.pack(fill="x", padx=10, pady=5)

        self.direccion_entry = ctk.CTkEntry(frame, placeholder_text="Dirección")
        self.direccion_entry.pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            frame, text="Guardar Proveedor",
            command=self.guardar_proveedor
        ).pack(fill="x", padx=10, pady=8)

        ctk.CTkButton(
            frame, text="Eliminar Proveedor",
            command=self.eliminar_proveedor
        ).pack(fill="x", padx=10, pady=5)

    # --------------------------------------------------
    # PANEL DERECHO
    # --------------------------------------------------

    def crear_panel_derecho(self):
        frame = ctk.CTkFrame(self.main_frame)
        frame.pack(side="right", fill="both", expand=True)

        ctk.CTkLabel(
            frame, text="BUSCAR POR NIT",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=10)

        self.busqueda_entry = ctk.CTkEntry(frame, placeholder_text="Ingrese NIT")
        self.busqueda_entry.pack(fill="x", padx=10, pady=5)
        self.busqueda_entry.bind("<KeyRelease>", lambda e: self.buscar_proveedor())

        self.lista = ctk.CTkTextbox(frame)
        self.lista.pack(fill="both", expand=True, padx=10, pady=5)
        self.lista.configure(state="disabled")
        self.lista.bind("<ButtonRelease-1>", self.seleccionar_proveedor)

        self.total_label = ctk.CTkLabel(frame, text="Total proveedores: 0")
        self.total_label.pack(anchor="w", padx=10)

    # --------------------------------------------------
    # BARRA INFERIOR
    # --------------------------------------------------

    def crear_barra_inferior(self):
        bar = ctk.CTkFrame(self)
        bar.pack(fill="x")

        ctk.CTkButton(bar, text="Volver", command=self.volver).pack(side="left", padx=10)
        ctk.CTkLabel(bar, text="Usuario: vendedor01").pack(side="right", padx=10)

    # --------------------------------------------------
    # FUNCIONES BD
    # --------------------------------------------------

    def guardar_proveedor(self):
        nit = self.nit_entry.get().strip()
        nombre = self.nombre_entry.get().strip()
        contacto = self.contacto_entry.get().strip()
        telefono = self.telefono_entry.get().strip()
        direccion = self.direccion_entry.get().strip()

        if not nit or not nombre:
            messagebox.showwarning("Error", "NIT y nombre son obligatorios")
            return

        cur = self.conn.cursor()

        try:
            cur.execute("""
                INSERT INTO proveedor (nit, nombre, nombre_contacto, telefono, direccion)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (nit)
                DO UPDATE SET
                    nombre = EXCLUDED.nombre,
                    nombre_contacto = EXCLUDED.nombre_contacto,
                    telefono = EXCLUDED.telefono,
                    direccion = EXCLUDED.direccion
            """, (nit, nombre, contacto, telefono, direccion))

            self.conn.commit()
            messagebox.showinfo("Éxito", "Proveedor guardado correctamente")
            self.limpiar_campos()
            self.listar_proveedores()

        except Exception as e:
            self.conn.rollback()
            messagebox.showerror("Error", str(e))
        finally:
            cur.close()

    def eliminar_proveedor(self):
        if not self.nit_actual:
            messagebox.showwarning("Error", "Seleccione un proveedor")
            return

        cur = self.conn.cursor()
        try:
            cur.execute("DELETE FROM proveedor WHERE nit=%s", (self.nit_actual,))
            self.conn.commit()
            messagebox.showinfo("Éxito", "Proveedor eliminado")
            self.limpiar_campos()
            self.listar_proveedores()
        except Exception as e:
            self.conn.rollback()
            messagebox.showerror("Error", str(e))
        finally:
            cur.close()

    def buscar_proveedor(self):
        texto = self.busqueda_entry.get().strip()

        cur = self.conn.cursor()

        if texto:
            cur.execute("SELECT * FROM proveedor WHERE nit=%s", (texto,))
        else:
            cur.execute("SELECT * FROM proveedor ORDER BY nombre")

        proveedores = cur.fetchall()
        cur.close()
        self.mostrar_proveedores(proveedores)

    def listar_proveedores(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM proveedor ORDER BY nombre")
        proveedores = cur.fetchall()
        cur.close()
        self.mostrar_proveedores(proveedores)

    # --------------------------------------------------
    # UTILIDADES
    # --------------------------------------------------

    def mostrar_proveedores(self, proveedores):
        self.lista.configure(state="normal")
        self.lista.delete("1.0", "end")

        for p in proveedores:
            self.lista.insert(
                "end",
                f"{p[0]} | {p[1]}\n"
            )

        self.lista.configure(state="disabled")
        self.total_label.configure(text=f"Total proveedores: {len(proveedores)}")
        self.proveedores_cache = proveedores

    def seleccionar_proveedor(self, event):
        try:
            index = self.lista.index(f"@{event.x},{event.y}")
            linea = int(index.split(".")[0]) - 1
            proveedor = self.proveedores_cache[linea]

            self.nit_actual = proveedor[0]

            self.nit_entry.delete(0, "end")
            self.nit_entry.insert(0, proveedor[0])

            self.nombre_entry.delete(0, "end")
            self.nombre_entry.insert(0, proveedor[1])

            self.contacto_entry.delete(0, "end")
            self.contacto_entry.insert(0, proveedor[2])

            self.telefono_entry.delete(0, "end")
            self.telefono_entry.insert(0, proveedor[3])

            self.direccion_entry.delete(0, "end")
            self.direccion_entry.insert(0, proveedor[4])

        except:
            pass

    def limpiar_campos(self):
        self.nit_actual = None
        self.nit_entry.delete(0, "end")
        self.nombre_entry.delete(0, "end")
        self.contacto_entry.delete(0, "end")
        self.telefono_entry.delete(0, "end")
        self.direccion_entry.delete(0, "end")

    def volver(self):
        self.destroy()
        from AdminMenu import AdminMenu
        app = AdminMenu("vendedor01")
        app.mainloop()


if __name__ == "__main__":
    app = gestionProveedor()
    app.mainloop()
