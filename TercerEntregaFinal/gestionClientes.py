from dotenv import load_dotenv
import customtkinter as ctk
import psycopg2
from tkinter import messagebox
import os

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class gestionCliente(ctk.CTk):

    def __init__(self):
        super().__init__()
        load_dotenv()

        self.cliente_id_actual = None  # 🔹 cliente seleccionado
        self.clientes_cache = []

        self.conectar_bd()
        self.configurar_ventana()

        self.crear_panel_izquierdo()
        self.crear_panel_derecho()
        self.crear_barra_inferior()

        self.listar_clientes()

    # --------------------------------------------------
    # CONFIGURACIÓN
    # --------------------------------------------------

    def configurar_ventana(self):
        self.title("Gestión de Clientes")
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
            frame, text="NUEVO / EDITAR CLIENTE",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=10)

        self.nombre_entry = ctk.CTkEntry(frame, placeholder_text="Nombre")
        self.nombre_entry.pack(fill="x", padx=10, pady=5)

        self.telefonos_entry = ctk.CTkEntry(frame, placeholder_text="Teléfonos")
        self.telefonos_entry.pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            frame, text="Guardar Cliente",
            command=self.guardar_cliente
        ).pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            frame, text="Eliminar Cliente",
            command=self.eliminar_cliente
        ).pack(fill="x", padx=10, pady=5)

    # --------------------------------------------------
    # PANEL DERECHO
    # --------------------------------------------------

    def crear_panel_derecho(self):
        frame = ctk.CTkFrame(self.main_frame)
        frame.pack(side="right", fill="both", expand=True)

        ctk.CTkLabel(
            frame, text="BUSCAR CLIENTE",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=10)

        self.busqueda_entry = ctk.CTkEntry(frame, placeholder_text="Documento o nombre")
        self.busqueda_entry.pack(fill="x", padx=10, pady=5)
        self.busqueda_entry.bind("<KeyRelease>", lambda e: self.buscar_cliente())

        self.lista_clientes = ctk.CTkTextbox(frame)
        self.lista_clientes.pack(fill="both", expand=True, padx=10, pady=5)
        self.lista_clientes.configure(state="disabled")
        self.lista_clientes.bind("<ButtonRelease-1>", self.seleccionar_cliente)

        self.total_label = ctk.CTkLabel(frame, text="Total clientes: 0")
        self.total_label.pack(anchor="w", padx=10)

    # --------------------------------------------------
    # BARRA INFERIOR
    # --------------------------------------------------

    def crear_barra_inferior(self):
        bar = ctk.CTkFrame(self)
        bar.pack(fill="x")

        ctk.CTkButton(bar, text="Cerrar", command=self.destroy).pack(side="left", padx=10)
        ctk.CTkLabel(bar, text="Usuario: vendedor01").pack(side="right", padx=10)

    # --------------------------------------------------
    # FUNCIONES DE BD
    # --------------------------------------------------

    def guardar_cliente(self):
        nombre = self.nombre_entry.get().strip()
        tel = self.telefonos_entry.get().strip()

        if not nombre:
            messagebox.showwarning("Error", "El nombre es obligatorio")
            return

        cur = self.conn.cursor()

        try:
            if self.cliente_id_actual is None:
                # INSERT
                cur.execute("""
                    INSERT INTO cliente (nombre_completo, telefono)
                    VALUES (%s, %s)
                """, (nombre, tel))
            else:
                # UPDATE
                cur.execute("""
                    UPDATE cliente
                    SET nombre_completo=%s, telefono=%s
                    WHERE id_cliente=%s
                """, (nombre, tel, self.cliente_id_actual))

            self.conn.commit()
            messagebox.showinfo("Éxito", "Cliente guardado correctamente")
            self.limpiar_campos()
            self.listar_clientes()

        except Exception as e:
            self.conn.rollback()
            messagebox.showerror("Error", str(e))
        finally:
            cur.close()

    def eliminar_cliente(self):
        if self.cliente_id_actual is None:
            messagebox.showwarning("Error", "Seleccione un cliente para eliminar")
            return

        cur = self.conn.cursor()
        try:
            cur.execute("DELETE FROM cliente WHERE id_cliente=%s", (self.cliente_id_actual,))
            self.conn.commit()
            messagebox.showinfo("Cliente eliminado", "Cliente eliminado correctamente")
            self.limpiar_campos()
            self.listar_clientes()
        except Exception as e:
            self.conn.rollback()
            messagebox.showerror("Error", str(e))
        finally:
            cur.close()

    def buscar_cliente(self):
        texto = self.busqueda_entry.get().strip()

        if not texto:
            self.listar_clientes()
            return

        cur = self.conn.cursor()

        if texto.isdigit():
            cur.execute(
                "SELECT * FROM cliente WHERE id_cliente=%s",
                (int(texto),)
            )
        else:
            cur.execute(
                "SELECT * FROM cliente WHERE nombre_completo ILIKE %s",
                (f"%{texto}%",)
            )

        clientes = cur.fetchall()
        cur.close()
        self.mostrar_clientes(clientes)

    def listar_clientes(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM cliente ORDER BY nombre_completo")
        clientes = cur.fetchall()
        cur.close()
        self.mostrar_clientes(clientes)

    # --------------------------------------------------
    # UTILIDADES
    # --------------------------------------------------

    def mostrar_clientes(self, clientes):
        self.lista_clientes.configure(state="normal")
        self.lista_clientes.delete("1.0", "end")

        for c in clientes:
            self.lista_clientes.insert("end", f"{c[0]} - {c[1]} - {c[2]}\n")

        self.lista_clientes.configure(state="disabled")
        self.total_label.configure(text=f"Total clientes: {len(clientes)}")
        self.clientes_cache = clientes

    def seleccionar_cliente(self, event):
        try:
            index = self.lista_clientes.index(f"@{event.x},{event.y}")
            linea = int(index.split(".")[0]) - 1
            cliente = self.clientes_cache[linea]

            self.cliente_id_actual = cliente[0]
            self.nombre_entry.delete(0, "end")
            self.nombre_entry.insert(0, cliente[1])

            self.telefonos_entry.delete(0, "end")
            self.telefonos_entry.insert(0, cliente[2])
        except:
            pass

    def limpiar_campos(self):
        self.cliente_id_actual = None
        self.nombre_entry.delete(0, "end")
        self.telefonos_entry.delete(0, "end")


if __name__ == "__main__":
    app = gestionCliente()
    app.mainloop()

