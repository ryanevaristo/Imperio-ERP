# Império ERP

Um sistema ERP (Enterprise Resource Planning) completo desenvolvido em Django para empresas imobiliárias e construtoras. O sistema oferece gestão integrada de clientes, produtos imobiliários, estoque, finanças e usuários com controle de permissões baseado em roles.

## 📋 Descrição

O Império ERP é uma solução robusta para gestão empresarial, especialmente projetada para o setor imobiliário. Permite o gerenciamento multi-empresa, controle de inventário, gestão financeira, cadastro de clientes e produtos imobiliários como lotes, quadras e empreendimentos.

## ✨ Funcionalidades

### 🏢 Gestão de Empresas
- Cadastro e gerenciamento de múltiplas empresas
- Controle de acesso por empresa
- Configurações específicas por empresa

### 👥 Gestão de Usuários
- Sistema de autenticação personalizado
- Controle de permissões baseado em roles
- Perfis de usuário flexíveis

### 🏠 Gestão de Produtos Imobiliários
- Cadastro de empreendimentos
- Controle de quadras e lotes
- Status de disponibilidade
- Upload de imagens

### 📦 Gestão de Estoque
- Controle de produtos e categorias
- Movimentações de entrada/saída/devolução
- Notificações de estoque baixo
- Relatórios de inventário

### 💰 Gestão Financeira
- Contas a receber e a pagar
- Controle de cheques
- Gestão de fornecedores
- Relatórios financeiros
- Controle de caixa

### 👨‍💼 Gestão de Clientes
- Cadastro completo de clientes (PF/PJ)
- Endereços e contatos
- Histórico de interações
- Relatórios em PDF

### 🛒 Vendas
- Sistema de vendas integrado
- Controle de vendas por empresa

## 🛠️ Tecnologias Utilizadas

- **Backend**: Django 5.0.2
- **Banco de Dados**: PostgreSQL
- **Frontend**: HTML5, CSS3, JavaScript
- **Containerização**: Docker & Docker Compose
- **Bibliotecas Python**:
  - django-role-permissions (controle de permissões)
  - openpyxl (manipulação de Excel)
  - pdfkit (geração de PDFs)
  - Pillow (processamento de imagens)
  - pandas (análise de dados)
  - python-dotenv (variáveis de ambiente)

## 📋 Pré-requisitos

- Python 3.8+
- Docker e Docker Compose
- PostgreSQL (via Docker)

## 🚀 Instalação

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/imperio-erp.git
   cd imperio-erp
   ```

2. **Configure as variáveis de ambiente:**
   Crie um arquivo `.env` na raiz do projeto:
   ```env
   POSTGRES_NAME=imperio_db
   POSTGRES_USER=imperio_user
   POSTGRES_PASSWORD=sua_senha_segura
   ```

3. **Execute com Docker:**
   ```bash
   docker-compose up --build
   ```

4. **Acesse a aplicação:**
   - Aplicação: http://localhost:8000
   - pgAdmin: http://localhost:5050 (se configurado)

## ⚙️ Configuração

### Migrações do Banco de Dados
```bash
docker-compose exec web python manage.py migrate
```

### Criar Superusuário
```bash
docker-compose exec web python manage.py createsuperuser
```

### Coletar Arquivos Estáticos
```bash
docker-compose exec web python manage.py collectstatic --noinput
```

## 📖 Uso

1. Acesse o admin do Django em `/admin/` com as credenciais do superusuário
2. Crie uma empresa através do admin
3. Cadastre usuários e atribua roles apropriadas
4. Comece a utilizar os módulos:
   - **Clientes**: Cadastro e gestão de clientes
   - **Produtos**: Gerenciamento de empreendimentos, quadras e lotes
   - **Estoque**: Controle de inventário e movimentações
   - **Financeiro**: Gestão de contas e relatórios
   - **Vendas**: Controle de vendas

## 🏗️ Estrutura do Projeto

```
imperio-erp/
├── imperio/              # Configurações principais do Django
├── core/                 # App principal (empresas)
├── usuarios/             # Gestão de usuários e permissões
├── cliente/              # Gestão de clientes
├── produto/              # Produtos imobiliários
├── estoque/              # Controle de estoque
├── financeiro/           # Gestão financeira
├── vendas/               # Sistema de vendas
├── templates/            # Templates HTML
├── media/                # Arquivos de mídia
├── static/               # Arquivos estáticos
├── docker-compose.yml    # Configuração Docker
├── Dockerfile            # Container da aplicação
├── requirements.txt      # Dependências Python
└── README.md            # Este arquivo
```

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.


**Nota**: Este projeto está em desenvolvimento ativo. Algumas funcionalidades podem estar incompletas ou sujeitas a mudanças.
