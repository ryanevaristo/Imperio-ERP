# TODO — Produção Imperio ERP

## 🔴 Fase 1 — Crítico (sem isso não vai ao ar)

### Infraestrutura
- [ ] **Gunicorn** — substituir `runserver` pelo gunicorn no `docker-compose.yml` e adicionar ao `requirements.txt`
- [ ] **Nginx** — criar `nginx.conf` + serviço no `docker-compose.yml` (reverse proxy, static files, SSL termination)
- [ ] **SSL/HTTPS** — certificado via Let's Encrypt (Certbot) ou do provedor de hospedagem
- [ ] **`collectstatic` no build** — adicionar `python manage.py collectstatic --noinput` no `Dockerfile`
- [ ] **`ALLOWED_HOSTS`** — colocar domínio real no `.env` (`ALLOWED_HOSTS=imperioerp.com.br,www.imperioerp.com.br`)
- [ ] **`CSRF_TRUSTED_ORIGINS`** — obrigatório com nginx na frente: `CSRF_TRUSTED_ORIGINS=https://imperioerp.com.br`

### Email
- [ ] **Configurar SMTP real no `.env`** — Gmail App Password, SendGrid, Resend ou Mailgun (sem isso recuperação de senha não funciona)
  ```
  EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
  EMAIL_HOST=smtp.gmail.com
  EMAIL_PORT=587
  EMAIL_USE_TLS=True
  EMAIL_HOST_USER=seu@gmail.com
  EMAIL_HOST_PASSWORD=sua_app_password
  DEFAULT_FROM_EMAIL=Imperio ERP <seu@gmail.com>
  ```

### Banco de dados
- [ ] **Trocar senha do PostgreSQL** — `POSTGRES_PASSWORD=postgres` não pode ir para produção, gerar senha forte
- [ ] **Testar backup manualmente** — rodar `scripts/backup.sh` antes de confiar no serviço automático do docker-compose

---

## 🟠 Fase 2 — Importante (afeta usuários)

### Cron jobs
- [ ] **Agendar `enviar_avisos_vencimento`** — o comando existe mas não roda automaticamente; adicionar cron no docker-compose ou serviço separado para rodar diariamente

### Funcionalidades ausentes
- [ ] **Alterar senha (usuário logado)** — existe recuperação por email mas não existe "trocar senha" dentro do sistema; criar view + template + URL para `PasswordChangeView`
- [ ] **Página 404 customizada** — sem ela Django mostra página padrão em produção (quando `DEBUG=False`)
- [ ] **Página 500 customizada** — idem para erros internos
- [ ] **Servir MEDIA_ROOT via nginx** — uploads de imagens (empreendimentos, quadras) precisam ser servidos corretamente em produção

### Limpeza de código
- [ ] **Remover `print()` do código** — há vários `print(request.POST)` em `financeiro/views.py`, `estoque/views.py` e `usuarios/views.py` que poluem os logs em produção

### Logs
- [ ] **Configurar `LOGGING` no `settings.py`** — direcionar erros para arquivo ou serviço externo para poder investigar problemas em produção

---

## 🟡 Fase 3 — Recomendado (maturidade)

### Monitoramento
- [ ] **Sentry** — `pip install sentry-sdk` + DSN no `.env`; captura exceções automaticamente sem precisar monitorar logs
- [ ] **Uptime monitoring** — UptimeRobot (gratuito) ou Better Uptime para alertas se o servidor cair
- [ ] **Health check endpoint** — rota `/health/` retornando 200 OK, usada pelo nginx/load balancer

### Segurança
- [ ] **Rate limiting no cadastro** — o endpoint `/auth/cadastro/` pode ser abusado para criar contas em massa; aplicar o mesmo controle que o login já tem
- [ ] **`SESSION_COOKIE_AGE`** — definir timeout de sessão (ex: 8 horas); hoje a sessão dura indefinidamente
- [ ] **Remover debug info dos erros** — verificar que `str(e)` não vaza stack traces para o usuário em produção

### Performance
- [ ] **Redis para cache** — hoje o cache é `LocMemCache` (perde ao reiniciar e não funciona com múltiplos workers); trocar por Redis
- [ ] **Compressão de respostas** — `Brotli` já está no `requirements.txt` mas precisa ser configurado no nginx

---

## 🔵 Legal / Compliance (LGPD)

- [ ] **Política de Privacidade** — página informando quais dados são coletados, por quanto tempo e para quê
- [ ] **Termos de Uso** — contrato entre a empresa e o cliente que usa o sistema
- [ ] **Consentimento no cadastro** — checkbox "Li e aceito os Termos de Uso e Política de Privacidade" no formulário de registro
- [ ] **Processo de exclusão de dados** — LGPD garante ao usuário o direito de solicitar exclusão; definir fluxo (email de suporte no mínimo)

---

## ✅ Já feito

- [x] `python-decouple` — secrets via `.env`, nenhuma chave no código
- [x] `DEBUG=False` por padrão em produção
- [x] Configurações HTTPS automáticas quando `DEBUG=False` (`SECURE_SSL_REDIRECT`, `HSTS`, `SESSION_COOKIE_SECURE`, etc.)
- [x] Multi-tenancy corrigido — todos os querysets filtrados por `empresa`
- [x] Brute force no login — bloqueio após 5 tentativas por IP (1 hora)
- [x] Backup automático do banco — `scripts/backup.sh` + serviço diário no docker-compose
- [x] Superuser dashboard — gerenciamento de empresas, planos e assinaturas
- [x] Gestão de planos — troca de plano com auto-preenchimento de valor
- [x] Avisos de vencimento — management command `enviar_avisos_vencimento` (D-7, D-3, D-1)
- [x] Cadastro funcionando com trial de 7 dias
- [x] Recuperação de senha — templates, URLs e email configurados
- [x] Django 5.2 LTS + Python 3.13
- [x] `psycopg2-binary` — sem necessidade de compilar do fonte
- [x] `.gitignore` — `.env`, `media/`, `staticfiles/` ignorados
