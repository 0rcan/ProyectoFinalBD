from controller.cliente_controller import ClienteController
from view.cliente_view import GestionClienteView

def main():
    controller = ClienteController()
    view = GestionClienteView(controller)
    controller.set_view(view)
    view.mainloop()

if __name__ == "__main__":
    main()
