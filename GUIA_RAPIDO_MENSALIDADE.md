# 🚀 Guia Rápido - Sistema de Mensalidade

## O que foi implementado?

Um sistema completo de controle de mensalidade que **bloqueia o acesso ao sistema** quando a mensalidade da empresa está vencida.

## ✅ Como funciona?

### 1. Bloqueio Automático
- Quando a data de vencimento passa, o sistema **bloqueia automaticamente** o login
- Usuários já logados são **desconectados automaticamente**
- Uma mensagem clara é exibida com informações de contato do suporte

### 2. Três Camadas de Segurança
1. **Backend de Autenticação**: Verifica antes de permitir login
2. **View de Login**: Validação adicional na view
3. **Middleware**: Monitora sessões ativas e desloga se vencer

## 📋 Como Usar

### Passo 1: Acessar o Admin
```
http://localhost:8000/admin/
```

### Passo 2: Gerenciar Empresas
1. Vá em **Core → Empresas**
2. Clique na empresa que deseja configurar
3. Role até a seção **"Informações de Mensalidade"**

### Passo 3: Configurar Mensalidade
Configure os seguintes campos:

- **✅ Mensalidade Ativa**: 
  - Marque para ativar o controle
  - Desmarque para bloquear acesso imediatamente

- **📅 Data de Vencimento da Mensalidade**:
  - Defina a data de vencimento
  - Formato: DD/MM/AAAA
  - Exemplo: 31/01/2026

- **💰 Valor da Mensalidade** (Opcional):
  - Valor mensal da assinatura
  - Apenas para controle interno

- **📆 Dia do Vencimento** (Opcional):
  - Dia do mês para cobrança (1-31)
  - Apenas para controle interno

### Passo 4: Salvar
Clique em **"Salvar"** para aplicar as configurações

## 🎯 Cenários de Uso

### Cenário 1: Ativar Mensalidade para Nova Empresa
```
✅ Mensalidade Ativa: SIM
📅 Data de Vencimento: 31/01/2026
💰 Valor: R$ 199,00
📆 Dia do Vencimento: 31
```
**Resultado**: Empresa pode acessar até 31/01/2026

### Cenário 2: Bloquear Empresa por Inadimplência
```
✅ Mensalidade Ativa: NÃO
```
**Resultado**: Acesso bloqueado imediatamente

### Cenário 3: Renovar Mensalidade
```
✅ Mensalidade Ativa: SIM
📅 Data de Vencimento: 28/02/2026 (nova data)
```
**Resultado**: Acesso liberado até a nova data

### Cenário 4: Empresa sem Controle de Mensalidade
```
✅ Mensalidade Ativa: SIM
📅 Data de Vencimento: (deixar vazio)
```
**Resultado**: Acesso sempre permitido

## 🔍 Verificar Status

No admin, a lista de empresas mostra o status:
- 🟢 **Ativa** - Mensalidade em dia
- 🔴 **Vencida** - Mensalidade vencida (acesso bloqueado)
- ⚠️ **Inativa** - Mensalidade desativada (acesso bloqueado)

## 💬 Mensagem ao Usuário

Quando bloqueado, o usuário vê:

```
⚠️ Mensalidade Vencida

Sua mensalidade está vencida. 
Entre em contato com o suporte para renovar:

📞 Telefone: (XX) XXXX-XXXX
📧 Email: suporte@exemplo.com
💬 WhatsApp: (XX) XXXXX-XXXX
```

## ⚙️ Personalizar Mensagem de Suporte

Edite o arquivo: `usuarios/templates/login.html`

Procure por:
```html
<p><strong>📞 Telefone:</strong> (XX) XXXX-XXXX</p>
<p><strong>📧 Email:</strong> suporte@exemplo.com</p>
<p><strong>💬 WhatsApp:</strong> (XX) XXXXX-XXXX</p>
```

Substitua pelos seus dados de contato.

## 🧪 Testar o Sistema

### Teste 1: Bloquear Acesso
1. Configure data de vencimento para **ontem**
2. Tente fazer login
3. ✅ Deve ser bloqueado com mensagem

### Teste 2: Liberar Acesso
1. Configure data de vencimento para **daqui 30 dias**
2. Faça login
3. ✅ Deve permitir acesso

### Teste 3: Deslogar Usuário Ativo
1. Faça login com mensalidade válida
2. No admin, altere data para **ontem**
3. Navegue para qualquer página
4. ✅ Deve ser deslogado automaticamente

## 📊 Relatórios

### Ver Empresas com Mensalidade Vencida
No admin:
1. Vá em **Core → Empresas**
2. Use o filtro **"Status da Mensalidade"**
3. Selecione **"Vencida"**

### Ver Empresas Ativas
1. Use o filtro **"Mensalidade Ativa"**
2. Selecione **"Sim"**

## ❓ Perguntas Frequentes

### P: O que acontece no dia do vencimento?
**R**: No dia do vencimento, o acesso ainda é permitido. O bloqueio ocorre no dia seguinte.

### P: Posso ter empresas sem controle de mensalidade?
**R**: Sim! Deixe o campo "Data de Vencimento" vazio e marque "Mensalidade Ativa" como SIM.

### P: Como renovar para múltiplas empresas?
**R**: Use a ação em massa no admin:
1. Selecione as empresas
2. Use "Ações" → (criar ação customizada se necessário)

### P: O sistema envia notificações de vencimento?
**R**: Não automaticamente. Você pode implementar um comando Django para enviar emails/SMS.

## 🔧 Manutenção

### Verificar Mensalidades Vencendo
Execute no terminal:
```bash
docker-compose exec web python manage.py shell
```

```python
from core.models import Empresa
from datetime import date, timedelta

# Empresas vencendo nos próximos 7 dias
vencendo = Empresa.objects.filter(
    mensalidade_ativa=True,
    data_vencimento_mensalidade__lte=date.today() + timedelta(days=7),
    data_vencimento_mensalidade__gte=date.today()
)

for empresa in vencendo:
    print(f"{empresa.nome} - Vence em: {empresa.data_vencimento_mensalidade}")
```

## 📞 Suporte

Para dúvidas sobre a implementação, consulte:
- `SISTEMA_MENSALIDADE_README.md` - Documentação técnica completa
- `TODO.md` - Status da implementação

---

**Sistema implementado e testado com sucesso! ✅**
