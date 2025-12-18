#!/bin/bash

# Script para criar empresas e usuários de exemplo no sistema Imperio ERP
# Uso: ./create_empresas.sh

echo "🚀 Criando empresas e usuários para o sistema Imperio ERP"
echo "=========================================================="

# Verificar se estamos no diretório correto
if [ ! -f "manage.py" ]; then
    echo "❌ Erro: Execute este script do diretório raiz do projeto Django (onde está o manage.py)"
    exit 1
fi

echo ""
echo "📋 Criando 4 empresas de exemplo..."
echo ""

# Empresa 1: Tech Solutions Ltda
echo "🏢 Criando Tech Solutions Ltda..."
python manage.py create_empresa_user \
    --empresa-nome "Tech Solutions Ltda" \
    --empresa-cnpj "12.345.678/0001-90" \
    --empresa-email "contato@techsolutions.com" \
    --user-username "admin_tech" \
    --user-email "admin@techsolutions.com" \
    --user-password "admin123" \
    --user-cargo "A" \
    --user-telefone "(11) 99999-9999"

echo ""

# Empresa 2: Build Corp S.A.
echo "🏗️  Criando Build Corp S.A...."
python manage.py create_empresa_user \
    --empresa-nome "Build Corp S.A." \
    --empresa-cnpj "98.765.432/0001-10" \
    --empresa-email "contato@buildcorp.com" \
    --user-username "admin_build" \
    --user-email "admin@buildcorp.com" \
    --user-password "admin123" \
    --user-cargo "A" \
    --user-telefone "(21) 88888-8888"

echo ""

# Empresa 3: Mega Construções Ltda
echo "🏗️  Criando Mega Construções Ltda..."
python manage.py create_empresa_user \
    --empresa-nome "Mega Construções Ltda" \
    --empresa-cnpj "45.678.901/0001-23" \
    --empresa-email "contato@megaconstrucoes.com" \
    --user-username "admin_mega" \
    --user-email "admin@megaconstrucoes.com" \
    --user-password "admin123" \
    --user-cargo "A" \
    --user-telefone "(31) 77777-7777"

echo ""

# Empresa 4: Comercial XYZ Ltda
echo "🏪 Criando Comercial XYZ Ltda..."
python manage.py create_empresa_user \
    --empresa-nome "Comercial XYZ Ltda" \
    --empresa-cnpj "78.901.234/0001-56" \
    --empresa-email "contato@comercialxyz.com" \
    --user-username "admin_xyz" \
    --user-email "admin@comercialxyz.com" \
    --user-password "admin123" \
    --user-cargo "A" \
    --user-telefone "(41) 66666-6666"

echo ""
echo "✅ Todas as empresas e usuários foram criados com sucesso!"
echo ""
echo "📊 Resumo das empresas criadas:"
echo "1. Tech Solutions Ltda     - admin_tech / admin123"
echo "2. Build Corp S.A.         - admin_build / admin123"
echo "3. Mega Construções Ltda   - admin_mega / admin123"
echo "4. Comercial XYZ Ltda      - admin_xyz / admin123"
echo ""
echo "🔐 Para testar o isolamento:"
echo "1. Acesse http://localhost:8000/admin/"
echo "2. Faça login com cada usuário acima"
echo "3. Verifique que cada um vê apenas dados da sua empresa"
echo ""
echo "💡 Dica: Crie um superusuário para gerenciar tudo:"
echo "   python manage.py createsuperuser"
echo ""
echo "🎉 Setup concluído! O sistema multi-tenant está pronto para uso."
