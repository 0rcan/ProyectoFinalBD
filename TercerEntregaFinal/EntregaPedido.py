import customtkinter as ctk
from tkinter import messagebox
import psycopg2
from datetime import datetime

# Configuración de apariencia
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class EntregaPedido(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configuración de la ventana
        self.title("Confecciones Valle - Entrega de Pedido")
        self.geometry("700x750")
        self.resizable(False, False)
        self.configure(fg_color="#f8f9fa")
        
        # Variable para almacenar datos del pedido actual
        self.pedido_actual = None
        
        # Conexión a PostgreSQL
        try:
            self.conn = psycopg2.connect(
                host="localhost",
                user="postgres",
                password="josue",
                dbname="ProyectoFinalEntrega2"
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
        
        ctk.CTkLabel(top_bar, text="ENTREGA DE PEDIDO",
                     font=ctk.CTkFont(size=24, weight="bold"),
                     text_color="#212529").pack(side="left", padx=30, pady=5)
        
        # ================== CONTENEDOR PRINCIPAL ==================
        main_container = ctk.CTkScrollableFrame(self, fg_color="#f8f9fa")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # ================== BÚSQUEDA DE PEDIDO ==================
        busqueda_frame = ctk.CTkFrame(main_container, fg_color="#e9ecef", corner_radius=10)
        busqueda_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(busqueda_frame, text="BUSCAR PEDIDO",
                     font=ctk.CTkFont(size=16, weight="bold"),
                     text_color="#212529").pack(pady=(10, 5), padx=15, anchor="w")
        
        search_row = ctk.CTkFrame(busqueda_frame, fg_color="transparent")
        search_row.pack(fill="x", padx=15, pady=10)
        
        ctk.CTkLabel(search_row, text="ID Pedido:",
                     text_color="#212529").pack(side="left", padx=(0, 10))
        
        self.entry_id_pedido = ctk.CTkEntry(search_row, width=150,
                                            placeholder_text="0897")
        self.entry_id_pedido.pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(search_row, text="Buscar", width=120,
                      fg_color="#2c3e50", hover_color="#345869",
                      command=self.buscar_pedido).pack(side="left")
        
        # ================== INFORMACIÓN DEL PEDIDO ==================
        info_frame = ctk.CTkFrame(main_container, fg_color="#e9ecef", corner_radius=10)
        info_frame.pack(fill="x", pady=(0, 15))
        
        # Título del pedido
        self.label_titulo = ctk.CTkLabel(info_frame, 
                                         text="ENTREGA DE PEDIDO #----",
                                         font=ctk.CTkFont(size=18, weight="bold"),
                                         text_color="#212529")
        self.label_titulo.pack(pady=(15, 10), padx=15)
        
        # Cliente
        self.label_cliente = ctk.CTkLabel(info_frame, 
                                          text="Cliente: -",
                                          font=ctk.CTkFont(size=14),
                                          text_color="#212529")
        self.label_cliente.pack(pady=5, padx=15, anchor="w")
        
        # Información financiera
        financiero_frame = ctk.CTkFrame(info_frame, fg_color="#d0d3d6", corner_radius=8)
        financiero_frame.pack(fill="x", padx=15, pady=10)
        
        self.label_total = ctk.CTkLabel(financiero_frame,
                                        text="Total pedido: $0.000",
                                        font=ctk.CTkFont(size=14),
                                        text_color="#212529")
        self.label_total.pack(pady=5, padx=15, anchor="w")
        
        self.label_abono = ctk.CTkLabel(financiero_frame,
                                        text="Abono: $0.000",
                                        font=ctk.CTkFont(size=14),
                                        text_color="#212529")
        self.label_abono.pack(pady=5, padx=15, anchor="w")
        
        self.label_saldo = ctk.CTkLabel(financiero_frame,
                                        text="→ SALDO A COBRAR: $0.000",
                                        font=ctk.CTkFont(size=15, weight="bold"),
                                        text_color="#dc3545")
        self.label_saldo.pack(pady=5, padx=15, anchor="w")
        
        # ================== PAGO ==================
        pago_frame = ctk.CTkFrame(main_container, fg_color="#e9ecef", corner_radius=10)
        pago_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(pago_frame, text="PAGO HOY",
                     font=ctk.CTkFont(size=16, weight="bold"),
                     text_color="#212529").pack(pady=(10, 5), padx=15, anchor="w")
        
        pago_input_frame = ctk.CTkFrame(pago_frame, fg_color="transparent")
        pago_input_frame.pack(fill="x", padx=15, pady=10)
        
        ctk.CTkLabel(pago_input_frame, text="Pago hoy: [ $",
                     text_color="#212529",
                     font=ctk.CTkFont(size=14)).pack(side="left", padx=(0, 5))
        
        self.entry_pago = ctk.CTkEntry(pago_input_frame, width=150,
                                       placeholder_text="0.00")
        self.entry_pago.pack(side="left", padx=(0, 5))
        
        ctk.CTkLabel(pago_input_frame, text="]",
                     text_color="#212529",
                     font=ctk.CTkFont(size=14)).pack(side="left", padx=(0, 10))
        
        self.combo_metodo = ctk.CTkComboBox(pago_input_frame,
                                            values=["Efectivo", "Tarjeta", "Transferencia", "Mixto"],
                                            width=150,
                                            state="readonly")
        self.combo_metodo.set("Efectivo")
        self.combo_metodo.pack(side="left")
        
        # ================== VERIFICACIÓN ==================
        verificacion_frame = ctk.CTkFrame(main_container, fg_color="#e9ecef", corner_radius=10)
        verificacion_frame.pack(fill="x", pady=(0, 15))
        
        self.check_var = ctk.BooleanVar(value=False)
        self.checkbox = ctk.CTkCheckBox(verificacion_frame,
                                        text="[X] Cliente revisó y aprueba las prendas",
                                        variable=self.check_var,
                                        font=ctk.CTkFont(size=14),
                                        text_color="#212529")
        self.checkbox.pack(pady=15, padx=15, anchor="w")
        
        # ================== BOTONES DE ACCIÓN ==================
        acciones_frame = ctk.CTkFrame(main_container, fg_color="#e9ecef", corner_radius=10)
        acciones_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(acciones_frame, text="ACCIONES",
                     font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#212529").pack(pady=(10, 5), padx=15)
        
        # Botón Generar Factura y Entregar
        ctk.CTkButton(acciones_frame, 
                      text="[ GENERAR FACTURA Y ENTREGAR ]",
                      width=400, height=45,
                      fg_color="#28a745", hover_color="#218838",
                      font=ctk.CTkFont(size=14, weight="bold"),
                      command=self.generar_factura_entregar).pack(pady=8, padx=15)
        
        # Botón Solo Recibir Pago
        ctk.CTkButton(acciones_frame,
                      text="[ Solo recibir pago (facturar después) ]",
                      width=400, height=40,
                      fg_color="#17a2b8", hover_color="#138496",
                      font=ctk.CTkFont(size=13),
                      command=self.solo_recibir_pago).pack(pady=8, padx=15)
        
        # Botón Volver sin Entregar
        ctk.CTkButton(acciones_frame,
                      text="[ Volver sin entregar ]",
                      width=400, height=40,
                      fg_color="#6c757d", hover_color="#5a6268",
                      font=ctk.CTkFont(size=13),
                      command=self.volver_sin_entregar).pack(pady=8, padx=15)
        
        # ================== INFO AL ENTREGAR ==================
        self.info_entrega = ctk.CTkFrame(main_container, fg_color="#d0d3d6", corner_radius=10)
        
        ctk.CTkLabel(self.info_entrega, text="Al entregar:",
                     font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#212529").pack(pady=(10, 5), padx=15, anchor="w")
        
        info_texts = [
            "→ Pedido pasa a 'ENTREGADO'",
            "→ Se descuenta del inventario",
            "→ Se genera e imprime factura automáticamente"
        ]
        
        for text in info_texts:
            ctk.CTkLabel(self.info_entrega, text=text,
                         font=ctk.CTkFont(size=13),
                         text_color="#212529").pack(pady=2, padx=15, anchor="w")
        
        self.info_entrega.pack(fill="x", pady=(0, 15))
        
        # ================== BOTÓN CERRAR ==================
        ctk.CTkButton(main_container, text="[ Cerrar ]",
                      width=200, height=40,
                      fg_color="#6c757d", hover_color="#5a6268",
                      font=ctk.CTkFont(size=14),
                      command=self.cerrar).pack(pady=(0, 10))
    
    # ================== MÉTODOS DE LÓGICA ==================
    
    def buscar_pedido(self):
        """Busca un pedido por ID y carga su información."""
        id_pedido = self.entry_id_pedido.get().strip()
        
        if not id_pedido:
            messagebox.showwarning("Advertencia", "Ingrese el ID del pedido.")
            return
        
        try:
            # Buscar información del pedido
            self.cursor.execute("""
                SELECT p.id_pedido, c.nombre_completo, p.abono, p.estado, p.id_factura
                FROM pedido p
                JOIN cliente c ON p.id_cliente = c.id_cliente
                WHERE p.id_pedido = %s
            """, (id_pedido,))
            
            resultado = self.cursor.fetchone()
            
            if not resultado:
                messagebox.showerror("Error", f"No se encontró el pedido #{id_pedido}")
                return
            
            id_ped, nombre_cliente, abono, estado, id_factura = resultado
            
            # Verificar si ya fue entregado
            if estado == "Entregado":
                messagebox.showinfo("Información", 
                                   f"El pedido #{id_pedido} ya fue ENTREGADO anteriormente.")
                return
            
            # Calcular total del pedido
            self.cursor.execute("""
                SELECT SUM(i.cantidad * pt.precio_venta)
                FROM incluye i
                JOIN producto_terminado pt ON i.codigo_prod = pt.codigo_prod
                WHERE i.id_pedido = %s
            """, (id_pedido,))
            
            total_resultado = self.cursor.fetchone()
            total = float(total_resultado[0]) if total_resultado and total_resultado[0] else 0.0
            abono_valor = float(abono) if abono else 0.0
            saldo = total - abono_valor
            
            # Guardar datos del pedido actual
            self.pedido_actual = {
                'id_pedido': id_ped,
                'cliente': nombre_cliente,
                'total': total,
                'abono': abono_valor,
                'saldo': saldo,
                'id_factura': id_factura
            }
            
            # Actualizar interfaz
            self.label_titulo.configure(text=f"ENTREGA DE PEDIDO #{id_pedido}")
            self.label_cliente.configure(text=f"Cliente: {nombre_cliente}")
            self.label_total.configure(text=f"Total pedido: ${total:,.3f}")
            self.label_abono.configure(text=f"Abono: ${abono_valor:,.3f}")
            self.label_saldo.configure(text=f"→ SALDO A COBRAR: ${saldo:,.3f}")
            
            # Pre-llenar el campo de pago con el saldo
            self.entry_pago.delete(0, 'end')
            self.entry_pago.insert(0, f"{saldo:.2f}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al buscar pedido: {e}")
            print(f"Detalle del error: {e}")
    
    def generar_factura_entregar(self):
        """Genera la factura, registra el pago y marca el pedido como entregado."""
        if not self.pedido_actual:
            messagebox.showwarning("Advertencia", "Debe buscar un pedido primero.")
            return
        
        if not self.check_var.get():
            messagebox.showwarning("Advertencia", 
                                  "Debe confirmar que el cliente revisó y aprueba las prendas.")
            return
        
        pago_hoy = self.entry_pago.get().strip()
        
        if not pago_hoy:
            messagebox.showwarning("Advertencia", "Ingrese el monto del pago.")
            return
        
        try:
            pago_valor = float(pago_hoy)
        except ValueError:
            messagebox.showwarning("Advertencia", "El monto del pago debe ser un número válido.")
            return
        
        metodo = self.combo_metodo.get()
        
        # Confirmar acción
        if not messagebox.askyesno("Confirmar Entrega",
                                   f"¿Confirmar ENTREGA del pedido #{self.pedido_actual['id_pedido']}?\n\n"
                                   f"Cliente: {self.pedido_actual['cliente']}\n"
                                   f"Pago recibido: ${pago_valor:,.2f}\n"
                                   f"Método: {metodo}\n\n"
                                   "Esta acción:\n"
                                   "- Marcará el pedido como ENTREGADO\n"
                                   "- Actualizará la factura\n"
                                   "- Descontará del inventario"):
            return
        
        try:
            # Actualizar factura
            self.cursor.execute("""
                UPDATE factura_venta
                SET metodo_de_pago = %s, pago = %s
                WHERE id_factura = %s
            """, (metodo, pago_valor, self.pedido_actual['id_factura']))
            
            # Marcar pedido como entregado
            self.cursor.execute("""
                UPDATE pedido
                SET estado = 'Entregado'
                WHERE id_pedido = %s
            """, (self.pedido_actual['id_pedido'],))
            
            # Descontar del inventario
            self.cursor.execute("""
                SELECT codigo_prod, cantidad
                FROM incluye
                WHERE id_pedido = %s
            """, (self.pedido_actual['id_pedido'],))
            
            productos = self.cursor.fetchall()
            
            for cod_prod, cantidad in productos:
                self.cursor.execute("""
                    UPDATE producto_terminado
                    SET cantidad_existencia = cantidad_existencia - %s
                    WHERE codigo_prod = %s
                """, (cantidad, cod_prod))
            
            self.conn.commit()
            
            messagebox.showinfo("Éxito",
                               f"¡Pedido #{self.pedido_actual['id_pedido']} ENTREGADO!\n\n"
                               f"Factura generada\n"
                               f"Inventario actualizado\n"
                               f"Estado: ENTREGADO")
            
            self.limpiar_formulario()
            
        except Exception as e:
            self.conn.rollback()
            messagebox.showerror("Error", f"Error al entregar pedido: {e}")
            print(f"Detalle del error: {e}")
    
    def solo_recibir_pago(self):
        """Registra un pago parcial sin entregar el pedido."""
        if not self.pedido_actual:
            messagebox.showwarning("Advertencia", "Debe buscar un pedido primero.")
            return
        
        pago_hoy = self.entry_pago.get().strip()
        
        if not pago_hoy:
            messagebox.showwarning("Advertencia", "Ingrese el monto del pago.")
            return
        
        try:
            pago_valor = float(pago_hoy)
        except ValueError:
            messagebox.showwarning("Advertencia", "El monto del pago debe ser un número válido.")
            return
        
        try:
            # Actualizar el abono del pedido
            nuevo_abono = self.pedido_actual['abono'] + pago_valor
            
            self.cursor.execute("""
                UPDATE pedido
                SET abono = %s
                WHERE id_pedido = %s
            """, (nuevo_abono, self.pedido_actual['id_pedido']))
            
            self.conn.commit()
            
            messagebox.showinfo("Pago Registrado",
                               f"Pago de ${pago_valor:,.2f} registrado\n\n"
                               f"Nuevo abono: ${nuevo_abono:,.2f}\n"
                               f"Saldo restante: ${self.pedido_actual['total'] - nuevo_abono:,.2f}")
            
            self.limpiar_formulario()
            
        except Exception as e:
            self.conn.rollback()
            messagebox.showerror("Error", f"Error al registrar pago: {e}")
    
    def volver_sin_entregar(self):
        """Vuelve al menú sin realizar cambios."""
        self.cerrar()
    
    def limpiar_formulario(self):
        """Limpia el formulario."""
        self.entry_id_pedido.delete(0, 'end')
        self.entry_pago.delete(0, 'end')
        self.check_var.set(False)
        self.pedido_actual = None
        
        self.label_titulo.configure(text="ENTREGA DE PEDIDO #----")
        self.label_cliente.configure(text="Cliente: -")
        self.label_total.configure(text="Total pedido: $0.000")
        self.label_abono.configure(text="Abono: $0.000")
        self.label_saldo.configure(text="→ SALDO A COBRAR: $0.000")
    
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
    app = EntregaPedido()
    app.mainloop()