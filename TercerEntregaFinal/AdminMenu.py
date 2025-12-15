# AdminMenu.py - Contenedor negro más pequeño y elegante
import customtkinter as ctk
from tkinter import messagebox


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class AdminMenu(ctk.CTk):
    def __init__(self, usuario="Admin"):
        super().__init__()
        self.title("Confecciones Valle - Panel Administrador")
        self.geometry("850x620")  # Ventana más pequeña
        self.resizable(False, False)
        self.configure(fg_color="#f8f9fa")

        # ================== BARRA SUPERIOR ==================
        top_bar = ctk.CTkFrame(self, height=60, fg_color="#e9ecef", corner_radius=0)
        top_bar.pack(fill="x")
        top_bar.pack_propagate(False)

        ctk.CTkLabel(top_bar, text="CONFECCIONES VALLE",
                     font=ctk.CTkFont(size=24, weight="bold"),
                     text_color="#212529").pack(side="left", padx=30, pady=5)

        ctk.CTkLabel(top_bar, text=usuario,
                     font=ctk.CTkFont(size=16),
                     text_color="#495057").pack(side="right", padx=30, pady=0)

        # ================== CONTENEDOR NEGRO MÁS PEQUEÑO ==================
        container = ctk.CTkFrame(self, 
                                 width=600,    # ← Más estrecho
                                 height=350,   # ← Más bajo
                                 fg_color="#e9ecef", 
                                 )
        container.pack(expand=True, pady=(50,0))  # Menos espacio arriba/abajo
        container.pack_propagate(False)

        content = ctk.CTkFrame(container, fg_color="transparent")
        content.pack( fill="both", padx=20, pady=0)  # Padding reducido

        # Columnas
        col_izq = ctk.CTkFrame(content, fg_color="transparent")
        col_izq.pack(side="left", expand=True, fill="both")
        col_der = ctk.CTkFrame(content, fg_color="transparent")
        col_der.pack(side="right", expand=True, fill="both")

        # Botones compactos
        self.boton_pequeno(col_izq, "Gestión de Usuarios", self.gestion_usuarios)
        self.boton_pequeno(col_izq, "Gestión de Clientes", self.gestion_clientes)
        self.boton_pequeno(col_izq, "Gestión de Proveedores", self.gestion_proveedores)
        self.boton_pequeno(col_izq, "Productos Terminados", self.productos_terminados)
        self.boton_pequeno(col_izq, "Reportes e Informes", self.reportes)

        self.boton_pequeno(col_der, "Gestión de Colegios", self.gestion_colegios)
        self.boton_pequeno(col_der, "Piezas de Uniforme", self.piezas_uniforme)
        self.boton_pequeno(col_der, "Materias Primas", self.materias_primas)
        self.boton_pequeno(col_der, "Pedidos y Facturación", self.pedidos_facturacion)

        # ================== BOTÓN CERRAR SESIÓN (bien visible) ==================
        ctk.CTkButton(self,
                      text="CERRAR SESIÓN",
                      command=self.cerrar_sesion, 
                      fg_color="#2c3e50", hover_color="#345869",
                      font=ctk.CTkFont(size=14)).pack(pady=(5, 10), padx=20)

        
        

    def boton_pequeno(self, parent, texto, comando):
        ctk.CTkButton(parent,
                      text=texto,
                      width=260, height=35,   # Botones más pequeños
                      corner_radius=12,
                      fg_color="transparent",
                      hover_color="#c0c4c8",
                      font=ctk.CTkFont(size=16),
                      text_color="#000000",
                      anchor="w",
                      command=comando
                      ).pack(pady=7, padx=8, fill="x")
        
        

    # =============== FUNCIONES ===============
    def gestion_usuarios(self):
        try:
            from gestionUsuarios import gestionUsuarios
            app = gestionUsuarios()
            app.mainloop()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    def gestion_clientes(self): 
        try:
            from gestionClientes import gestionCliente
            app = gestionCliente()
            app.mainloop()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir Gestión de Clientes: {e}")
    def gestion_proveedores(self): 
        try:
            from gestionProveedor import gestionProveedor
            app = gestionProveedor()
            app.mainloop()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir Gestión de Proveedores: {e}")
    def productos_terminados(self): 
        messagebox.showinfo("Admin", "Abriendo Productos Terminados")
    def reportes(self): 
        messagebox.showinfo("Admin", "Abriendo Reportes e Informes")
    def gestion_colegios(self):
        try:
            from GestionColegios import GestionColegios
            app = GestionColegios()
            app.mainloop()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    def piezas_uniforme(self):
        try:
            from gestionPiezas import gestionPiezas
            app = gestionPiezas()
            app.mainloop()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    def materias_primas(self): 
        try:
            from gestionMateriaPrima import GestionMateriaPrima
            app = GestionMateriaPrima()
            app.mainloop()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir Materias Primas: {e}")
    def pedidos_facturacion(self): 
        messagebox.showinfo("Admin", "Abriendo Pedidos y Facturación")

    def cerrar_sesion(self):
        
        if messagebox.askyesno("Cerrar Sesión", "¿Desea cerrar sesión y volver al login?"):
            self.destroy()
            from Login import LoginApp
            LoginApp().mainloop()


if __name__ == "__main__":
    app = AdminMenu("Admin")
    app.mainloop()