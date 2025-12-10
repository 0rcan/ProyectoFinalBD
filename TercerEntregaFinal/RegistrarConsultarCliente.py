import customtkinter as ctk
import psycopg2
from tkinter import messagebox

# Configuración de apariencia de CustomTkinter
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class RegistrarConsultarCliente(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Configuración de la Ventana Principal ---
        self.title("REGISTRAR/CONSULTAR CLIENTE")
        self.geometry("600x700")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Conexión a la Base de Datos ---
        try:
            self.conn = psycopg2.connect(
                host="localhost",           # Servidor pgadmin
                user="postgres",            # Usuario
                password="josue",           # Contraseña
                dbname="ProyectoFinalEntrega2" # Base de datos
            )
        except Exception as e:
            messagebox.showerror("Error de Conexión", f"No se pudo conectar a la base de datos: {e}")
            self.conn = None

        # --- Frame Principal (para centrar y organizar) ---
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)

        # ----------------------------------------------------------------------
        #                       SECCIÓN DE CONSULTA
        # ----------------------------------------------------------------------

        ## Título de la sección
        ctk.CTkLabel(self.main_frame, text="REGISTRAR/CONSULTAR CLIENTE", 
                     font=ctk.CTkFont(size=20, weight="bold")).grid(row=0, column=0, pady=(0, 20))

        ## Campo de Búsqueda (Solo por ID/Documento)
        # Se usa 'id_cliente' para la búsqueda.
        self.search_label = ctk.CTkLabel(self.main_frame, text="Buscar cliente: [ID de Cliente]", anchor="w")
        self.search_label.grid(row=1, column=0, sticky="ew", padx=10)
        
        self.search_entry = ctk.CTkEntry(self.main_frame, placeholder_text="ID_cliente (e.g., 101)")
        self.search_entry.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 10))
        
        # Botón de Búsqueda
        self.search_button = ctk.CTkButton(self.main_frame, text="Buscar Cliente", command=self.buscar_cliente)
        self.search_button.grid(row=3, column=0, sticky="ew", padx=10, pady=(0, 20))

        ## Resultado Encontrado
        ctk.CTkLabel(self.main_frame, text="Resultado encontrado:", anchor="w").grid(row=4, column=0, sticky="w", padx=10)
        
        # Labels para mostrar el resultado
        self.result_id_nombre = ctk.CTkLabel(self.main_frame, text="", anchor="w", 
                                             font=ctk.CTkFont(size=14, weight="bold"))
        self.result_id_nombre.grid(row=5, column=0, sticky="w", padx=10)
        
        self.result_tel = ctk.CTkLabel(self.main_frame, text="", anchor="w")
        self.result_tel.grid(row=6, column=0, sticky="w", padx=10, pady=(0, 10))

        # --- Botón de Regresar ---
        self.return_button = ctk.CTkButton(self.main_frame, text="[ Regresar a Menú de Vendedor ]", 
                                          command=self.regresar_menu)
        self.return_button.grid(row=7, column=0, sticky="ew", padx=10, pady=(10, 30))

        # ----------------------------------------------------------------------
        #                       SECCIÓN DE REGISTRO RÁPIDO
        # ----------------------------------------------------------------------
        
        ctk.CTkLabel(self.main_frame, text="¿Cliente nuevo? → Registrar rápido:", 
                     font=ctk.CTkFont(size=16, weight="bold")).grid(row=8, column=0, sticky="w", padx=10, pady=(10, 5))
        
        # Campo ID Cliente
        ctk.CTkLabel(self.main_frame, text="ID de Cliente:", anchor="w").grid(row=9, column=0, sticky="w", padx=10)
        self.id_entry = ctk.CTkEntry(self.main_frame)
        self.id_entry.grid(row=10, column=0, sticky="ew", padx=10, pady=(0, 5))

        # Campo Nombre Completo
        ctk.CTkLabel(self.main_frame, text="Nombre Completo:", anchor="w").grid(row=11, column=0, sticky="w", padx=10)
        self.name_entry = ctk.CTkEntry(self.main_frame)
        self.name_entry.grid(row=12, column=0, sticky="ew", padx=10, pady=(0, 5))

        # Campo Teléfono
        ctk.CTkLabel(self.main_frame, text="Teléfono:", anchor="w").grid(row=13, column=0, sticky="w", padx=10)
        self.phone_entry = ctk.CTkEntry(self.main_frame)
        self.phone_entry.grid(row=14, column=0, sticky="ew", padx=10, pady=(0, 10))

        ## Botón "Crear cliente y continuar"
        self.create_client_button = ctk.CTkButton(self.main_frame, text="[ Crear cliente y continuar ]", 
                                                  command=self.crear_cliente)
        self.create_client_button.grid(row=15, column=0, sticky="ew", padx=10, pady=(20, 0))

    # ----------------------------------------------------------------------
    #                          MÉTODOS DE LA LÓGICA
    # ----------------------------------------------------------------------

    def buscar_cliente(self):
        """Busca un cliente SOLO por su ID de Cliente en la base de datos."""
        id_cliente = self.search_entry.get().strip()
        if not id_cliente:
            messagebox.showwarning("Advertencia", "Por favor, ingrese el ID del cliente para buscar.")
            return

        if not self.conn:
            return

        try:
            cursor = self.conn.cursor()
            # Se usan los nombres de columnas de tu base de datos: id_cliente, nombre_completo, telefono
            sql = """
            SELECT id_cliente, nombre_completo, telefono 
            FROM cliente 
            WHERE CAST(id_cliente AS TEXT) = %s;
            """
            
            cursor.execute(sql, (id_cliente,))
            cliente = cursor.fetchone()
            cursor.close()

            if cliente:
                id_cliente, nombre_completo, telefono = cliente
                # Mostrar el resultado
                self.result_id_nombre.configure(text=f"{id_cliente} - {nombre_completo.upper()}")
                self.result_tel.configure(text=f"Tel: {telefono}")
            else:
                self.result_id_nombre.configure(text="Cliente NO encontrado.")
                self.result_tel.configure(text="")
                messagebox.showinfo("Resultado", f"No se encontró un cliente con el ID: {id_cliente}.")

        except Exception as e:
            messagebox.showerror("Error de Búsqueda", f"Ocurrió un error al buscar el cliente: {e}")

    def regresar_menu(self):
        """Maneja la acción de regresar al menú de vendedor."""
        messagebox.showinfo("Regresar", "Regresando al Menú de Vendedor...")
        self.destroy() 
        from VendedorMenu import MenuVendedor
        menu = MenuVendedor(rol="Vendedor")
        menu.mainloop()


    def crear_cliente(self):
        """Registra un nuevo cliente en la base de datos."""
        id_cliente = self.id_entry.get().strip()
        nombre_completo = self.name_entry.get().strip()
        telefono = self.phone_entry.get().strip()

        if not id_cliente or not nombre_completo or not telefono:
            messagebox.showwarning("Advertencia", "Todos los campos de registro son obligatorios.")
            return

        if not self.conn:
            return

        try:
            cursor = self.conn.cursor()
            # Se usan los nombres de columnas de tu base de datos: id_cliente, nombre_completo, telefono
            sql = """
            INSERT INTO cliente (id_cliente, nombre_completo, telefono) 
            VALUES (%s, %s, %s) 
            RETURNING id_cliente, nombre_completo, telefono;
            """
            cursor.execute(sql, (id_cliente, nombre_completo, telefono))
            self.conn.commit()
            
            nuevo_cliente = cursor.fetchone() 
            cursor.close()
            
            messagebox.showinfo("Registro Exitoso", f"Cliente {nombre_completo} registrado. Continuando con la operación...")
            

        except psycopg2.errors.UniqueViolation:
            messagebox.showerror("Error de Registro", f"El ID de cliente {id_cliente} ya existe en la base de datos.")
            self.conn.rollback() 
        except Exception as e:
            messagebox.showerror("Error de Registro", f"Ocurrió un error al registrar el cliente: {e}")
            self.conn.rollback()

# ----------------------------------------------------------------------
#                      EJECUCIÓN DE LA APLICACIÓN
# ----------------------------------------------------------------------
if __name__ == "__main__":
    app = RegistrarConsultarCliente()
    app.mainloop()