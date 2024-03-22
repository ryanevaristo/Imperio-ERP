from rolepermissions.roles import AbstractUserRole

class Administrador(AbstractUserRole):
    available_permissions = {
        'create_user': True,
        'delete_user': True,
        'edit_user': True,
        'view_user': True,
        'create_product': True,
        'delete_product': True,
        'edit_product': True,
        'view_product': True,
        'create_order': True,
        'delete_order': True,
        'edit_order': True,
        'view_order': True,
    }

class Usuario(AbstractUserRole):
    available_permissions = {
        'create_order': True,
        'delete_order': True,
        'edit_order': True,
        'view_order': True,
    }

class Vendedor(AbstractUserRole):
    available_permissions = {
        'create_order': True,
        'delete_order': True,
        'edit_order': True,
        'view_order': True,
    }