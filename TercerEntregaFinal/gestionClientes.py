from dotenv import load_dotenv
import customtkinter as ctk
import psycopg2
from tkinter import messagebox
import os

# Configuración de apariencia de CustomTkinter
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class gestionCliente(ctk.CTk):
    def __init__(self):
        super().__init__()
        load_dotenv()

        
        # --- Configuración de la Ventana Principal ---
        self.title("Gestion de Clientes")
        self.geometry("600x600")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Conexión a la Base de Datos ---
        try:
            self.conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),   # Servidor pgAdmin
            user=os.getenv("DB_USER"),                # Usuario
            password=os.getenv("DB_PASSWORD"),        # Contraseña
            dbname=os.getenv("DB_NAME", "ProyectoFinal")
            )
        except Exception as e:
           messagebox.showerror(
        "Error de Conexión",
        f"No se pudo conectar a la base de datos: {e}"
            )
        self.conn = None

        # --- Frame Principal (para centrar y organizar) ---
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self.main_frame, text="REGISTRAR/CONSULTAR CLIENTE", 
            font=ctk.CTkFont(size=20, weight="bold")).grid(row=0, column=0, pady=(0, 20))

        self.boton_eliminar_cliente = ctk.CTkButton(self.main_frame, text="Eliminar", command=self.button_eliminar_cliente)
        self.boton_eliminar_cliente.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))
        self.boton_guardar_cliente = ctk.CTkButton(self.main_frame, text="Guardar", command=self.button_guardar_cliente)



    def button_eliminar_cliente(self):
        messagebox.showinfo("Eliminar Cliente", "Funcionalidad para eliminar cliente aún no implementada.")

    def button_guardar_cliente(self):
        messagebox.showinfo("Guardar Cliente", "Funcionalidad para guardar cliente aún no implementada.")

if __name__ == "__main__":
    app = gestionCliente()
    app.mainloop()