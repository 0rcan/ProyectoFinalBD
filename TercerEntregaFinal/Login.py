# Login.py
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from customtkinter import CTkImage
from conexion import obtener_conexion
import os

# import psycopg2
import hashlib  # Permite cifrar contraseñas
import psycopg2 # permite la conexión con PostgreSQL

# ================== CONFIGURACIÓN DE INTERFAZ ==================
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class LoginApp(ctk.CTk):
    def __init__(self):
        
        super().__init__()
        
        # ================== CONFIGURACIÓN DE VENTANA ==================
        self.title("Confecciones Valle - Inicio de Sesión")
        self.geometry("950x600")
        self.resizable(False, False)
        self.selected_role = ctk.StringVar(value="") # Variable para rol seleccionado
        self.configure(fg_color="#f0f0f0")


        # =============================================================
        # ================== CONEXIÓN CON POSTGRESQL ==================
        # =============================================================
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
            messagebox.showerror("Error de Conexión", 
                                 f"No se pudo conectar a PostgreSQL: {e}")
            self.destroy() # Cierra la aplicación si la conexión falla
            return
        
        
        # ================== INTERFAZ IZQUIERDA ==================
        # contenedor izquierdo
        left_frame = ctk.CTkFrame(self, width=400, height=600, fg_color="#e8e8e8")
        left_frame.pack(side="left", fill="y") # posicionamiento
        left_frame.pack_propagate(False) # evitar que el frame salga de la ventana

        # Textos y entradas
        ctk.CTkLabel(left_frame, text="CONFECCIONES\nVALLE", 
                     font=ctk.CTkFont(size=30, weight="bold"), text_color="#2c3e50").pack(pady=60)
        
        # Texto
        ctk.CTkLabel(left_frame, text="Usuario").pack(pady=(30,5))
        # Entrada de usuario
        self.entry_user = ctk.CTkEntry(left_frame, width=300, height=50, placeholder_text="Ingrese su usuario")
        self.entry_user.pack(pady=5)

        # Texto
        ctk.CTkLabel(left_frame, text="Contraseña").pack(pady=(20,5))
        # Entrada de contraseña
        self.entry_pass = ctk.CTkEntry(left_frame, width=300, height=50, show="*", placeholder_text="Contraseña")
        self.entry_pass.pack(pady=5)

        # Label rol seleccionado
        self.label_rol = ctk.CTkLabel(left_frame, text="Rol seleccionado: Ninguno", text_color="gray")
        self.label_rol.pack(pady=10)
        
        # Botón ingresar
        ctk.CTkButton(left_frame, text="INGRESAR", width=300, height=50,
                      font=ctk.CTkFont(size=16, weight="bold"), fg_color="#2c3e50",
                      command=self.verificar_login).pack(pady=20)


        # ================== ROLES ==================
        # Contenedor derecho
        right_frame = ctk.CTkFrame(self, width=500, height=600, corner_radius=0, fg_color="#f8f9fa")
        right_frame.pack(side="right", fill="both", expand=True)
        right_frame.pack_propagate(False)
        
        # Texto    
        ctk.CTkLabel(right_frame, text="Seleccione su rol", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=60)

        # Contenedor de botones de rol
        roles_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        roles_frame.pack(pady=40)
        
        # Imágenes de botones (resolviendo rutas relativas de forma segura)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        img_dir = os.path.join(base_dir, "Imagenes")

        campana_path = os.path.join(img_dir, "campana.png")
        usuario_path = os.path.join(img_dir, "usuario.png")

        vendedor_img = None
        admin_img = None

        try:
            if os.path.exists(campana_path):
                vendedor_img = CTkImage(Image.open(campana_path), size=(80, 80))
            else:
                print(f"Advertencia: No se encontró imagen: {campana_path}")
        except Exception as e:
            print(f"Error cargando imagen de vendedor: {e}")

        try:
            if os.path.exists(usuario_path):
                admin_img = CTkImage(Image.open(usuario_path), size=(80, 80))
            else:
                print(f"Advertencia: No se encontró imagen: {usuario_path}")
        except Exception as e:
            print(f"Error cargando imagen de administrador: {e}")


        # Botones de rol
        # Boton Vendedor
        btn_vendedor = ctk.CTkButton(roles_frame, width=180, height=180, corner_radius=20,
                         fg_color="#e9ecef", hover_color="#c0c4c8", image=vendedor_img if vendedor_img else None, text="",
                                     command=lambda: self.seleccionar_rol("vendedor"))
        # Estilo
        btn_vendedor.grid(row=0, column=0, padx=40, pady=20)
        ctk.CTkLabel(btn_vendedor, text="Vendedor", font=ctk.CTkFont(size=16, weight="bold")).place(relx=0.5, rely=0.8, anchor="center")


        # Boton Administrador
        btn_admin = ctk.CTkButton(roles_frame, width=180, height=180, corner_radius=20,
                      fg_color="#e9ecef", hover_color="#c0c4c8", image=admin_img if admin_img else None, text="",
                                  command=lambda: self.seleccionar_rol("admin"))
        
        # Estilo
        btn_admin.grid(row=0, column=1, padx=40, pady=20)
        ctk.CTkLabel(btn_admin, text="Administrador", font=ctk.CTkFont(size=16, weight="bold")).place(relx=0.5, rely=0.8, anchor="center")


    # ===============================================
    # ================== FUNCIONES ==================
    # ===============================================
    def seleccionar_rol(self, rol):
        self.selected_role.set(rol)
        self.label_rol.configure(text=f"Rol seleccionado: {rol.upper()}", text_color="#2c3e50")
        
    def verificar_login(self):
        usuario = self.entry_user.get().strip()
        contraseña = self.entry_pass.get()
        rol = self.selected_role.get()

        if not usuario or not contraseña or not rol:
            messagebox.showerror("Error", "Complete todos los campos y seleccione su rol")
            return

        # Verificar en la base de datos (USANDO %s)
        # Evita SQL Injection
        self.cursor.execute("SELECT contraseña, rol FROM usuario WHERE usuario=%s", (usuario,)) 
        
        ## Almacena la fila de consulta
        resultado = self.cursor.fetchone()


        if resultado:
            hash_guardado, rol_bd = resultado
            #Si el usuario existe, verificar la contraseña


            # Se verifica si el hash de la contraseña escrita coincide con la de la BD
            # y el rol
            if hashlib.sha256(contraseña.encode()).hexdigest() == hash_guardado and rol_bd == rol:
                messagebox.showinfo("Éxito", f"¡Bienvenido, {usuario.upper()}!")
                
                # Abrir el menú vendedor
                if rol == "vendedor":
                    self.destroy()
                    from VendedorMenu import MenuVendedor
                    menu = MenuVendedor(rol="Vendedor")
                    menu.mainloop()
                    
                # Administrador
                elif rol == "admin":
                    self.destroy()
                    from AdminMenu import AdminMenu
                    menu = AdminMenu()
                    menu.mainloop()
                
    
            else:
                messagebox.showerror("Error", "Contraseña incorrecta o rol no válido")
        else:
            
            # USUARIO NO EXISTE → PREGUNTAR SI CREARLO CON LA MISMA CONTRASEÑA
            if messagebox.askyesno("Usuario no encontrado", f"El usuario '{usuario}' no existe.\n\n"
            f"¿Desea crearlo ahora como {rol.upper()} con esta contraseña?"):
                
                # Cifra la contraseña antes de guardarla
                hash_pass = hashlib.sha256(contraseña.encode()).hexdigest()
                
                try:
                    # INSERTAR EN POSTGRESQL (USANDO %s y COMMIT)
                    self.cursor.execute("INSERT INTO usuario (usuario, contraseña, rol) VALUES (%s, %s, %s)", 
                                        (usuario, hash_pass, rol))
                    
                    # Mensaje de confirmación
                    self.conn.commit()
                    messagebox.showinfo("¡Usuario creado!", 
                                        f"Usuario '{usuario}' creado como {rol.upper()}\n"
                                        f"¡Ya puedes ingresar!")
                    
                except psycopg2.Error as e:
                    # Si falla (ej. si el usuario ya existe por alguna razón o hay un error de DB)
                    self.conn.rollback() 
                    messagebox.showerror("Error DB", f"Error al crear usuario: {e}")
            else:
                return


if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()
