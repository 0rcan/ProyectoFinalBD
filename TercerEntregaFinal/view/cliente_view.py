import customtkinter as ctk

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class GestionClienteView(ctk.CTk):

    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.title("Gestión de Clientes")
        self.geometry("700x600")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._crear_interfaz()

    def _crear_interfaz(self):
        # -------- Frame principal --------
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.main_frame.grid_columnconfigure(0, minsize=320)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)

        # -------- Título --------
        ctk.CTkLabel(
            self.main_frame,
            text="GESTIÓN DE CLIENTES",
            font=ctk.CTkFont(size=20, weight="bold")
        ).grid(row=0, column=0, columnspan=2, pady=(0, 10))

        # -------- Panel izquierdo --------
        self._panel_izquierdo()

        # -------- Panel derecho --------
        self._panel_derecho()

        # -------- Mensaje de estado --------
        self.mensaje_label = ctk.CTkLabel(
            self.main_frame,
            text="",
            fg_color="grey15"
        )
        self.mensaje_label.grid(
            row=2, column=0, columnspan=2, sticky="ew", pady=6
        )

        # -------- Barra inferior --------
        self._barra_inferior()

    # ================= PANEL IZQUIERDO =================
    def _panel_izquierdo(self):
        self.cambio_info_cliente = ctk.CTkFrame(
            self.main_frame, fg_color="grey20", width=340
        )
        self.cambio_info_cliente.grid(
            row=1, column=0, padx=(0, 15), pady=10, sticky="nsw"
        )
        self.cambio_info_cliente.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self.cambio_info_cliente,
            text="NUEVO / EDITAR CLIENTE",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, sticky="w", padx=10, pady=(8, 6))

        # Documento
        ctk.CTkLabel(self.cambio_info_cliente, text="Documento:") \
            .grid(row=1, column=0, sticky="w", padx=10)
        self.doc_entry = ctk.CTkEntry(
            self.cambio_info_cliente, placeholder_text="1032456789"
        )
        self.doc_entry.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 8))

        # Nombre
        ctk.CTkLabel(self.cambio_info_cliente, text="Nombre:") \
            .grid(row=3, column=0, sticky="w", padx=10)
        self.nombre_entry = ctk.CTkEntry(
            self.cambio_info_cliente, placeholder_text="Maria Alejandra López"
        )
        self.nombre_entry.grid(row=4, column=0, sticky="ew", padx=10, pady=(0, 8))

        # Teléfonos
        ctk.CTkLabel(self.cambio_info_cliente, text="Teléfonos:") \
            .grid(row=5, column=0, sticky="w", padx=10)
        self.telefonos_entry = ctk.CTkEntry(
            self.cambio_info_cliente,
            placeholder_text="3159876543, 6012345678"
        )
        self.telefonos_entry.grid(row=6, column=0, sticky="ew", padx=10, pady=(0, 12))

        # Botones
        ctk.CTkButton(
            self.cambio_info_cliente,
            text="Guardar Cliente",
            command=self.controller.guardar_cliente
        ).grid(row=7, column=0, sticky="ew", padx=10)

        ctk.CTkButton(
            self.cambio_info_cliente,
            text="Eliminar Cliente",
            command=self.controller.eliminar_cliente
        ).grid(row=8, column=0, sticky="ew", padx=10, pady=(8, 10))

    # ================= PANEL DERECHO =================
    def _panel_derecho(self):
        self.panel_derecho = ctk.CTkFrame(
            self.main_frame, fg_color="transparent"
        )
        self.panel_derecho.grid(
            row=1, column=1, pady=10, sticky="nsew"
        )
        self.panel_derecho.grid_columnconfigure(0, weight=1)
        self.panel_derecho.grid_rowconfigure(2, weight=1)

        # Búsqueda
        ctk.CTkLabel(
            self.panel_derecho,
            text="BUSCAR CLIENTE",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, sticky="w", padx=10)

        self.busqueda_entry = ctk.CTkEntry(
            self.panel_derecho,
            placeholder_text="Ingrese documento o nombre..."
        )
        self.busqueda_entry.grid(
            row=1, column=0, sticky="ew", padx=10, pady=(6, 12)
        )

        # Lista de clientes
        self.lista_clientes = ctk.CTkTextbox(
            self.panel_derecho, height=280
        )
        self.lista_clientes.grid(
            row=2, column=0, sticky="nsew", padx=10
        )
        self.lista_clientes.configure(state="disabled")

        # Total
        self.total_label = ctk.CTkLabel(
            self.panel_derecho, text="Total clientes: 0"
        )
        self.total_label.grid(row=3, column=0, sticky="w", padx=10)

    # ================= BARRA INFERIOR =================
    def _barra_inferior(self):
        self.bottom_bar = ctk.CTkFrame(
            self.main_frame, fg_color="transparent"
        )
        self.bottom_bar.grid(
            row=3, column=0, columnspan=2, sticky="ew"
        )

        ctk.CTkButton(
            self.bottom_bar,
            text="Cerrar",
            width=100,
            command=self.destroy
        ).grid(row=0, column=0, padx=10, pady=6)

        ctk.CTkLabel(
            self.bottom_bar,
            text="Usuario: vendedor01"
        ).grid(row=0, column=2, padx=10, pady=6)

    # ================= MÉTODOS USADOS POR EL CONTROLLER =================
    def obtener_datos_cliente(self):
        return (
            self.doc_entry.get(),
            self.nombre_entry.get(),
            self.telefonos_entry.get()
        )

    def mostrar_mensaje(self, texto):
        self.mensaje_label.configure(text=texto)

    def mostrar_clientes(self, clientes):
        self.lista_clientes.configure(state="normal")
        self.lista_clientes.delete("1.0", "end")

        for c in clientes:
            self.lista_clientes.insert(
                "end", f"{c[0]} - {c[1]} - {c[2]}\n"
            )

        self.lista_clientes.configure(state="disabled")
        self.total_label.configure(text=f"Total clientes: {len(clientes)}")
