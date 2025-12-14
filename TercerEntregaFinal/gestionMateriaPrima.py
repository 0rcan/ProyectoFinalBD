import customtkinter as ctk
import psycopg2
from tkinter import messagebox
from dotenv import load_dotenv
import os

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class GestionMateriaPrima(ctk.CTk):

    def __init__(self):
        super().__init__()
        load_dotenv()

        self.codigo_actual = None  # almacenará el id_materia
        self.materias_cache = []
        self.col_codigo = None
        self.pk_col = None

        self.conectar_bd()
        self.configurar_ventana()

        self.crear_panel_izquierdo()
        self.crear_panel_derecho()
        self.crear_barra_inferior()

        # Detectar columnas de la tabla para evitar errores por nombres
        self.detectar_columnas_tabla()
        self.listar_materias()

    # --------------------------------------------------
    # CONFIGURACIÓN
    # --------------------------------------------------

    def configurar_ventana(self):
        self.title("Gestión de Materias Primas")
        self.geometry("900x600")

        self.main = ctk.CTkFrame(self)
        self.main.pack(fill="both", expand=True, padx=20, pady=20)

    def conectar_bd(self):
        self.conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            dbname=os.getenv("DB_NAME", "ProyectoFinal")
        )

    def detectar_columnas_tabla(self):
        try:
            cur = self.conn.cursor()
            cur.execute("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = 'materia_prima'
                ORDER BY ordinal_position
            """)
            cols = [r[0] for r in cur.fetchall()]
            cur.close()

            # Determinar columna de código (si existe)
            if 'codigo' in cols:
                self.col_codigo = 'codigo'
            # Determinar una columna clave primaria común
            for cand in ['id_materia_prima', 'id_materia', 'id', 'id_mp']:
                if cand in cols:
                    self.pk_col = cand
                    break
            # Si no hay 'codigo' usar la PK como identificador para UI/búsqueda
            if not self.col_codigo and not self.pk_col:
                # fallback: usar primera columna como identificador
                self.pk_col = cols[0] if cols else None
        except Exception:
            # Si falla, dejar valores por defecto y permitir que el error se muestre luego
            self.col_codigo = None
            self.pk_col = None

    # --------------------------------------------------
    # PANEL IZQUIERDO
    # --------------------------------------------------

    def crear_panel_izquierdo(self):
        frame = ctk.CTkFrame(self.main, width=380)
        frame.pack(side="left", fill="y", padx=(0, 15))

        ctk.CTkLabel(
            frame, text="NUEVA / EDITAR MATERIA PRIMA",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=10)

        self.codigo_label = ctk.CTkLabel(frame, text="ID Materia: (automático)")
        self.codigo_label.pack(anchor="w", padx=10)

        ctk.CTkLabel(frame, text="Nombre:").pack(anchor="w", padx=10)
        self.nombre_entry = ctk.CTkEntry(frame, placeholder_text="Nombre")
        self.nombre_entry.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(frame, text="Tipo:").pack(anchor="w", padx=10)
        self.tipo_combo = ctk.CTkComboBox(
            frame,
            values=["Tela", "Hilo", "Botón", "Cierre"]
        )
        self.tipo_combo.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(frame, text="Unidad:").pack(anchor="w", padx=10)
        self.unidad_combo = ctk.CTkComboBox(
            frame,
            values=["Metro", "Unidad", "Kilo", "Rollo"]
        )
        self.unidad_combo.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(frame, text="Cantidad:").pack(anchor="w", padx=10)
        self.cantidad_entry = ctk.CTkEntry(frame, placeholder_text="Cantidad")
        self.cantidad_entry.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(frame, text="Descripción:").pack(anchor="w", padx=10)
        self.descripcion_entry = ctk.CTkEntry(frame, placeholder_text="Descripción")
        self.descripcion_entry.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(
            frame, text="Proveedores que la suministran:"
        ).pack(anchor="w", padx=10, pady=(10, 0))

        self.proveedores_vars = {}
        self.cargar_proveedores(frame)

        ctk.CTkButton(
            frame, text="Guardar Materia",
            command=self.guardar_materia
        ).pack(fill="x", padx=10, pady=8)

        ctk.CTkButton(
            frame, text="Eliminar",
            command=self.eliminar_materia
        ).pack(fill="x", padx=10)

    def cargar_proveedores(self, frame):
        cur = self.conn.cursor()
        cur.execute("SELECT nit, nombre FROM proveedor ORDER BY nombre")
        proveedores = cur.fetchall()
        cur.close()

        for nit, nombre in proveedores:
            var = ctk.BooleanVar()
            chk = ctk.CTkCheckBox(frame, text=nombre, variable=var)
            chk.pack(anchor="w", padx=20)
            self.proveedores_vars[nit] = var

    # --------------------------------------------------
    # PANEL DERECHO
    # --------------------------------------------------

    def crear_panel_derecho(self):
        frame = ctk.CTkFrame(self.main)
        frame.pack(side="right", fill="both", expand=True)

        ctk.CTkLabel(frame, text="BUSCAR", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=10)
        self.buscar_entry = ctk.CTkEntry(frame, placeholder_text="Nombre o ID materia")
        self.buscar_entry.pack(fill="x", padx=10, pady=5)
        self.buscar_entry.bind("<KeyRelease>", lambda e: self.buscar())

        self.lista = ctk.CTkTextbox(frame)
        self.lista.pack(fill="both", expand=True, padx=10)
        self.lista.configure(state="disabled")
        self.lista.bind("<ButtonRelease-1>", self.seleccionar)

        stats_frame = ctk.CTkFrame(frame)
        stats_frame.pack(fill="x", padx=10, pady=(5, 10))
        self.total_label = ctk.CTkLabel(stats_frame, text="Total items: 0")
        self.total_label.pack(side="left")
        self.criticos_label = ctk.CTkLabel(stats_frame, text="Existencia crítica: 0 items")
        self.criticos_label.pack(side="right")

        umbral_frame = ctk.CTkFrame(frame)
        umbral_frame.pack(fill="x", padx=10, pady=(0, 10))
        ctk.CTkLabel(umbral_frame, text="Umbral crítico:").pack(side="left")
        self.umbral_entry = ctk.CTkEntry(umbral_frame, width=80)
        self.umbral_entry.pack(side="left", padx=(5, 10))
        self.umbral_entry.insert(0, "10")
        ctk.CTkButton(umbral_frame, text="Aplicar", width=80, command=self.actualizar_criticos).pack(side="left")

    # --------------------------------------------------
    # FUNCIONES
    # --------------------------------------------------

    def generar_codigo(self, tipo):
        # Ya no se usa 'codigo'; la PK es id_materia autogenerada
        return None

    def guardar_materia(self):
        nombre = self.nombre_entry.get().strip()
        tipo = self.tipo_combo.get()
        unidad = self.unidad_combo.get()
        cantidad = self.cantidad_entry.get().strip()
        descripcion = self.descripcion_entry.get().strip()

        if not nombre or not cantidad:
            messagebox.showwarning("Error", "Campos obligatorios")
            return

        cur = self.conn.cursor()

        try:
            if not self.codigo_actual:
                # Inserción acorde al ERD: id_materia serial, nombre, tipo, descripcion, cantidad, unidad_medida
                # Convertir cantidad a número si es posible
                try:
                    cantidad_num = float(str(cantidad).replace(',', '.'))
                except Exception:
                    cantidad_num = cantidad

                cur.execute(
                    """
                    INSERT INTO materia_prima (nombre, tipo, descripcion, cantidad, unidad_medida)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id_materia
                    """,
                    (nombre, tipo, descripcion, cantidad_num, unidad),
                )
                self.codigo_actual = cur.fetchone()[0]
            else:
                codigo = self.codigo_actual
                # Convertir cantidad a número si es posible
                try:
                    cantidad_num = float(str(cantidad).replace(',', '.'))
                except Exception:
                    cantidad_num = cantidad

                cur.execute(
                    """
                    UPDATE materia_prima
                    SET nombre=%s, tipo=%s, descripcion=%s, cantidad=%s, unidad_medida=%s
                    WHERE id_materia=%s
                    """,
                    (nombre, tipo, descripcion, cantidad_num, unidad, codigo),
                )

                # Actualizar relaciones con proveedores
                cur.execute(
                    "DELETE FROM provee WHERE id_materia=%s",
                    (codigo,),
                )

            for nit, var in self.proveedores_vars.items():
                if var.get():
                    cur.execute(
                        """
                        INSERT INTO provee (id_materia, nit)
                        VALUES (%s, %s)
                        """,
                        (self.codigo_actual, nit),
                    )

            self.conn.commit()
            self.mostrar_mensaje(f"Inventario actualizado - {nombre}")
            self.limpiar()
            self.listar_materias()

        except Exception as e:
            self.conn.rollback()
            messagebox.showerror("Error", str(e))
        finally:
            cur.close()

    def listar_materias(self):
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT id_materia, nombre, cantidad, unidad_medida
            FROM materia_prima ORDER BY nombre
            """
        )
        self.materias_cache = cur.fetchall()
        cur.close()

        self.lista.configure(state="normal")
        self.lista.delete("1.0", "end")

        # Encabezado estilo tabla simple
        self.lista.insert("end", "ID | Nombre | Cantidad\n")
        self.lista.insert("end", "----------------------------------------\n")
        for m in self.materias_cache:
            cant = f"{m[2]} {m[3]}" if m[3] else str(m[2])
            self.lista.insert("end", f"{m[0]} | {m[1]} | {cant}\n")

        self.lista.configure(state="disabled")
        self.total_label.configure(text=f"Total items: {len(self.materias_cache)}")
        self.actualizar_criticos()

    def buscar(self):
        texto = self.buscar_entry.get().lower()

        def to_str(v):
            return str(v).lower() if v is not None else ""
        filtrados = [m for m in self.materias_cache if texto in to_str(m[0]) or texto in to_str(m[1])]

        self.lista.configure(state="normal")
        self.lista.delete("1.0", "end")

        self.lista.insert("end", "ID | Nombre | Cantidad\n")
        self.lista.insert("end", "----------------------------------------\n")
        for m in filtrados:
            cant = f"{m[2]} {m[3]}" if m[3] else str(m[2])
            self.lista.insert("end", f"{m[0]} | {m[1]} | {cant}\n")

        self.lista.configure(state="disabled")

    def seleccionar(self, event):
        try:
            # La tabla tiene 2 líneas de encabezado, los datos inician en la línea 3
            line_clicked = int(self.lista.index(f"@{event.x},{event.y}").split(".")[0])
            index = line_clicked - 3
            if index < 0 or index >= len(self.materias_cache):
                return
            materia = self.materias_cache[index]
            self.codigo_actual = materia[0]

            self.nombre_entry.delete(0, "end")
            self.nombre_entry.insert(0, materia[1])
            self.cantidad_entry.delete(0, "end")
            self.cantidad_entry.insert(0, materia[2])
            # unidad en combo
            try:
                self.unidad_combo.set(materia[3])
            except:
                pass

        except:
            pass

    def eliminar_materia(self):
        if not self.codigo_actual:
            messagebox.showwarning("Error", "Seleccione una materia")
            return

        cur = self.conn.cursor()
        cur.execute("DELETE FROM materia_prima WHERE id_materia=%s", (self.codigo_actual,))
        self.conn.commit()
        cur.close()

        self.limpiar()
        self.listar_materias()

    def limpiar(self):
        self.codigo_actual = None
        self.nombre_entry.delete(0, "end")
        self.cantidad_entry.delete(0, "end")
        self.descripcion_entry.delete(0, "end")
        for var in self.proveedores_vars.values():
            var.set(False)

    def volver(self):
        self.destroy()
        from AdminMenu import AdminMenu
        app = AdminMenu("vendedor01")
        app.mainloop()

    def crear_barra_inferior(self):
        bar = ctk.CTkFrame(self)
        bar.pack(fill="x")

        ctk.CTkButton(bar, text="Volver", width=100, command=self.volver).pack(side="left", padx=10, pady=5)
        self.msg = ctk.CTkLabel(bar, text="")
        self.msg.pack(side="left", padx=10)

    def mostrar_mensaje(self, texto):
        self.msg.configure(text=texto)

    def actualizar_criticos(self):
        try:
            umbral = float(self.umbral_entry.get()) if hasattr(self, 'umbral_entry') else 10.0
        except Exception:
            umbral = 10.0
        def parse_cantidad(v):
            try:
                return float(v)
            except Exception:
                try:
                    return float(str(v).replace(',', '.'))
                except Exception:
                    return 0.0
        criticos = sum(1 for m in self.materias_cache if parse_cantidad(m[2]) <= umbral)
        self.criticos_label.configure(text=f"Existencia crítica: {criticos} items")


if __name__ == "__main__":
    app = GestionMateriaPrima()
    app.mainloop()
