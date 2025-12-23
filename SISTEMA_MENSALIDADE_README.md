# Sistema de Mensalidade - Imperio ERP

## 📋 Visão Geral

Este sistema implementa controle de mensalidade para empresas no Imperio ERP. Quando a mensalidade de uma empresa vence, todos os usuários associados a ela são impedidos de acessar o sistema até que a mensalidade seja renovada.

## 🔒 Funcionalidades

### 1. Bloqueio Automático no Login
- Usuários de empresas com mensalidade vencida não conseguem fazer login
- Mensagem clara informando sobre o vencimento
- Informações de contato do suporte exibidas automaticamente

### 2. Verificação Durante Sessão Ativa
- Middleware monitora todas as requisições
- Se a mensalidade vencer durante uma sessão ativa, o usuário é deslogado automaticamente
- Redirecionamento para tela de login com mensagem apropriada

### 3. Gerenciamento via Django Admin
- Interface visual para gerenciar mensalidades
- Status em tempo real (✅ Ativa, ❌ Vencida, ⚠️ Inativa)
- Filtros e busca facilitados

## 🗄️ Campos Adicionados ao Modelo Empresa

```python
data_vencimento_mensalidade  # Data de vencimento da mensalidade
mensalidade_ativa            # Flag indicando se está ativa
mensalidade_valor            # Valor mensal (opcional)
mensalidade_dia_vencimento   # Dia do mês para vencimento (opcional)
```

## 🚀 Como Usar

### 1. Aplicar Migração

Primeiro, aplique a migração no banco de dados:

```bash
python manage.py migrate
```

Ou se estiver usando Docker:

```bash
docker-compose exec web python manage.py migrate
```

### 2. Configurar Mensalidade de uma Empresa

#### Via Django Admin:

1. Acesse o Django Admin: `http://localhost:8000/admin/`
2. Vá em **Core > Empresas**
3. Selecione a empresa desejada
4. Na seção **Mensalidade**, configure:
   - **Mensalidade Ativa**: Marque como ativo
   - **Data de Vencimento da Mensalidade**: Defina a data de vencimento
   - **Valor da Mensalidade**: (Opcional) Valor mensal
   - **Dia do Vencimento**: (Opcional) Dia do mês para vencimento
5. Salve as alterações

#### Via Python Shell:

```python
from core.models import Empresa
from datetime import date, timedelta

# Buscar empresa
empresa = Empresa.objects.get(nome="Nome da Empresa")

# Configurar mensalidade
empresa.mensalidade_ativa = True
empresa.data_vencimento_mensalidade = date.today() + timedelta(days=30)
empresa.mensalidade_valor = 199.90
empresa.mensalidade_dia_vencimento = 10
empresa.save()
```

### 3. Testar o Sistema

#### Teste 1: Mensalidade Ativa
```python
# Definir vencimento futuro
empresa.data_vencimento_mensalidade = date.today() + timedelta(days=30)
empresa.mensalidade_ativa = True
empresa.save()

# Resultado: Login permitido normalmente
```

#### Teste 2: Mensalidade Vencida
```python
# Definir vencimento no passado
empresa.data_vencimento_mensalidade = date.today() - timedelta(days=1)
empresa.mensalidade_ativa = True
empresa.save()

# Resultado: Login bloqueado com mensagem de suporte
```

#### Teste 3: Mensalidade Inativa
```python
# Desativar mensalidade
empresa.mensalidade_ativa = False
empresa.save()

# Resultado: Login bloqueado
```

## 🔧 Configuração Adicional

### Personalizar Informações de Suporte

Edite o arquivo `usuarios/templates/login.html` e substitua os placeholders:

```html
📞 Telefone: (11) 1234-5678
📧 Email: suporte@suaempresa.com.br
💬 WhatsApp: (11) 91234-5678
```

### URLs Isentas de Verificação

O middleware não verifica mensalidade nas seguintes URLs:
- `/auth/login/` - Página de login
- `/auth/logout/` - Logout
- `/admin/` - Django Admin
- `/static/` - Arquivos estáticos
- `/media/` - Arquivos de mídia

Para adicionar mais URLs isentas, edite `usuarios/middleware.py`:

```python
EXEMPT_URLS = [
    '/auth/login/',
    '/auth/logout/',
    '/admin/',
    '/static/',
    '/media/',
    '/sua-url-aqui/',  # Adicione aqui
]
```

## 📊 Métodos Úteis

### Verificar Status da Mensalidade

```python
from core.models import Empresa

empresa = Empresa.objects.get(nome="Nome da Empresa")

# Verificar se mensalidade está vencida
if empresa.mensalidade_vencida():
    print("Mensalidade vencida!")

# Verificar se pode acessar o sistema
if empresa.pode_acessar_sistema():
    print("Acesso permitido!")
else:
    print("Acesso bloqueado!")
```

## 🛡️ Segurança

O sistema implementa verificação em múltiplas camadas:

1. **Backend de Autenticação** (`usuarios/backends.py`)
   - Verifica mensalidade durante o processo de autenticação
   - Impede login se mensalidade vencida

2. **View de Login** (`usuarios/views.py`)
   - Validação adicional após autenticação
   - Mensagens de erro específicas

3. **Middleware** (`usuarios/middleware.py`)
   - Monitora todas as requisições
   - Desloga usuários se mensalidade vencer durante sessão

## 🔄 Renovação de Mensalidade

Para renovar a mensalidade de uma empresa:

```python
from core.models import Empresa
from datetime import date, timedelta

empresa = Empresa.objects.get(nome="Nome da Empresa")

# Renovar por 30 dias
empresa.data_vencimento_mensalidade = date.today() + timedelta(days=30)
empresa.mensalidade_ativa = True
empresa.save()

print(f"Mensalidade renovada até: {empresa.data_vencimento_mensalidade}")
```

## 📝 Logs e Monitoramento

Para monitorar tentativas de login bloqueadas, verifique os logs do Django. As mensagens de erro são registradas automaticamente.

## ⚠️ Observações Importantes

1. **Superusuários**: Usuários sem empresa associada (como superusuários) não são afetados pela verificação de mensalidade.

2. **Timezone**: O sistema usa `date.today()` para comparações. Certifique-se de que o timezone está configurado corretamente em `settings.py`.

3. **Migração de Dados Existentes**: Empresas existentes terão `mensalidade_ativa=True` por padrão após a migração. Configure as datas de vencimento conforme necessário.

4. **Performance**: O middleware adiciona uma verificação em cada requisição. Para sistemas com alto tráfego, considere implementar cache.

## 🐛 Troubleshooting

### Problema: Usuários ainda conseguem acessar após vencimento

**Solução**: Verifique se:
1. O middleware está registrado em `settings.py`
2. A migração foi aplicada corretamente
3. O campo `mensalidade_ativa` está como `True`
4. A data de vencimento está no passado

### Problema: Mensagem de suporte não aparece

**Solução**: Limpe o cache do navegador e verifique se o template foi atualizado corretamente.

### Problema: Erro ao aplicar migração

**Solução**: 
```bash
# Verificar migrações pendentes
python manage.py showmigrations

# Aplicar migrações específicas
python manage.py migrate core 0003
```

## 📞 Suporte

Para dúvidas ou problemas com o sistema de mensalidade, entre em contato com a equipe de desenvolvimento.

---

**Versão**: 1.0  
**Data**: 2024  
**Autor**: Imperio ERP Team
