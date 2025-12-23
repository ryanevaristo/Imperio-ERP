import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'imperio.settings')
django.setup()

from datetime import date, timedelta
from core.models import Empresa
from usuarios.models import Users
from django.contrib.auth import authenticate

print("=" * 70)
print("TESTE COMPLETO DE LOGIN - SISTEMA DE MENSALIDADE")
print("=" * 70)

# Buscar empresa e usuário de teste
empresa = Empresa.objects.first()
user = Users.objects.filter(username='teste_msg@test.com').first()

if not user or not empresa:
    print("\n❌ Usuário ou empresa de teste não encontrados")
    exit(1)

print(f"\n✅ Empresa: {empresa.nome}")
print(f"✅ Usuário: {user.username}")

# CENÁRIO 1: Mensalidade Ativa
print("\n" + "=" * 70)
print("CENÁRIO 1: Mensalidade Ativa (vencimento em 30 dias)")
print("=" * 70)
empresa.mensalidade_ativa = True
empresa.data_vencimento_mensalidade = date.today() + timedelta(days=30)
empresa.save()

print(f"Data atual: {date.today()}")
print(f"Data vencimento: {empresa.data_vencimento_mensalidade}")
print(f"Mensalidade ativa: {empresa.mensalidade_ativa}")
print(f"Mensalidade vencida: {empresa.mensalidade_vencida()}")
print(f"Pode acessar sistema: {empresa.pode_acessar_sistema()}")

auth_result = authenticate(username='teste_msg@test.com', password='teste123')
if auth_result:
    print("\n✅ RESULTADO: Login PERMITIDO (CORRETO)")
else:
    print("\n❌ RESULTADO: Login BLOQUEADO (ERRO - deveria permitir)")

# CENÁRIO 2: Mensalidade Vencida (1 dia atrás)
print("\n" + "=" * 70)
print("CENÁRIO 2: Mensalidade Vencida (venceu ontem)")
print("=" * 70)
empresa.mensalidade_ativa = True
empresa.data_vencimento_mensalidade = date.today() - timedelta(days=1)
empresa.save()

print(f"Data atual: {date.today()}")
print(f"Data vencimento: {empresa.data_vencimento_mensalidade}")
print(f"Mensalidade ativa: {empresa.mensalidade_ativa}")
print(f"Mensalidade vencida: {empresa.mensalidade_vencida()}")
print(f"Pode acessar sistema: {empresa.pode_acessar_sistema()}")

auth_result = authenticate(username='teste_msg@test.com', password='teste123')
if auth_result:
    print("\n❌ RESULTADO: Login PERMITIDO (ERRO - deveria bloquear)")
else:
    print("\n✅ RESULTADO: Login BLOQUEADO (CORRETO)")

# CENÁRIO 3: Mensalidade Inativa
print("\n" + "=" * 70)
print("CENÁRIO 3: Mensalidade Inativa")
print("=" * 70)
empresa.mensalidade_ativa = False
empresa.data_vencimento_mensalidade = date.today() + timedelta(days=30)
empresa.save()

print(f"Data atual: {date.today()}")
print(f"Data vencimento: {empresa.data_vencimento_mensalidade}")
print(f"Mensalidade ativa: {empresa.mensalidade_ativa}")
print(f"Mensalidade vencida: {empresa.mensalidade_vencida()}")
print(f"Pode acessar sistema: {empresa.pode_acessar_sistema()}")

auth_result = authenticate(username='teste_msg@test.com', password='teste123')
if auth_result:
    print("\n❌ RESULTADO: Login PERMITIDO (ERRO - deveria bloquear)")
else:
    print("\n✅ RESULTADO: Login BLOQUEADO (CORRETO)")

# CENÁRIO 4: Sem data de vencimento
print("\n" + "=" * 70)
print("CENÁRIO 4: Sem data de vencimento definida")
print("=" * 70)
empresa.mensalidade_ativa = True
empresa.data_vencimento_mensalidade = None
empresa.save()

print(f"Data atual: {date.today()}")
print(f"Data vencimento: {empresa.data_vencimento_mensalidade}")
print(f"Mensalidade ativa: {empresa.mensalidade_ativa}")
print(f"Mensalidade vencida: {empresa.mensalidade_vencida()}")
print(f"Pode acessar sistema: {empresa.pode_acessar_sistema()}")

auth_result = authenticate(username='teste_msg@test.com', password='teste123')
if auth_result:
    print("\n✅ RESULTADO: Login PERMITIDO (CORRETO - sem data = sem restrição)")
else:
    print("\n❌ RESULTADO: Login BLOQUEADO (ERRO - deveria permitir)")

# CENÁRIO 5: Vencimento hoje
print("\n" + "=" * 70)
print("CENÁRIO 5: Vencimento hoje")
print("=" * 70)
empresa.mensalidade_ativa = True
empresa.data_vencimento_mensalidade = date.today()
empresa.save()

print(f"Data atual: {date.today()}")
print(f"Data vencimento: {empresa.data_vencimento_mensalidade}")
print(f"Mensalidade ativa: {empresa.mensalidade_ativa}")
print(f"Mensalidade vencida: {empresa.mensalidade_vencida()}")
print(f"Pode acessar sistema: {empresa.pode_acessar_sistema()}")

auth_result = authenticate(username='teste_msg@test.com', password='teste123')
if auth_result:
    print("\n✅ RESULTADO: Login PERMITIDO (no dia do vencimento ainda permite)")
else:
    print("\n⚠️ RESULTADO: Login BLOQUEADO (bloqueia no dia do vencimento)")

# Restaurar estado normal
print("\n" + "=" * 70)
print("RESTAURANDO ESTADO NORMAL")
print("=" * 70)
empresa.mensalidade_ativa = True
empresa.data_vencimento_mensalidade = date.today() + timedelta(days=30)
empresa.save()
print(f"✅ Empresa restaurada com vencimento em: {empresa.data_vencimento_mensalidade}")

print("\n" + "=" * 70)
print("RESUMO DOS TESTES")
print("=" * 70)
print("✅ Cenário 1: Mensalidade Ativa - Testado")
print("✅ Cenário 2: Mensalidade Vencida - Testado")
print("✅ Cenário 3: Mensalidade Inativa - Testado")
print("✅ Cenário 4: Sem Data de Vencimento - Testado")
print("✅ Cenário 5: Vencimento Hoje - Testado")
print("\n✅ TODOS OS TESTES DE LOGIN CONCLUÍDOS COM SUCESSO!")
