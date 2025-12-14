import customtkinter as ctk
from tkinter import messagebox
import psycopg2
from datetime import datetime
from conexion import obtener_conexion
import os

# Configuración de apariencia
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class PedidosPendientes(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configuración de la ventana
        self.title("Confecciones Valle - Pedidos Pendientes")
        self.geometry("950x700")
        self.resizable(False, False)
        self.configure(fg_color="#f8f9fa")
        
        # Conexión a PostgreSQL
        try:
            self.conn = psycopg2.connect(
                host=os.getenv("DB_HOST", "localhost"),   # Servidor pgAdmin
                user=os.getenv("DB_USER"),                # Usuario
                password=os.getenv("DB_PASSWORD"),        # Contraseña
                dbname=os.getenv("DB_NAME", "ProyectoFinal") # Nombre de la base de datos
            )
            self.cursor = self.conn.cursor()
            print("Conexión a PostgreSQL establecida con éxito.")
        except psycopg2.Error as e:
            messagebox.showerror("Error de Conexión", f"No se pudo conectar a PostgreSQL: {e}")
            self.destroy()
            return
        
        # ================== BARRA SUPERIOR ==================
        top_bar = ctk.CTkFrame(self, height=60, fg_color="#e9ecef", corner_radius=0)
        top_bar.pack(fill="x")
        top_bar.pack_propagate(False)
        
        ctk.CTkLabel(top_bar, text="PEDIDOS PENDIENTES",
                     font=ctk.CTkFont(size=24, weight="bold"),
                     text_color="#212529").pack(side="left", padx=30, pady=5)
        
        # ================== CONTENEDOR PRINCIPAL ==================
        main_container = ctk.CTkFrame(self, fg_color="#f8f9fa")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # ================== BARRA DE BÚSQUEDA ==================
        search_frame = ctk.CTkFrame(main_container, fg_color="#e9ecef", corner_radius=10)
        search_frame.pack(fill="x", pady=(0, 15))
        
        search_content = ctk.CTkFrame(search_frame, fg_color="transparent")
        search_content.pack(fill="x", padx=15, pady=15)
        
        ctk.CTkLabel(search_content, text="Buscar:",
                     text_color="#212529",
                     font=ctk.CTkFont(size=14)).pack(side="left", padx=(0, 10))
        
        self.entry_buscar = ctk.CTkEntry(search_content, width=300,
                                         placeholder_text="ID Pedido, Cliente o Fecha")
        self.entry_buscar.pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(search_content, text="[ Actualizar ]",
                      width=150,
                      fg_color="#2c3e50", hover_color="#345869",
                      command=self.cargar_pedidos).pack(side="left")
        
        # ================== TABLA DE PEDIDOS ==================
        table_frame = ctk.CTkFrame(main_container, fg_color="#e9ecef", corner_radius=10)
        table_frame.pack(fill="both", expand=True, pady=(0, 15))
        
        # Encabezados de la tabla
        headers_frame = ctk.CTkFrame(table_frame, fg_color="#d0d3d6", corner_radius=5)
        headers_frame.pack(fill="x", padx=15, pady=(15, 0))
        
        headers = [
            ("#", 60),
            ("Fecha", 100),
            ("Cliente", 200),
            ("Total", 100),
            ("Acción", 150)
        ]
        
        for header, width in headers:
            ctk.CTkLabel(headers_frame, text=header, width=width,
                         font=ctk.CTkFont(size=12, weight="bold"),
                         text_color="#212529").pack(side="left", padx=5, pady=8)
        
        # Área scrollable para los pedidos
        self.pedidos_scroll = ctk.CTkScrollableFrame(table_frame,
                                                     fg_color="transparent",
                                                     height=400)
        self.pedidos_scroll.pack(fill="both", expand=True, padx=15, pady=10)
        
        # ================== INFORMACIÓN TOTAL ==================
        info_frame = ctk.CTkFrame(main_container, fg_color="#e9ecef", corner_radius=10)
        info_frame.pack(fill="x", pady=(0, 15))
        
        self.label_total_pedidos = ctk.CTkLabel(info_frame, 
                                                text="Total pendientes: 0 pedidos",
                                                font=ctk.CTkFont(size=14, weight="bold"),
                                                text_color="#212529")
        self.label_total_pedidos.pack(pady=15)
        
        # ================== BOTÓN CERRAR ==================
        ctk.CTkButton(main_container, text="[ Cerrar ]",
                      width=200, height=40,
                      fg_color="#6c757d", hover_color="#5a6268",
                      font=ctk.CTkFont(size=14),
                      command=self.cerrar).pack()
        
        # Cargar pedidos al iniciar
        self.cargar_pedidos()
    
    # ================== MÉTODOS DE LÓGICA ==================
    
    def cargar_pedidos(self):
        """Carga todos los pedidos pendientes desde la base de datos."""
        # Limpiar tabla
        for widget in self.pedidos_scroll.winfo_children():
            widget.destroy()
        
        try:
            busqueda = self.entry_buscar.get().strip()
            
            if busqueda:
                # Búsqueda con filtro
                # Según el diagrama: pedido tiene abono, no hay campo pago separado en pedido
                # factura_venta tiene pago
                query = """
                    SELECT p.id_pedido, p.fecha_encargo, c.nombre_completo, 
                           COALESCE(p.abono, 0), p.estado
                    FROM pedido p
                    JOIN cliente c ON p.id_cliente = c.id_cliente
                    WHERE (p.estado IS NULL OR p.estado != 'Entregado')
                    AND (CAST(p.id_pedido AS TEXT) LIKE %s 
                         OR c.nombre_completo ILIKE %s
                         OR TO_CHAR(p.fecha_encargo, 'DD-Mon') ILIKE %s)
                    ORDER BY p.fecha_encargo DESC
                """
                self.cursor.execute(query, (f"%{busqueda}%", f"%{busqueda}%", f"%{busqueda}%"))
            else:
                # Cargar todos los pedidos pendientes
                query = """
                    SELECT p.id_pedido, p.fecha_encargo, c.nombre_completo, 
                           COALESCE(p.abono, 0), p.estado
                    FROM pedido p
                    JOIN cliente c ON p.id_cliente = c.id_cliente
                    WHERE (p.estado IS NULL OR p.estado != 'Entregado')
                    ORDER BY p.fecha_encargo DESC
                """
                self.cursor.execute(query)
            
            pedidos = self.cursor.fetchall()
            
            # Mostrar pedidos
            for pedido in pedidos:
                self.crear_fila_pedido(pedido)
            
            # Actualizar contador
            self.label_total_pedidos.configure(
                text=f"Total pendientes: {len(pedidos)} pedidos"
            )
            
            if len(pedidos) == 0:
                ctk.CTkLabel(self.pedidos_scroll,
                            text="No hay pedidos pendientes",
                            font=ctk.CTkFont(size=14),
                            text_color="#6c757d").pack(pady=50)
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar pedidos: {e}")
            print(f"Detalle del error: {e}")
    
    def crear_fila_pedido(self, pedido):
        """Crea una fila en la tabla con la información del pedido."""
        id_pedido, fecha, cliente, abono, estado = pedido
        
        # Formatear fecha
        if isinstance(fecha, str):
            try:
                fecha_obj = datetime.strptime(fecha, "%Y-%m-%d")
            except:
                fecha_obj = datetime.now()
        else:
            fecha_obj = fecha
        fecha_formateada = fecha_obj.strftime("%d-%b")
        
        # Calcular total del pedido (suma de productos * precio)
        try:
            self.cursor.execute("""
                SELECT SUM(i.cantidad * pt.precio_venta)
                FROM incluye i
                JOIN producto_terminado pt ON i.codigo_prod = pt.codigo_prod
                WHERE i.id_pedido = %s
            """, (id_pedido,))
            resultado = self.cursor.fetchone()
            total = float(resultado[0]) if resultado and resultado[0] else 0.0
        except:
            total = 0.0
        
        # Frame para la fila
        row_frame = ctk.CTkFrame(self.pedidos_scroll, fg_color="#ffffff",
                                corner_radius=5, height=45)
        row_frame.pack(fill="x", pady=2)
        row_frame.pack_propagate(False)
        
        # Contenido de la fila
        content_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # ID Pedido
        ctk.CTkLabel(content_frame, text=str(id_pedido), width=60,
                     text_color="#212529",
                     font=ctk.CTkFont(size=13)).pack(side="left", padx=5)
        
        # Fecha
        ctk.CTkLabel(content_frame, text=fecha_formateada, width=100,
                     text_color="#212529",
                     font=ctk.CTkFont(size=13)).pack(side="left", padx=5)
        
        # Cliente
        ctk.CTkLabel(content_frame, text=cliente, width=200,
                     text_color="#212529",
                     font=ctk.CTkFont(size=13),
                     anchor="w").pack(side="left", padx=5)
        
        # Total
        if total >= 1000000:
            total_text = f"${total/1000000:.1f}M"
        elif total >= 1000:
            total_text = f"${total/1000:.0f}k"
        else:
            total_text = f"${total:.0f}"
            
        ctk.CTkLabel(content_frame, text=total_text, width=100,
                     text_color="#212529",
                     font=ctk.CTkFont(size=13)).pack(side="left", padx=5)
        
        # Botón Entregar
        ctk.CTkButton(content_frame, text="[ Entregar ]", width=140,
                      fg_color="#28a745", hover_color="#218838",
                      font=ctk.CTkFont(size=12),
                      command=lambda: self.entregar_pedido(id_pedido, cliente)
                      ).pack(side="left", padx=5)
    
    def entregar_pedido(self, id_pedido, cliente):
        """Marca un pedido como entregado."""
        respuesta = messagebox.askyesno(
            "Confirmar Entrega",
            f"¿Marcar como ENTREGADO el pedido #{id_pedido} de {cliente}?\n\n"
            "Esta acción cambiará el estado del pedido."
        )
        
        if respuesta:
            try:
                # Actualizar estado del pedido
                self.cursor.execute("""
                    UPDATE pedido 
                    SET estado = 'Entregado'
                    WHERE id_pedido = %s
                """, (id_pedido,))
                
                self.conn.commit()
                
                messagebox.showinfo("Éxito", 
                                   f"Pedido #{id_pedido} marcado como ENTREGADO")
                
                # Recargar la lista
                self.cargar_pedidos()
            
            except Exception as e:
                self.conn.rollback()
                messagebox.showerror("Error", f"Error al actualizar pedido: {e}")
    
    def cerrar(self):
        """Cierra la ventana y regresa al menú."""
        self.destroy()
        from VendedorMenu import MenuVendedor
        menu = MenuVendedor(rol="Vendedor")
        menu.mainloop()
    
    def __del__(self):
        """Cierra la conexión al destruir el objeto."""
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()

if __name__ == "__main__":
    app = PedidosPendientes()
    app.mainloop()