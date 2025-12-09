import customtkinter as ctk
from PIL import Image
from customtkinter import CTkImage

# ================== CONFIGURACIÓN GENERAL ==================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class MenuVendedor(ctk.CTk):
    def __init__(self, rol="Vendedor"):
        super().__init__()
        
        # 1. Configuración de la Ventana (Reducción de tamaño)
        self.title("Menú Principal - Confecciones Valle")
        self.geometry("480x550") # Ventana más compacta
        self.resizable(False, False)
        
        # 2. Frame Contenedor Principal (para el borde externo)
        main_container = ctk.CTkFrame(self, fg_color="#f0f0f0")
        main_container.pack(fill="both", expand=True)
        


       
        header_frame = ctk.CTkFrame(main_container, fg_color="#e8e8e8")
        header_frame.pack(fill="both", expand=True)
        
        header_frame.grid_columnconfigure((1, 0), weight=1)
        header_frame.grid_rowconfigure((1, 0), weight=1)
        
        # Encabezado
        self.create_header(header_frame,rol)


        
        # 4. Frame para el Contenido Central (Grid 2x2)
        content_frame = ctk.CTkFrame(main_container, fg_color="#f0f0f0")
        content_frame.pack(padx=10, pady=20, fill="both", expand=True)
        
        # Configuración del grid dentro del content_frame
        content_frame.grid_columnconfigure((0, 1), weight=1, minsize=200)
        content_frame.grid_rowconfigure((0, 1), weight=1, minsize=100)


        # Crear 4 botones 2x2
        
        # CLIENTES
        cliente_image = CTkImage(Image.open("Imagenes/cliente.png"), size=(40, 40))
        
        btn_clientes = ctk.CTkButton(content_frame, text="Clientes consultar/registrar", 
            command=lambda: self.handle_action("Clientes"),
            fg_color="#e9ecef", text_color="#000000", hover_color="#c0c4c8",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=60,
            image=cliente_image, compound="top")  # Agregar la imagen arriba del texto
        btn_clientes.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")


        # PEDIDOS
        pedidos_image = CTkImage(Image.open("Imagenes/carrito.png"), size=(40, 40))
        
        btn_pedidos = ctk.CTkButton(content_frame, text="Nuevo pedidos", 
            command=lambda: self.handle_action("Pedidos"),
            fg_color="#e9ecef", text_color="#000000", hover_color="#c0c4c8",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=60,
            image=pedidos_image, compound="top")
        btn_pedidos.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")


        # PRODUCTOS
        productos_image = CTkImage(Image.open("Imagenes/caja.png"), size=(40, 40))
        
        btn_productos = ctk.CTkButton(content_frame, text="Pedidos cliente", 
            command=lambda: self.handle_action("Productos"),
            fg_color="#e9ecef", text_color="#000000", hover_color="#c0c4c8",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=60,
            image=productos_image, compound="top")
        btn_productos.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")


        # REPORTES
        reportes_image = CTkImage(Image.open("Imagenes/aprobar.png"), size=(40, 40))
        
        btn_reportes = ctk.CTkButton(content_frame, text="Entregar y facturar", 
            command=lambda: self.handle_action("Reportes"),
            fg_color="#e9ecef", text_color="#000000", hover_color="#c0c4c8",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=60,
            image=reportes_image, compound="top")
        btn_reportes.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        
        
        # 6. Botón de Cerrar Sesión (Reubicado en el main_container)
        ctk.CTkButton(main_container, text="CERRAR SESIÓN", 
                      command=self.cerrar_sesion, 
                      fg_color="#2c3e50", hover_color="#345869",
                      font=ctk.CTkFont(size=14)).pack(pady=(5, 20), padx=20)


    def create_header(self, parent, rol):
        """Crea el encabezado de bienvenida."""
        header_text = f"BIENVENIDO - ({rol})"
        
        ctk.CTkLabel(parent, text=header_text, 
                     font=ctk.CTkFont(size=16, weight="bold"),
                     text_color="#000000").pack(expand=True)
        


    def handle_action(self, action_name):
        """Función de ejemplo para manejar el clic en cada panel."""
        print(f"Acción seleccionada: {action_name}")
        # Aquí iría el código para abrir la ventana de Clientes, Pedidos, etc.

    def cerrar_sesion(self):
        """Cierra la ventana actual."""
        print("Cerrando Sesión...")
        # Lógica para volver a la ventana de Login
        self.destroy()
        from Login import LoginApp
        login = LoginApp()
        login.mainloop()

if __name__ == "__main__":
    app = MenuVendedor()
    app.mainloop()