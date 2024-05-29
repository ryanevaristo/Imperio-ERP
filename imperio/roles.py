from rolepermissions.roles import AbstractUserRole

class Administrador(AbstractUserRole):
    available_permissions = {
        "cadastrar_usuario": True,
        "Usuarios": True,
        "editar_usuario": True,
    }

class Vendedor(AbstractUserRole):
    available_permissions = {
        "cadastrar_usuario": False,
        "Usuarios": False,
        "editar_usuario": False,
    }

class Gerente(AbstractUserRole):
        available_permissions = {
        "cadastrar_usuario": True,
        "Usuarios": True,}