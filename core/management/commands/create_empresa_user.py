#!/usr/bin/env python
"""
Comando Django para criar empresas e usuários associados.
Uso: python manage.py create_empresa_user
"""

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from core.models import Empresa
from usuarios.models import Users


class Command(BaseCommand):
    help = 'Cria uma empresa e um usuário administrador associado'

    def add_arguments(self, parser):
        parser.add_argument(
            '--empresa-nome',
            type=str,
            required=True,
            help='Nome da empresa'
        )
        parser.add_argument(
            '--empresa-cnpj',
            type=str,
            default='',
            help='CNPJ da empresa (opcional)'
        )
        parser.add_argument(
            '--empresa-email',
            type=str,
            default='',
            help='Email da empresa (opcional)'
        )
        parser.add_argument(
            '--user-username',
            type=str,
            required=True,
            help='Username do usuário administrador'
        )
        parser.add_argument(
            '--user-email',
            type=str,
            required=True,
            help='Email do usuário'
        )
        parser.add_argument(
            '--user-password',
            type=str,
            required=True,
            help='Senha do usuário'
        )
        parser.add_argument(
            '--user-cargo',
            type=str,
            default='A',
            choices=['A', 'V', 'G', 'E'],
            help='Cargo do usuário: A=Administrador, V=Vendedor, G=Gerente, E=Estoquista'
        )
        parser.add_argument(
            '--user-telefone',
            type=str,
            default='',
            help='Telefone do usuário (opcional)'
        )

    def handle(self, *args, **options):
        try:
            # Criar empresa
            empresa, empresa_created = Empresa.objects.get_or_create(
                nome=options['empresa_nome'],
                defaults={
                    'cnpj': options['empresa_cnpj'],
                    'email': options['empresa_email'],
                }
            )

            if empresa_created:
                self.stdout.write(
                    self.style.SUCCESS(f'Empresa "{empresa.nome}" criada com sucesso!')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Empresa "{empresa.nome}" já existe!')
                )

            # Criar usuário usando o modelo customizado Users
            if Users.objects.filter(user__username=options['user_username']).exists():
                raise CommandError(f'Usuário "{options["user_username"]}" já existe!')

            # Criar usuário usando o manager customizado
            user = Users.objects.create_user(
                username=options['user_username'],
                email=options['user_email'],
                password=options['user_password'],
                cargo=options['user_cargo'],
                telefone=options['user_telefone'],
                empresa=empresa,
                is_staff=True
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f'Usuário "{user.username}" criado com sucesso para a empresa "{empresa.nome}"!'
                )
            )
            self.stdout.write(
                f'  - Cargo: {user.get_cargo_display()}'
            )
            self.stdout.write(
                f'  - Email: {user.email}'
            )
            self.stdout.write(
                f'  - Empresa: {empresa.nome}'
            )

        except Exception as e:
            raise CommandError(f'Erro ao criar empresa/usuário: {str(e)}')
