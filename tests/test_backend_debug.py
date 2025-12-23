import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'imperio.settings')
django.setup()

from datetime import date, timedelta
from core.models import Empresa
from usuarios.models import Users
from django.contrib.auth import authenticate
from django.conf import settings

print("=" * 70)
print("DEBUG DO BACKEND DE AUTENTICAÇÃO")
print("=" * 70)

print("\n1. Verificando configuração do settings:")
print(f"   AUTHENTICATION_BACKENDS: {settings.AUTHENTICATION_BACKENDS}")

print("\n2. Testando import do backend:")
try:
    from usuarios.backends import MensalidadeBackend
    backend = MensalidadeBackend()
    print("   ✅ Backend importado com sucesso")
    print(f"   Classe: {backend.__class__.__name__}")
except Exception as e:
    print(f"   ❌ Erro ao importar backend: {e}")

print("\n3. Testando autenticação direta com o backend:")
empresa = Empresa.objects.first()
user = Users.objects.filter(username='teste_msg@test.com').first()

if user and empresa:
    # Configurar mensalidade vencida
    empresa.mensalidade_ativa = True
    empresa.data_vencimento_mensalidade = date.today() - timedelta(days=1)
    empresa.save()
    
    print(f"   Usuário: {user.username}")
    print(f"   Empresa: {empresa.nome}")
    print(f"   Vencimento: {empresa.data_vencimento_mensalidade}")
    print(f"   Pode acessar: {empresa.pode_acessar_sistema()}")
    
    # Testar com backend diretamente
    print("\n4. Testando backend diretamente:")
    result = backend.authenticate(None, username='teste_msg@test.com', password='teste123')
    print(f"   Resultado do backend: {result}")
    if result is None:
        print("   ✅ Backend bloqueou corretamente")
    else:
        print("   ❌ Backend permitiu (ERRO)")
    
    # Testar com authenticate()
    print("\n5. Testando com authenticate():")
    result = authenticate(username='teste_msg@test.com', password='teste123')
    print(f"   Resultado do authenticate(): {result}")
    if result is None:
        print("   ✅ authenticate() bloqueou corretamente")
    else:
        print("   ❌ authenticate() permitiu (ERRO)")
        print(f"   Tipo do resultado: {type(result)}")
        print(f"   Backend usado: {result.backend if hasattr(result, 'backend') else 'N/A'}")
