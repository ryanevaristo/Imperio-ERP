-- Script SQL para migrar dados existentes para empresa padrão
-- Execute este script diretamente no banco PostgreSQL

-- Primeiro, criar empresa padrão se não existir
INSERT INTO core_empresa (id, nome, cnpj, endereco, telefone, email, created_at)
VALUES (
    '550e8400-e29b-41d4-a716-446655440000'::uuid,
    'Império',
    NULL,
    NULL,
    NULL,
    NULL,
    NOW()
)
ON CONFLICT (nome) DO NOTHING;

-- Atualizar todos os modelos com empresa NULL para a empresa padrão
-- Estoque
UPDATE estoque_produtos SET empresa_id = '550e8400-e29b-41d4-a716-446655440000' WHERE empresa_id IS NULL;
UPDATE estoque_estoquecategoria SET empresa_id = '550e8400-e29b-41d4-a716-446655440000' WHERE empresa_id IS NULL;
UPDATE estoque_movimentacao SET empresa_id = '550e8400-e29b-41d4-a716-446655440000' WHERE empresa_id IS NULL;
UPDATE estoque_movimentacaoitem SET empresa_id = '550e8400-e29b-41d4-a716-446655440000' WHERE empresa_id IS NULL;
UPDATE estoque_notificacao SET empresa_id = '550e8400-e29b-41d4-a716-446655440000' WHERE empresa_id IS NULL;

-- Financeiro
UPDATE financeiro_contapagar SET empresa_id = '550e8400-e29b-41d4-a716-446655440000' WHERE empresa_id IS NULL;
UPDATE financeiro_despesascategoria SET empresa_id = '550e8400-e29b-41d4-a716-446655440000' WHERE empresa_id IS NULL;
UPDATE financeiro_contareceber SET empresa_id = '550e8400-e29b-41d4-a716-446655440000' WHERE empresa_id IS NULL;
UPDATE financeiro_cheque SET empresa_id = '550e8400-e29b-41d4-a716-446655440000' WHERE empresa_id IS NULL;
UPDATE financeiro_fornecedor SET empresa_id = '550e8400-e29b-41d4-a716-446655440000' WHERE empresa_id IS NULL;

-- Produto
UPDATE produto_empreendimento SET empresa_id = '550e8400-e29b-41d4-a716-446655440000' WHERE empresa_id IS NULL;
UPDATE produto_quadra SET empresa_id = '550e8400-e29b-41d4-a716-446655440000' WHERE empresa_id IS NULL;
UPDATE produto_lote SET empresa_id = '550e8400-e29b-41d4-a716-446655440000' WHERE empresa_id IS NULL;

-- Vendas
UPDATE vendas_vendas SET empresa_id = '550e8400-e29b-41d4-a716-446655440000' WHERE empresa_id IS NULL;
UPDATE vendas_pagamento SET empresa_id = '550e8400-e29b-41d4-a716-446655440000' WHERE empresa_id IS NULL;

-- Cliente
UPDATE cliente_cliente SET empresa_id = '550e8400-e29b-41d4-a716-446655440000' WHERE empresa_id IS NULL;

-- Usuarios
UPDATE usuarios_users SET empresa_id = '550e8400-e29b-41d4-a716-446655440000' WHERE empresa_id IS NULL;

-- Verificar se a migração foi bem-sucedida
SELECT 'Empresa Padrão criada/verificada' as status;

-- Contar registros atualizados por tabela
SELECT
    'estoque_produtos' as tabela,
    COUNT(*) as total_registros,
    SUM(CASE WHEN empresa_id = '550e8400-e29b-41d4-a716-446655440000' THEN 1 ELSE 0 END) as com_empresa_padrao
FROM estoque_produtos
UNION ALL
SELECT
    'estoque_estoquecategoria' as tabela,
    COUNT(*) as total_registros,
    SUM(CASE WHEN empresa_id = '550e8400-e29b-41d4-a716-446655440000' THEN 1 ELSE 0 END) as com_empresa_padrao
FROM estoque_estoquecategoria
UNION ALL
SELECT
    'cliente_cliente' as tabela,
    COUNT(*) as total_registros,
    SUM(CASE WHEN empresa_id = '550e8400-e29b-41d4-a716-446655440000' THEN 1 ELSE 0 END) as com_empresa_padrao
FROM cliente_cliente
UNION ALL
SELECT
    'usuarios_users' as tabela,
    COUNT(*) as total_registros,
    SUM(CASE WHEN empresa_id = '550e8400-e29b-41d4-a716-446655440000' THEN 1 ELSE 0 END) as com_empresa_padrao
FROM usuarios_users;
