from model.cliente_model import ClienteModel
from tkinter import messagebox

class ClienteController:

    def __init__(self):
        self.view = None

    def set_view(self, view):
        self.view = view

    def guardar_cliente(self):
        documento = self.view.doc_entry.get()
        nombre = self.view.nombre_entry.get()
        telefonos = self.view.telefonos_entry.get()

        if not documento or not nombre:
            messagebox.showwarning(
                "Error", "Documento y nombre son obligatorios"
            )
            return

        ClienteModel.guardar(documento, nombre, telefonos)
        messagebox.showinfo("Éxito", "Cliente guardado correctamente")

    def eliminar_cliente(self):
        documento = self.view.doc_entry.get()

        if not documento:
            messagebox.showwarning(
                "Error", "Ingrese el documento"
            )
            return

        ClienteModel.eliminar(documento)
        messagebox.showinfo("Éxito", "Cliente eliminado")
