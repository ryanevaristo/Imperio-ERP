
class CargoUsuario:
    ADMINISTRADOR = 'administrador'
    GERENTE = 'gerente'
    VENDEDOR = 'vendedor'
    SUPERVISOR = 'supervisor'
    ESTOQUISTA = 'estoquista'



lista_todas_permissoes = [
    CargoUsuario.ADMINISTRADOR,
    CargoUsuario.GERENTE,
    CargoUsuario.VENDEDOR,
    CargoUsuario.SUPERVISOR,
    CargoUsuario.ESTOQUISTA,
]

lista_permissoes_estoque = [
    CargoUsuario.ADMINISTRADOR,
    CargoUsuario.GERENTE,
    CargoUsuario.ESTOQUISTA,
]

lista_permissoes_vendas = [
    CargoUsuario.ADMINISTRADOR,
    CargoUsuario.GERENTE,
    CargoUsuario.VENDEDOR,
    CargoUsuario.SUPERVISOR,
]

lista_permissoes_produto = [
    CargoUsuario.ADMINISTRADOR,
    CargoUsuario.GERENTE,
    CargoUsuario.SUPERVISOR,
    CargoUsuario.ESTOQUISTA,
    ]

lista_permissoes_financeiro = [
    CargoUsuario.ADMINISTRADOR,
    CargoUsuario.GERENTE,
]