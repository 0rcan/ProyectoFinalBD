from dotenv import load_dotenv
import customtkinter as ctk
import psycopg2
from tkinter import messagebox
import os

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class gestionUsuarios(ctk.CTk):

    def __init__(self):
        super().__init__()
        load_dotenv()

        self.usuario_id_actual = None
        self.usuarios_cache = []

        self.conectar_bd()
        self.configurar_ventana()

        self.crear_panel_izquierdo()
        self.crear_panel_derecho()
        self.crear_barra_inferior()

        self.listar_usuarios()

    # --------------------------------------------------
    # CONFIGURACIÓN
    # --------------------------------------------------

    def configurar_ventana(self):
        self.title("Gestión de Usuarios")
        self.geometry("800x620")

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
        frame = ctk.CTkFrame(self.main_frame, width=350)
        frame.pack(side="left", fill="y", padx=(0, 15))

        ctk.CTkLabel(
            frame, text="NUEVO / EDITAR USUARIO",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=10)

        self.usuario_entry = ctk.CTkEntry(frame, placeholder_text="Usuario")
        self.usuario_entry.pack(fill="x", padx=10, pady=5)

        self.nombre_entry = ctk.CTkEntry(frame, placeholder_text="Nombre completo")
        self.nombre_entry.pack(fill="x", padx=10, pady=5)

        self.pass_entry = ctk.CTkEntry(
            frame, placeholder_text="Contraseña", show="*"
        )
        self.pass_entry.pack(fill="x", padx=10, pady=5)

        self.pass2_entry = ctk.CTkEntry(
            frame, placeholder_text="Repetir contraseña", show="*"
        )
        self.pass2_entry.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(frame, text="Rol:").pack(anchor="w", padx=10, pady=(10, 0))
        self.rol_option = ctk.CTkOptionMenu(
            frame, values=["Admin", "Vendedor"]
        )
        self.rol_option.pack(fill="x", padx=10, pady=5)

        self.estado_check = ctk.CTkCheckBox(
            frame, text="Usuario activo"
        )
        self.estado_check.pack(anchor="w", padx=10, pady=5)

        ctk.CTkButton(
            frame, text="Guardar Usuario",
            command=self.guardar_usuario
        ).pack(fill="x", padx=10, pady=(10, 5))

        ctk.CTkButton(
            frame, text="Cambiar Contraseña",
            command=self.cambiar_contrasena
        ).pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            frame, text="Eliminar Usuario",
            fg_color="#8B0000",
            hover_color="#A52A2A",
            command=self.eliminar_usuario
        ).pack(fill="x", padx=10, pady=(5, 10))

    # --------------------------------------------------
    # PANEL DERECHO
    # --------------------------------------------------

    def crear_panel_derecho(self):
        frame = ctk.CTkFrame(self.main_frame)
        frame.pack(side="right", fill="both", expand=True)

        ctk.CTkLabel(
            frame, text="BUSCAR USUARIO",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=10)

        self.busqueda_entry = ctk.CTkEntry(
            frame, placeholder_text="Usuario o nombre"
        )
        self.busqueda_entry.pack(fill="x", padx=10, pady=5)
        self.busqueda_entry.bind("<KeyRelease>", lambda e: self.buscar_usuario())

        self.lista = ctk.CTkTextbox(frame)
        self.lista.pack(fill="both", expand=True, padx=10, pady=5)
        self.lista.configure(state="disabled")
        self.lista.bind("<ButtonRelease-1>", self.seleccionar_usuario)

        self.total_label = ctk.CTkLabel(frame, text="Total usuarios: 0")
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

    def guardar_usuario(self):
        usuario = self.usuario_entry.get().strip()
        nombre = self.nombre_entry.get().strip()
        pwd = self.pass_entry.get()
        pwd2 = self.pass2_entry.get()
        rol = self.rol_option.get()
        estado = self.estado_check.get()

        if not usuario or not nombre:
            messagebox.showwarning("Error", "Usuario y nombre son obligatorios")
            return

        if self.usuario_id_actual is None and not pwd:
            messagebox.showwarning("Error", "Debe ingresar contraseña")
            return

        if pwd != pwd2:
            messagebox.showwarning("Error", "Las contraseñas no coinciden")
            return

        cur = self.conn.cursor()

        try:
            if self.usuario_id_actual is None:
                cur.execute("""
                    INSERT INTO usuario (usuario, contraseña, rol, nombre_completo, estado)
                    VALUES (%s, %s, %s, %s, %s)
                """, (usuario, pwd, rol, nombre, estado))
            else:
                cur.execute("""
                    UPDATE usuario
                    SET usuario=%s, rol=%s, nombre_completo=%s, estado=%s
                    WHERE id_usuario=%s
                """, (usuario, rol, nombre, estado, self.usuario_id_actual))

            self.conn.commit()
            messagebox.showinfo("Éxito", "Usuario guardado correctamente")
            self.limpiar_campos()
            self.listar_usuarios()

        except Exception as e:
            self.conn.rollback()
            messagebox.showerror("Error", str(e))
        finally:
            cur.close()

    def cambiar_contrasena(self):
        if self.usuario_id_actual is None:
            messagebox.showwarning("Error", "Seleccione un usuario")
            return

        pwd = self.pass_entry.get()
        pwd2 = self.pass2_entry.get()

        if not pwd or pwd != pwd2:
            messagebox.showwarning("Error", "Contraseñas inválidas")
            return

        cur = self.conn.cursor()
        try:
            cur.execute(
                "UPDATE usuario SET contraseña=%s WHERE id_usuario=%s",
                (pwd, self.usuario_id_actual)
            )
            self.conn.commit()
            messagebox.showinfo("Éxito", "Contraseña actualizada")
            self.pass_entry.delete(0, "end")
            self.pass2_entry.delete(0, "end")
        except Exception as e:
            self.conn.rollback()
            messagebox.showerror("Error", str(e))
        finally:
            cur.close()

    def eliminar_usuario(self):
        if self.usuario_id_actual is None:
            messagebox.showwarning("Error", "Seleccione un usuario")
            return

        cur = self.conn.cursor()
        try:
            cur.execute(
                "DELETE FROM usuario WHERE id_usuario=%s",
                (self.usuario_id_actual,)
            )
            self.conn.commit()
            messagebox.showinfo("Eliminado", "Usuario eliminado")
            self.limpiar_campos()
            self.listar_usuarios()
        except Exception as e:
            self.conn.rollback()
            messagebox.showerror("Error", str(e))
        finally:
            cur.close()

    def buscar_usuario(self):
        texto = self.busqueda_entry.get().strip()
        cur = self.conn.cursor()

        cur.execute("""
            SELECT * FROM usuario
            WHERE usuario ILIKE %s OR nombre_completo ILIKE %s
            ORDER BY usuario
        """, (f"%{texto}%", f"%{texto}%"))

        usuarios = cur.fetchall()
        cur.close()
        self.mostrar_usuarios(usuarios)

    def listar_usuarios(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM usuario ORDER BY usuario")
        usuarios = cur.fetchall()
        cur.close()
        self.mostrar_usuarios(usuarios)

    # --------------------------------------------------
    # UTILIDADES
    # --------------------------------------------------

    def mostrar_usuarios(self, usuarios):
        self.lista.configure(state="normal")
        self.lista.delete("1.0", "end")

        for u in usuarios:
            estado = "Activo" if u[5] else "Inactivo"
            self.lista.insert(
                "end", f"{u[0]} - {u[1]} - {u[3]} - {estado}\n"
            )

        self.lista.configure(state="disabled")
        self.total_label.configure(text=f"Total usuarios: {len(usuarios)}")
        self.usuarios_cache = usuarios

    def seleccionar_usuario(self, event):
        try:
            index = self.lista.index(f"@{event.x},{event.y}")
            linea = int(index.split(".")[0]) - 1
            u = self.usuarios_cache[linea]

            self.usuario_id_actual = u[0]

            self.usuario_entry.delete(0, "end")
            self.usuario_entry.insert(0, u[1])

            self.nombre_entry.delete(0, "end")
            self.nombre_entry.insert(0, u[4])

            self.rol_option.set(u[3])
            self.estado_check.select() if u[5] else self.estado_check.deselect()

            self.pass_entry.delete(0, "end")
            self.pass2_entry.delete(0, "end")
        except:
            pass

    def limpiar_campos(self):
        self.usuario_id_actual = None
        self.usuario_entry.delete(0, "end")
        self.nombre_entry.delete(0, "end")
        self.pass_entry.delete(0, "end")
        self.pass2_entry.delete(0, "end")
        self.estado_check.deselect()


if __name__ == "__main__":
    app = gestionUsuarios()
    app.mainloop()
