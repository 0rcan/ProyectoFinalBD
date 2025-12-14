import customtkinter as ctk
from tkinter import messagebox
import psycopg2
from datetime import datetime, timedelta
from conexion import obtener_conexion
import os

# Configuración de apariencia
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class NuevoPedido(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configuración de la ventana
        self.title("Confecciones Valle - Nuevo Pedido")
        self.geometry("900x750")
        self.resizable(False, False)
        self.configure(fg_color="#f8f9fa")
        
        # Lista de productos en el pedido
        self.productos_pedido = []
        
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
        
        ctk.CTkLabel(top_bar, text="NUEVO PEDIDO",
                     font=ctk.CTkFont(size=24, weight="bold"),
                     text_color="#212529").pack(side="left", padx=30, pady=5)
        
        # ================== CONTENEDOR PRINCIPAL ==================
        main_container = ctk.CTkScrollableFrame(self, fg_color="#f8f9fa")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # ================== SECCIÓN CLIENTE ==================
        cliente_frame = ctk.CTkFrame(main_container, fg_color="#e9ecef", corner_radius=10)
        cliente_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(cliente_frame, text="INFORMACIÓN DEL CLIENTE",
                     font=ctk.CTkFont(size=16, weight="bold"),
                     text_color="#212529").pack(pady=(10, 5), padx=15, anchor="w")
        
        # Frame para búsqueda de cliente
        buscar_frame = ctk.CTkFrame(cliente_frame, fg_color="transparent")
        buscar_frame.pack(fill="x", padx=15, pady=10)
        
        ctk.CTkLabel(buscar_frame, text="ID Cliente:",
                     text_color="#212529").pack(side="left", padx=(0, 10))
        
        self.entry_id_cliente = ctk.CTkEntry(buscar_frame, width=150,
                                             placeholder_text="[1032456789]")
        self.entry_id_cliente.pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(buscar_frame, text="Buscar", width=100,
                      fg_color="#2c3e50", hover_color="#345869",
                      command=self.buscar_cliente).pack(side="left")
        
        # Labels para mostrar información del cliente
        self.label_cliente = ctk.CTkLabel(cliente_frame, text="Cliente: -",
                                          font=ctk.CTkFont(size=14),
                                          text_color="#212529")
        self.label_cliente.pack(pady=5, padx=15, anchor="w")
        
        # ================== SECCIÓN PRODUCTO ==================
        producto_frame = ctk.CTkFrame(main_container, fg_color="#e9ecef", corner_radius=10)
        producto_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(producto_frame, text="AGREGAR PRODUCTO",
                     font=ctk.CTkFont(size=16, weight="bold"),
                     text_color="#212529").pack(pady=(10, 5), padx=15, anchor="w")
        
        # Selector de producto y colegio
        selector_frame = ctk.CTkFrame(producto_frame, fg_color="transparent")
        selector_frame.pack(fill="x", padx=15, pady=10)
        
        # Producto
        prod_left = ctk.CTkFrame(selector_frame, fg_color="transparent")
        prod_left.pack(side="left", expand=True, fill="x", padx=(0, 10))
        
        ctk.CTkLabel(prod_left, text="Producto:",
                     text_color="#212529").pack(anchor="w")
        
        self.combo_producto = ctk.CTkComboBox(prod_left, 
                                              values=["Seleccione..."],
                                              width=300,
                                              state="readonly")
        self.combo_producto.pack(fill="x", pady=(5, 0))
        
        # Colegio
        cole_right = ctk.CTkFrame(selector_frame, fg_color="transparent")
        cole_right.pack(side="left", expand=True, fill="x")
        
        ctk.CTkLabel(cole_right, text="Colegio:",
                     text_color="#212529").pack(anchor="w")
        
        self.combo_colegio = ctk.CTkComboBox(cole_right,
                                             values=["Seleccione..."],
                                             width=300,
                                             state="readonly")
        self.combo_colegio.pack(fill="x", pady=(5, 0))
        
        # Medidas y Cantidad
        detalles_frame = ctk.CTkFrame(producto_frame, fg_color="transparent")
        detalles_frame.pack(fill="x", padx=15, pady=10)
        
        # Medidas
        medidas_frame = ctk.CTkFrame(detalles_frame, fg_color="transparent")
        medidas_frame.pack(side="left", expand=True, fill="x", padx=(0, 10))
        
        ctk.CTkLabel(medidas_frame, text="Medidas:",
                     text_color="#212529").pack(anchor="w")
        
        self.entry_medidas = ctk.CTkEntry(medidas_frame,
                                          placeholder_text="[Pecho: 76, Largo: 58]")
        self.entry_medidas.pack(fill="x", pady=(5, 0))
        
        # Cantidad
        cantidad_frame = ctk.CTkFrame(detalles_frame, fg_color="transparent")
        cantidad_frame.pack(side="left", expand=True, fill="x")
        
        ctk.CTkLabel(cantidad_frame, text="Cantidad:",
                     text_color="#212529").pack(anchor="w")
        
        self.entry_cantidad = ctk.CTkEntry(cantidad_frame, width=100,
                                           placeholder_text="1")
        self.entry_cantidad.pack(fill="x", pady=(5, 0))
        
        # Botón agregar producto
        ctk.CTkButton(producto_frame, text="[ Agregar ]", width=200,
                      fg_color="#2c3e50", hover_color="#345869",
                      command=self.agregar_producto).pack(pady=10)
        
        # ================== TABLA DE PRODUCTOS ==================
        tabla_frame = ctk.CTkFrame(main_container, fg_color="#e9ecef", corner_radius=10)
        tabla_frame.pack(fill="both", expand=True, pady=(0, 15))
        
        ctk.CTkLabel(tabla_frame, text="PRODUCTOS EN EL PEDIDO",
                     font=ctk.CTkFont(size=16, weight="bold"),
                     text_color="#212529").pack(pady=(10, 5), padx=15, anchor="w")
        
        # Encabezados de la tabla
        headers_frame = ctk.CTkFrame(tabla_frame, fg_color="#d0d3d6", corner_radius=5)
        headers_frame.pack(fill="x", padx=15, pady=(5, 0))
        
        ctk.CTkLabel(headers_frame, text="Producto", width=250,
                     font=ctk.CTkFont(size=12, weight="bold"),
                     text_color="#212529").pack(side="left", padx=10, pady=5)
        
        ctk.CTkLabel(headers_frame, text="Cantidad", width=80,
                     font=ctk.CTkFont(size=12, weight="bold"),
                     text_color="#212529").pack(side="left", padx=10, pady=5)
        
        ctk.CTkLabel(headers_frame, text="Medidas", width=150,
                     font=ctk.CTkFont(size=12, weight="bold"),
                     text_color="#212529").pack(side="left", padx=10, pady=5)
        
        ctk.CTkLabel(headers_frame, text="Acción", width=100,
                     font=ctk.CTkFont(size=12, weight="bold"),
                     text_color="#212529").pack(side="left", padx=10, pady=5)
        
        # Scrollable frame para productos
        self.productos_scroll = ctk.CTkScrollableFrame(tabla_frame, 
                                                       fg_color="transparent",
                                                       height=150)
        self.productos_scroll.pack(fill="both", expand=True, padx=15, pady=10)
        
        # ================== SECCIÓN TOTALES ==================
        totales_frame = ctk.CTkFrame(main_container, fg_color="#e9ecef", corner_radius=10)
        totales_frame.pack(fill="x", pady=(0, 15))
        
        # Total y Abono
        valores_frame = ctk.CTkFrame(totales_frame, fg_color="transparent")
        valores_frame.pack(fill="x", padx=15, pady=15)
        
        # Total
        total_frame = ctk.CTkFrame(valores_frame, fg_color="transparent")
        total_frame.pack(side="left", expand=True, fill="x", padx=(0, 20))
        
        ctk.CTkLabel(total_frame, text="Total:",
                     font=ctk.CTkFont(size=16, weight="bold"),
                     text_color="#212529").pack(side="left", padx=(0, 10))
        
        self.label_total = ctk.CTkLabel(total_frame, text="$0.00",
                                        font=ctk.CTkFont(size=20, weight="bold"),
                                        text_color="#2c3e50")
        self.label_total.pack(side="left")
        
        # Abono
        abono_frame = ctk.CTkFrame(valores_frame, fg_color="transparent")
        abono_frame.pack(side="left", expand=True, fill="x")
        
        ctk.CTkLabel(abono_frame, text="Abono:",
                     font=ctk.CTkFont(size=14),
                     text_color="#212529").pack(anchor="w")
        
        self.entry_abono = ctk.CTkEntry(abono_frame, width=150,
                                        placeholder_text="$0.00")
        self.entry_abono.pack(anchor="w", pady=(5, 0))
        
        # ================== BOTONES DE ACCIÓN ==================
        botones_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        botones_frame.pack(fill="x", pady=(0, 10))
        
        ctk.CTkButton(botones_frame, text="[ GUARDAR PEDIDO ]",
                      width=200, height=40,
                      fg_color="#2c3e50", hover_color="#345869",
                      font=ctk.CTkFont(size=14, weight="bold"),
                      command=self.guardar_pedido).pack(side="left", expand=True, padx=5)
        
        ctk.CTkButton(botones_frame, text="[ Cancelar ]",
                      width=200, height=40,
                      fg_color="#6c757d", hover_color="#5a6268",
                      font=ctk.CTkFont(size=14),
                      command=self.cancelar).pack(side="left", expand=True, padx=5)
        
        # Cargar datos iniciales
        self.cargar_productos()
        self.cargar_colegios()
    
    # ================== MÉTODOS DE LÓGICA ==================
    
    def buscar_cliente(self):
        """Busca un cliente por ID."""
        id_cliente = self.entry_id_cliente.get().strip()
        if not id_cliente:
            messagebox.showwarning("Advertencia", "Ingrese el ID del cliente.")
            return
        
        try:
            self.cursor.execute(
                "SELECT nombre_completo, telefono FROM cliente WHERE id_cliente = %s",
                (id_cliente,)
            )
            resultado = self.cursor.fetchone()
            
            if resultado:
                nombre, telefono = resultado
                self.label_cliente.configure(
                    text=f"Cliente: [{id_cliente}] {nombre} - Tel: {telefono}"
                )
            else:
                messagebox.showerror("Error", f"No se encontró cliente con ID: {id_cliente}")
                self.label_cliente.configure(text="Cliente: -")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al buscar cliente: {e}")
    
    def cargar_productos(self):
        """Carga los productos disponibles desde la base de datos."""
        try:
            self.cursor.execute(
                "SELECT codigo_prod, descripcion FROM producto_terminado"
            )
            productos = self.cursor.fetchall()
            
            valores = ["Seleccione..."] + [f"[{cod}] {desc}" for cod, desc in productos]
            self.combo_producto.configure(values=valores)
            self.combo_producto.set("Seleccione...")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar productos: {e}")
    
    def cargar_colegios(self):
        """Carga los colegios disponibles desde la base de datos."""
        try:
            self.cursor.execute("SELECT id_colegio, nombre FROM colegio")
            colegios = self.cursor.fetchall()
            
            valores = ["Seleccione..."] + [f"[{id_c}] {nombre}" for id_c, nombre in colegios]
            self.combo_colegio.configure(values=valores)
            self.combo_colegio.set("Seleccione...")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar colegios: {e}")
    
    def agregar_producto(self):
        """Agrega un producto a la lista del pedido."""
        producto = self.combo_producto.get()
        cantidad = self.entry_cantidad.get().strip()
        medidas = self.entry_medidas.get().strip()
        
        if producto == "Seleccione...":
            messagebox.showwarning("Advertencia", "Seleccione un producto.")
            return
        
        if not cantidad or not cantidad.isdigit():
            messagebox.showwarning("Advertencia", "Ingrese una cantidad válida.")
            return
        
        # Extraer código del producto
        codigo_prod = producto.split("]")[0].replace("[", "")
        
        # Agregar a la lista
        producto_info = {
            "codigo": codigo_prod,
            "nombre": producto,
            "cantidad": int(cantidad),
            "medidas": medidas if medidas else "Sin especificar"
        }
        
        self.productos_pedido.append(producto_info)
        self.actualizar_tabla_productos()
        self.calcular_total()
        
        # Limpiar campos
        self.entry_cantidad.delete(0, 'end')
        self.entry_medidas.delete(0, 'end')
    
    def actualizar_tabla_productos(self):
        """Actualiza la visualización de productos en la tabla."""
        # Limpiar tabla
        for widget in self.productos_scroll.winfo_children():
            widget.destroy()
        
        # Agregar productos
        for idx, prod in enumerate(self.productos_pedido):
            row_frame = ctk.CTkFrame(self.productos_scroll, fg_color="#ffffff",
                                     corner_radius=5)
            row_frame.pack(fill="x", pady=2)
            
            ctk.CTkLabel(row_frame, text=prod["nombre"], width=250,
                         text_color="#212529", anchor="w").pack(side="left", padx=10, pady=5)
            
            ctk.CTkLabel(row_frame, text=str(prod["cantidad"]), width=80,
                         text_color="#212529").pack(side="left", padx=10, pady=5)
            
            ctk.CTkLabel(row_frame, text=prod["medidas"], width=150,
                         text_color="#212529").pack(side="left", padx=10, pady=5)
            
            ctk.CTkButton(row_frame, text="Quitar", width=100,
                          fg_color="#dc3545", hover_color="#c82333",
                          command=lambda i=idx: self.quitar_producto(i)).pack(side="left", padx=10, pady=5)
    
    def quitar_producto(self, index):
        """Elimina un producto de la lista."""
        self.productos_pedido.pop(index)
        self.actualizar_tabla_productos()
        self.calcular_total()
    
    def calcular_total(self):
        """Calcula el total del pedido."""
        total = 0
        for prod in self.productos_pedido:
            try:
                self.cursor.execute(
                    "SELECT precio_venta FROM producto_terminado WHERE codigo_prod = %s",
                    (prod["codigo"],)
                )
                resultado = self.cursor.fetchone()
                if resultado:
                    precio = float(resultado[0])
                    total += precio * prod["cantidad"]
            except Exception as e:
                print(f"Error al calcular precio: {e}")
        
        self.label_total.configure(text=f"${total:,.2f}")
    
    def guardar_pedido(self):
        """Guarda el pedido en la base de datos."""
        id_cliente = self.entry_id_cliente.get().strip()
        abono = self.entry_abono.get().strip()
        
        if not id_cliente:
            messagebox.showwarning("Advertencia", "Debe buscar un cliente primero.")
            return
        
        if not self.productos_pedido:
            messagebox.showwarning("Advertencia", "Debe agregar al menos un producto.")
            return
        
        try:
            # Crear factura primero
            fecha_actual = datetime.now().date()
            total = float(self.label_total.cget("text").replace("$", "").replace(",", ""))
            abono_valor = float(abono) if abono else 0.0
            
            # Insertar factura
            self.cursor.execute("""
                INSERT INTO factura_venta (fecha, metodo_de_pago, pago)
                VALUES (%s, %s, %s) RETURNING id_factura
            """, (fecha_actual, "Pendiente", total))
            
            id_factura = self.cursor.fetchone()[0]
            
            # Insertar pedido
            fecha_estimada = fecha_actual + timedelta(days=15)
            self.cursor.execute("""
                INSERT INTO pedido (id_cliente, id_factura, estado, fecha_encargo, fecha_estimada, abono)
                VALUES (%s, %s, %s, %s, %s, %s) RETURNING id_pedido
            """, (id_cliente, id_factura, "Pendiente", fecha_actual, fecha_estimada, abono_valor))
            
            id_pedido = self.cursor.fetchone()[0]
            
            # Insertar productos del pedido
            for prod in self.productos_pedido:
                self.cursor.execute("""
                    INSERT INTO incluye (id_pedido, codigo_prod, medidas, cantidad)
                    VALUES (%s, %s, %s, %s)
                """, (id_pedido, prod["codigo"], prod["medidas"], prod["cantidad"]))
            
            self.conn.commit()
            
            messagebox.showinfo("Éxito", f"Pedido #{id_pedido} creado exitosamente.")
            self.limpiar_formulario()
        
        except Exception as e:
            self.conn.rollback()
            messagebox.showerror("Error", f"Error al guardar pedido: {e}")
    
    def limpiar_formulario(self):
        """Limpia todos los campos del formulario."""
        self.entry_id_cliente.delete(0, 'end')
        self.label_cliente.configure(text="Cliente: -")
        self.productos_pedido = []
        self.actualizar_tabla_productos()
        self.label_total.configure(text="$0.00")
        self.entry_abono.delete(0, 'end')
        self.combo_producto.set("Seleccione...")
        self.combo_colegio.set("Seleccione...")
    
    def cancelar(self):
        """Cancela y regresa al menú de vendedor."""
        if messagebox.askyesno("Confirmar", "¿Desea cancelar y regresar al menú?"):
            self.destroy()
            from VendedorMenu import MenuVendedor
            menu = MenuVendedor(rol="Vendedor")
            menu.mainloop()

if __name__ == "__main__":
    app = NuevoPedido()
    app.mainloop()
