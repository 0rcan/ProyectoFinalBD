import customtkinter as ctk
from PIL import Image
from customtkinter import CTkImage
import os

# ================== CONFIGURACIÓN GENERAL ==================
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class MenuVendedor(ctk.CTk):
    def __init__(self, rol="Vendedor"):
        super().__init__()
        
        # 1. Configuración de la Ventana
        self.title("Menú Principal - Confecciones Valle")
        self.geometry("480x550") # Ventana más compacta
        self.resizable(False, False)
        
        # 2. Frame Contenedor Principal
        main_container = ctk.CTkFrame(self, fg_color="#f0f0f0")
        main_container.pack(fill="both", expand=True)
        


       # 3. Frame para el Encabezado
        header_frame = ctk.CTkFrame(main_container, fg_color="#e8e8e8")
        header_frame.pack(fill="both", expand=True)
        
        header_frame.grid_columnconfigure((1, 0), weight=1)
        header_frame.grid_rowconfigure((1, 0), weight=1)
        
        self.create_header(header_frame,rol)


        
        # 4. Frame para el Contenido Central (Grid 2x2)
        content_frame = ctk.CTkFrame(main_container, fg_color="#f0f0f0")
        content_frame.pack(padx=10, pady=20, fill="both", expand=True)
        
        # Configuración del grid dentro del content_frame
        content_frame.grid_columnconfigure((0, 1), weight=1, minsize=200)
        content_frame.grid_rowconfigure((0, 1), weight=1, minsize=100)


        # Crear 4 botones 2x2

        # Helper para cargar imágenes de forma segura relativa al archivo
        def load_icon(filename: str, size: tuple[int, int]):
            try:
                base_dir = os.path.dirname(__file__)
                img_path = os.path.join(base_dir, "Imagenes", filename)
                if not os.path.exists(img_path):
                    raise FileNotFoundError(img_path)
                return CTkImage(Image.open(img_path), size=size)
            except Exception as e:
                # Si falla, devuelve None para crear botón solo con texto
                print(f"Advertencia: no se pudo cargar la imagen '{filename}': {e}")
                return None
        
        # CLIENTES
        # Imagen para el botón de Clientes
        cliente_image = load_icon("cliente.png", size=(40, 40))
        
        # Botón de Clientes
        btn_clientes = ctk.CTkButton(content_frame, text="Clientes consultar/registrar", 
            command=lambda: self.consultar_cliente("Clientes"),
            fg_color="#e9ecef", text_color="#000000", hover_color="#c0c4c8",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=60,
            image=cliente_image, compound="top" if cliente_image else None)  # Agregar la imagen arriba del texto si existe
        btn_clientes.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")


        # PEDIDOS
        # Imagen para el botón de Pedidos
        pedidos_image = load_icon("carrito.png", size=(40, 40))
        
        # Botón de Pedidos
        btn_pedidos = ctk.CTkButton(content_frame, text="Nuevo pedidos", 
            command=lambda: self.nuevo_pedidos("Pedidos"),
            fg_color="#e9ecef", text_color="#000000", hover_color="#c0c4c8",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=60,
            image=pedidos_image, compound="top" if pedidos_image else None)
        btn_pedidos.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")


        # PRODUCTOS
        # Imagen para el botón de Productos
        productos_image = load_icon("caja.png", size=(40, 40))
        
        # Botón de Productos
        btn_productos = ctk.CTkButton(content_frame, text="Pedidos cliente", 
            command=lambda: self.pedidos_cliente("Productos"),
            fg_color="#e9ecef", text_color="#000000", hover_color="#c0c4c8",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=60,
            image=productos_image, compound="top" if productos_image else None)
        btn_productos.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")


        # REPORTES
        # Imagen para el botón de Reportes
        reportes_image = load_icon("aprobar.png", size=(40, 40))
        
        # Botón de Reportes
        btn_reportes = ctk.CTkButton(content_frame, text="Entregar y facturar", 
            command=lambda: self.entregar_factura("Reportes"),
            fg_color="#e9ecef", text_color="#000000", hover_color="#c0c4c8",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=60,
            image=reportes_image, compound="top" if reportes_image else None)
        btn_reportes.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        
        
        # 6. Botón de Cerrar Sesión
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
        


    def consultar_cliente(self, modulo):
        """Función para manejar consulta de clientes."""
        print(f"Acción seleccionada: {modulo}")
          # Cerrar la ventana actual
        from RegistrarConsultarCliente import RegistrarConsultarCliente
        app = RegistrarConsultarCliente()
        app.mainloop()
        # Aquí iría el código para abrir la ventana de Clientes

    def nuevo_pedidos(self, modulo):
        print(f"Acción seleccionada: {modulo}")
        
        from NuevoPedido import NuevoPedido
        app = NuevoPedido()
        app.mainloop()
        

    def pedidos_cliente(self, modulo):
        print (f"Acción seleccionada: {modulo}")
        from PedidosPendientes import PedidosPendientes
        app = PedidosPendientes()
        app.mainloop()

    def entregar_factura(self, modulo):
        print (f"Acción seleccionada: {modulo}")
        
        from EntregaPedido import EntregaPedido
        app = EntregaPedido()
        app.mainloop()

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