-- Script SQL para criar gerentes para empresas específicas
-- IDs das empresas: ["15fee538-21f7-4ad1-a253-7f7c9d668c3e", "f7103460-5670-402a-9240-a8147d0c0161", "5b9f0b98-3b6d-4d60-992d-91c7abe2772b", "11812c58-1605-4848-ba2d-3bdb34b51850"]

-- Inserir usuários gerentes no Django (tabela auth_user)
-- Senha padrão: gerente123 (hash do Django para 'gerente123')
-- O hash do Django para 'gerente123' é: pbkdf2_sha256$600000$abc123def456$hash...

INSERT INTO auth_user (password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) VALUES
-- Gerente Empresa 1 (15fee538-21f7-4ad1-a253-7f7c9d668c3e)
('pbkdf2_sha256$600000$abc123def456$hash_placeholder', NULL, 0, 'gerente_empresa_1', 'Gerente', 'Empresa 1', 'gerente1@empresa.com', 1, 1, NOW()),
-- Gerente Empresa 2 (f7103460-5670-402a-9240-a8147d0c0161)
('pbkdf2_sha256$600000$abc123def456$hash_placeholder', NULL, 0, 'gerente_empresa_2', 'Gerente', 'Empresa 2', 'gerente2@empresa.com', 1, 1, NOW()),
-- Gerente Empresa 3 (5b9f0b98-3b6d-4d60-992d-91c7abe2772b)
('pbkdf2_sha256$600000$abc123def456$hash_placeholder', NULL, 0, 'gerente_empresa_3', 'Gerente', 'Empresa 3', 'gerente3@empresa.com', 1, 1, NOW()),
-- Gerente Empresa 4 (11812c58-1605-4848-ba2d-3bdb34b51850)
('pbkdf2_sha256$600000$abc123def456$hash_placeholder', NULL, 0, 'gerente_empresa_4', 'Gerente', 'Empresa 4', 'gerente4@empresa.com', 1, 1, NOW());

-- Inserir perfis de usuário na tabela usuarios_users
INSERT INTO usuarios_users (user_id, cargo, telefone, empresa_id) VALUES
-- Gerente Empresa 1
((SELECT id FROM auth_user WHERE username = 'gerente_empresa_1'), 'G', '(11) 99999-0001', '15fee538-21f7-4ad1-a253-7f7c9d668c3e'),
-- Gerente Empresa 2
((SELECT id FROM auth_user WHERE username = 'gerente_empresa_2'), 'G', '(11) 99999-0002', 'f7103460-5670-402a-9240-a8147d0c0161'),
-- Gerente Empresa 3
((SELECT id FROM auth_user WHERE username = 'gerente_empresa_3'), 'G', '(11) 99999-0003', '5b9f0b98-3b6d-4d60-992d-91c7abe2772b'),
-- Gerente Empresa 4
((SELECT id FROM auth_user WHERE username = 'gerente_empresa_4'), 'G', '(11) 99999-0004', '11812c58-1605-4848-ba2d-3bdb34b51850');

-- Verificar inserções
SELECT
    au.username,
    au.email,
    uu.cargo,
    uu.telefone,
    e.nome as empresa_nome,
    e.id as empresa_id
FROM auth_user au
JOIN usuarios_users uu ON au.id = uu.user_id
JOIN core_empresa e ON uu.empresa_id = e.id
WHERE au.username LIKE 'gerente_empresa_%'
ORDER BY au.username;
