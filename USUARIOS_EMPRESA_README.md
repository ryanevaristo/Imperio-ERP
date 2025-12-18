# Associação de Usuários com Empresas - Django Admin

## Alterações Implementadas

### 1. Formulários (`usuarios/forms.py`)
- ✅ Adicionado campo `empresa` em `UserChangeForm`
- ✅ Adicionado campo `empresa` em `UserCreationForm`

### 2. Admin (`usuarios/admin.py`)
- ✅ Adicionado campo `empresa` nos fieldsets (seção "Informações Adicionais")
- ✅ Adicionado campo `telefone` nos fieldsets
- ✅ Configurado `list_display` para mostrar: username, email, cargo, empresa, is_staff, is_active
- ✅ Configurado `list_filter` para filtrar por: cargo, empresa, is_staff, is_active
- ✅ Configurado `search_fields` para buscar por: username, email, first_name, last_name

## Funcionalidades Disponíveis

### Na Interface Admin do Django:

1. **Criar Usuário com Empresa**
   - Ao criar um novo usuário, você pode selecionar a empresa associada
   - O campo empresa é opcional (null=True, blank=True)

2. **Editar Usuário**
   - Pode alterar a empresa de um usuário existente
   - Pode adicionar/remover a associação com empresa

3. **Listagem de Usuários**
   - Visualize a empresa de cada usuário na lista
   - Filtre usuários por empresa específica
   - Filtre por cargo, status de staff e ativo

4. **Busca**
   - Busque usuários por username, email, nome ou sobrenome

## Como Usar

### Acessar o Admin:
```
http://localhost:8000/admin/usuarios/users/
```

### Criar Usuário com Empresa:
1. Clique em "Adicionar User"
2. Preencha os campos obrigatórios (username, password)
3. Selecione o **Cargo** (Administrador, Vendedor, Gerente, Estoquista)
4. Selecione a **Empresa** no dropdown
5. Opcionalmente, adicione o telefone
6. Salve

### Filtrar Usuários por Empresa:
1. Na lista de usuários, use o painel lateral direito
2. Clique em "Empresa" e selecione a empresa desejada
3. A lista será filtrada automaticamente

## Estrutura do Modelo

```python
class Users(AbstractUser):
    cargo = models.CharField(max_length=1, choices=choice_cargo, default='V')
    telefone = models.CharField(max_length=15, blank=True, null=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True, blank=True)
```

## Observações Importantes

- ⚠️ O campo `empresa` é **opcional** (pode ser null)
- ⚠️ Se uma empresa for deletada, todos os usuários associados também serão deletados (CASCADE)
- ✅ Um usuário pode pertencer a apenas uma empresa
- ✅ Uma empresa pode ter múltiplos usuários

## Próximos Passos Sugeridos

1. **Testar a Funcionalidade**
   - Criar usuários com diferentes empresas
   - Verificar os filtros e buscas
   - Testar a edição de usuários existentes

2. **Considerar Melhorias Futuras**
   - Adicionar validação para garantir que certos cargos tenham empresa obrigatória
   - Implementar permissões baseadas em empresa
   - Criar relatórios por empresa

3. **Migração de Dados (se necessário)**
   - Se você já tem usuários existentes sem empresa, considere criar um script para associá-los

## Exemplo de Uso em Views

```python
# Filtrar usuários por empresa
usuarios_empresa = Users.objects.filter(empresa=empresa_obj)

# Obter empresa do usuário logado
empresa_usuario = request.user.empresa

# Verificar se usuário tem empresa
if request.user.empresa:
    # Fazer algo específico da empresa
    pass
```

## Suporte

Para dúvidas ou problemas, verifique:
- Model: `usuarios/models.py`
- Admin: `usuarios/admin.py`
- Forms: `usuarios/forms.py`
