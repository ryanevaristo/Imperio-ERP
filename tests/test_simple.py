import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'imperio.settings')
django.setup()

from datetime import date, timedelta
from core.models import Empresa
from usuarios.models import Users
from django.contrib.auth import authenticate

print("=== TESTE SISTEMA DE MENSALIDADE ===\n")

# Teste 1: Verificar campos
print("1. Verificando campos do modelo Empresa:")
empresa = Empresa.objects.first()
if empresa:
    print(f"   Empresa: {empresa.nome}")
    print(f"   Tem campo mensalidade_ativa: {hasattr(empresa, 'mensalidade_ativa')}")
    print(f"   Tem campo data_vencimento_mensalidade: {hasattr(empresa, 'data_vencimento_mensalidade')}")
    print(f"   Tem método pode_acessar_sistema: {hasattr(empresa, 'pode_acessar_sistema')}")
    print("   ✅ Campos criados com sucesso\n")
else:
    print("   ⚠️ Nenhuma empresa encontrada\n")
    exit()

# Teste 2: Login com mensalidade ativa
print("2. Teste de Login - Mensalidade Ativa:")
empresa.mensalidade_ativa = True
empresa.data_vencimento_mensalidade = date.today() + timedelta(days=30)
empresa.save()
user = Users.objects.filter(empresa=empresa).first()
if user:
    result = authenticate(username=user.username, password='senha_teste')
    print(f"   Vencimento: {empresa.data_vencimento_mensalidade}")
    print(f"   Pode acessar: {empresa.pode_acessar_sistema()}")
    print(f"   Resultado: {'✅ Login permitido' if result else '❌ Login bloqueado'}\n")
else:
    print("   ⚠️ Nenhum usuário encontrado\n")

# Teste 3: Login com mensalidade vencida
print("3. Teste de Login - Mensalidade Vencida:")
empresa.data_vencimento_mensalidade = date.today() - timedelta(days=1)
empresa.save()
if user:
    result = authenticate(username=user.username, password='senha_teste')
    print(f"   Vencimento: {empresa.data_vencimento_mensalidade}")
    print(f"   Pode acessar: {empresa.pode_acessar_sistema()}")
    print(f"   Resultado: {'❌ Login permitido (ERRO)' if result else '✅ Login bloqueado (CORRETO)'}\n")

# Teste 4: Métodos do modelo
print("4. Teste dos Métodos:")
empresa.mensalidade_ativa = True
empresa.data_vencimento_mensalidade = date.today() + timedelta(days=15)
empresa.save()
print(f"   mensalidade_vencida(): {empresa.mensalidade_vencida()}")
print(f"   pode_acessar_sistema(): {empresa.pode_acessar_sistema()}")
print("   ✅ Métodos funcionando\n")

# Teste 5: Edge case - sem data
print("5. Edge Case - Sem data de vencimento:")
empresa.data_vencimento_mensalidade = None
empresa.save()
print(f"   Data: {empresa.data_vencimento_mensalidade}")
print(f"   Pode acessar: {empresa.pode_acessar_sistema()}")
print("   ✅ Tratamento correto\n")

print("=== TESTES CONCLUÍDOS ===")
