# Login.py
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from customtkinter import CTkImage

# import psycopg2
import hashlib
import psycopg2

# ================== CONFIGURACIÓN DE INTERFAZ ==================
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Confecciones Valle - Inicio de Sesión")
        self.geometry("950x600")
        self.resizable(False, False)

        self.selected_role = ctk.StringVar(value="")
        self.configure(fg_color="#f0f0f0")

        # =============================================================
        # ================== CONEXIÓN CON POSTGRESQL ==================
        # =============================================================
        try:
            self.conn = psycopg2.connect(
                host="localhost",           # Servidor pgadmin
                user="postgres",            # Usuario
                password="josue",           # Contraseña
                dbname="ProyectoFinalEntrega2" # Base de datos
            )
            self.cursor = self.conn.cursor()
            print("Conexión a PostgreSQL establecida con éxito.")
            
            
        except psycopg2.Error as e:
            messagebox.showerror("Error de Conexión", 
                                 f"No se pudo conectar a PostgreSQL: {e}")
            self.destroy() # Cierra la aplicación si la conexión falla
            return
        
        
        # ================== INTERFAZ IZQUIERDA (Resumen) ==================
        left_frame = ctk.CTkFrame(self, width=400, height=600, corner_radius=0, fg_color="#e8e8e8")
        left_frame.pack(side="left", fill="y")
        left_frame.pack_propagate(False)

        ctk.CTkLabel(left_frame, text="CONFECCIONES\nVALLE", 
                     font=ctk.CTkFont(size=30, weight="bold"), text_color="#2c3e50").pack(pady=60)

        ctk.CTkLabel(left_frame, text="Usuario").pack(pady=(30,5))
        self.entry_user = ctk.CTkEntry(left_frame, width=300, height=50, placeholder_text="Ingrese su usuario")
        self.entry_user.pack(pady=5)

        ctk.CTkLabel(left_frame, text="Contraseña").pack(pady=(20,5))
        self.entry_pass = ctk.CTkEntry(left_frame, width=300, height=50, show="*", placeholder_text="Contraseña")
        self.entry_pass.pack(pady=5)

        self.label_rol = ctk.CTkLabel(left_frame, text="Rol seleccionado: Ninguno", text_color="gray")
        self.label_rol.pack(pady=10)

        ctk.CTkButton(left_frame, text="INGRESAR", width=300, height=50,
                      font=ctk.CTkFont(size=16, weight="bold"), fg_color="#2c3e50",
                      command=self.verificar_login).pack(pady=20)


        # ================== ROLES (Resumen) ==================
        right_frame = ctk.CTkFrame(self, width=500, height=600, corner_radius=0, fg_color="#f8f9fa")
        right_frame.pack(side="right", fill="both", expand=True)
        right_frame.pack_propagate(False)

        ctk.CTkLabel(right_frame, text="Logo", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=30)
        ctk.CTkLabel(right_frame, text="Seleccione su rol", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=60)

        roles_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        roles_frame.pack(pady=40)

        try:
            vendedor_img = CTkImage(Image.open("Imagenes/campana.png"), size=(80, 80))
            admin_img = CTkImage(Image.open("Imagenes/usuario.png"), size=(80, 80))
        except:
            vendedor_img = admin_img = None


        btn_vendedor = ctk.CTkButton(roles_frame, width=180, height=180, corner_radius=20,
                                     fg_color="#e9ecef", hover_color="#c0c4c8", image=vendedor_img, text="",
                                     command=lambda: self.seleccionar_rol("vendedor"))
        
        btn_vendedor.grid(row=0, column=0, padx=40, pady=20)
        ctk.CTkLabel(btn_vendedor, text="Vendedor", font=ctk.CTkFont(size=16, weight="bold")).place(relx=0.5, rely=0.8, anchor="center")


        btn_admin = ctk.CTkButton(roles_frame, width=180, height=180, corner_radius=20,
                                  fg_color="#e9ecef", hover_color="#c0c4c8", image=admin_img, text="",
                                  command=lambda: self.seleccionar_rol("admin"))
        
        btn_admin.grid(row=0, column=1, padx=40, pady=20)
        ctk.CTkLabel(btn_admin, text="Administrador", font=ctk.CTkFont(size=16, weight="bold")).place(relx=0.5, rely=0.8, anchor="center")


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
        self.cursor.execute("SELECT contraseña, rol FROM usuario WHERE usuario=%s", (usuario,)) 
        resultado = self.cursor.fetchone()


        if resultado:
            hash_guardado, rol_bd = resultado
            # hash_guardado y rol_bd son strings de la BD, no necesitamos .encode()
            if hashlib.sha256(contraseña.encode()).hexdigest() == hash_guardado and rol_bd == rol:
                messagebox.showinfo("Éxito", f"¡Bienvenido, {usuario.upper()}!")
                if rol == "vendedor":
                    
                    self.destroy()
                    from VendedorMenu import MenuVendedor
                    menu = MenuVendedor(rol="Vendedor")
                    menu.mainloop()
                # elif rol == "admin":
                #     self.destroy()
                #     from AdminMenu import MenuAdmin
                #     menu = MenuAdmin(rol="Administrador")
                #     menu.mainloop()
                
                
                # Aquí irán tus menús
            else:
                messagebox.showerror("Error", "Contraseña incorrecta o rol no válido")
        else:
            # USUARIO NO EXISTE → PREGUNTAR SI CREARLO CON LA MISMA CONTRASEÑA
            if messagebox.askyesno("Usuario no encontrado",
                                   f"El usuario '{usuario}' no existe.\n\n"
                                   f"¿Desea crearlo ahora como {rol.upper()} con esta contraseña?"):
                hash_pass = hashlib.sha256(contraseña.encode()).hexdigest()
                try:
                    # INSERTAR EN POSTGRESQL (USANDO %s y COMMIT)
                    self.cursor.execute("INSERT INTO usuario (usuario, contraseña, rol) VALUES (%s, %s, %s)", 
                                        (usuario, hash_pass, rol))
                    self.conn.commit()
                    messagebox.showinfo("¡Usuario creado!", 
                                        f"Usuario '{usuario}' creado como {rol.upper()}\n"
                                        f"¡Ya puedes ingresar!")
                    
                    # Aquí también puedes abrir el menú directamente
                except psycopg2.Error as e:
                    # Si falla (ej. si el usuario ya existe por alguna razón o hay un error de DB)
                    self.conn.rollback() 
                    messagebox.showerror("Error DB", f"Error al crear usuario: {e}")
            else:
                return

# La sección global de conexión al inicio de tu archivo original debe ser eliminada
# o colocada dentro de la clase como en el código corregido.

if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()
