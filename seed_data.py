"""
Script de ingestão de dados fake para o Império ERP.
Rodar: docker exec <container> python manage.py shell < seed_data.py
"""
import os
import sys
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'imperio.settings')
django.setup()

import random
from decimal import Decimal
from datetime import date, datetime, timedelta
from uuid import uuid4

from core.models import Empresa, NotificacoesGeral
from usuarios.models import Users
from cliente.models import Cliente
from produto.models import Empreendimento, Quadra, Lote
from vendas.models import Vendas, Pagamento
from financeiro.models import ContaPagar, ContaReceber, Cheque, Fornecedor, DespesasCategoria
from estoque.models import Produtos, EstoqueCategoria, Movimentacao, MovimentacaoItem, Notificacao
from rolepermissions.roles import assign_role

print("=" * 60)
print("  INGESTÃO DE DADOS FAKE — IMPÉRIO ERP")
print("=" * 60)

# ─── EMPRESA ───────────────────────────────────────────────
empresa = Empresa.objects.first()
if not empresa:
    empresa = Empresa.objects.create(
        nome='Império Construtora Ltda',
        cnpj='12.345.678/0001-99',
        endereco='Av. Paulista, 1000 - São Paulo/SP',
        telefone='(11) 3456-7890',
        email='contato@imperioconstrutora.com.br',
        data_vencimento_mensalidade=date(2027, 12, 31),
        mensalidade_ativa=True,
        mensalidade_valor=Decimal('299.90'),
        mensalidade_dia_vencimento=15,
    )
else:
    empresa.nome = 'Império Construtora Ltda'
    empresa.cnpj = '12.345.678/0001-99'
    empresa.endereco = 'Av. Paulista, 1000 - São Paulo/SP'
    empresa.telefone = '(11) 3456-7890'
    empresa.email = 'contato@imperioconstrutora.com.br'
    empresa.data_vencimento_mensalidade = date(2027, 12, 31)
    empresa.mensalidade_ativa = True
    empresa.mensalidade_valor = Decimal('299.90')
    empresa.mensalidade_dia_vencimento = 15
    empresa.save()

print(f"[OK] Empresa: {empresa.nome}")

# ─── USUÁRIOS ──────────────────────────────────────────────
users_data = [
    ('admin', 'admin@imperio.com', 'A', 'administrador'),
    ('gerente_maria', 'maria@imperio.com', 'G', 'gerente'),
    ('vendedor_joao', 'joao@imperio.com', 'V', 'vendedor'),
    ('estoquista_carlos', 'carlos@imperio.com', 'E', 'estoquista'),
]

for uname, email, cargo, role in users_data:
    u, created = Users.objects.get_or_create(
        username=uname,
        defaults={
            'email': email,
            'cargo': cargo,
            'empresa': empresa,
            'is_staff': True,
            'is_superuser': uname == 'admin',
        }
    )
    if created:
        u.set_password('admin123')
        u.save()
        assign_role(u, role)
    print(f"  {'[NOVO]' if created else '[JÁ EXISTE]'} Usuário: {uname} ({role})")

print(f"[OK] {Users.objects.filter(empresa=empresa).count()} usuários")

# ─── CLIENTES ──────────────────────────────────────────────
clientes_data = [
    ('Ana Paula Ferreira', '123.456.789-01', 'ana.paula@email.com', '(11) 91234-5678', 'Rua das Flores, 123', 'São Paulo', 'SP', '01001-000'),
    ('Bruno Oliveira Santos', '234.567.890-12', 'bruno.santos@email.com', '(21) 99876-5432', 'Av. Copacabana, 456', 'Rio de Janeiro', 'RJ', '22041-080'),
    ('Carla Mendes Silva', '345.678.901-23', 'carla.mendes@email.com', '(31) 98765-4321', 'Rua da Bahia, 789', 'Belo Horizonte', 'MG', '30160-011'),
    ('Daniel Costa Lima', '456.789.012-34', 'daniel.lima@email.com', '(41) 97654-3210', 'Rua XV de Novembro, 321', 'Curitiba', 'PR', '80020-310'),
    ('Elaine Rodrigues Souza', '567.890.123-45', 'elaine.souza@email.com', '(51) 96543-2109', 'Av. Ipiranga, 654', 'Porto Alegre', 'RS', '90160-093'),
    ('Fernando Almeida Rocha', '678.901.234-56', 'fernando.rocha@email.com', '(61) 95432-1098', 'SQN 308, Bloco B', 'Brasília', 'DF', '70747-020'),
    ('Gabriela Martins Pereira', '789.012.345-67', 'gabi.pereira@email.com', '(71) 94321-0987', 'Rua Chile, 112', 'Salvador', 'BA', '40015-170'),
    ('Henrique Barros Neto', '890.123.456-78', 'henrique.neto@email.com', '(81) 93210-9876', 'Av. Boa Viagem, 888', 'Recife', 'PE', '51011-000'),
    ('Isabela Franco Dias', '901.234.567-89', 'isabela.dias@email.com', '(85) 92109-8765', 'Rua Dragão do Mar, 45', 'Fortaleza', 'CE', '60060-390'),
    ('João Pedro Vieira', '012.345.678-90', 'jp.vieira@email.com', '(62) 91098-7654', 'Av. T-63, 1200', 'Goiânia', 'GO', '74250-020'),
    ('Karen Lopes Araújo', '111.222.333-44', 'karen.araujo@email.com', '(92) 90987-6543', 'Rua Ramos Ferreira, 567', 'Manaus', 'AM', '69010-120'),
    ('Lucas Ribeiro Cunha', '222.333.444-55', 'lucas.cunha@email.com', '(27) 98765-1234', 'Av. Nossa Sra. da Penha, 890', 'Vitória', 'ES', '29055-131'),
    ('Mariana Teixeira Pinto', '333.444.555-66', 'mari.pinto@email.com', '(48) 97654-2345', 'Rua Felipe Schmidt, 234', 'Florianópolis', 'SC', '88010-001'),
    ('Nicolas Gomes Freitas', '444.555.666-77', 'nicolas.freitas@email.com', '(65) 96543-3456', 'Av. do CPA, 1100', 'Cuiabá', 'MT', '78050-970'),
    ('Patricia Campos Ramos', '555.666.777-88', 'patricia.ramos@email.com', '(91) 95432-4567', 'Av. Presidente Vargas, 678', 'Belém', 'PA', '66017-000'),
    ('Ricardo Nascimento', '14.567.890/0001-01', 'ricardo@construtora.com.br', '(11) 3456-0000', 'Av. Industrial, 500', 'Guarulhos', 'SP', '07042-000'),
    ('Construtora ABC Ltda', '23.456.789/0001-02', 'contato@abc.com.br', '(21) 2222-3333', 'Rua do Comércio, 100', 'Niterói', 'RJ', '24020-096'),
    ('Maria Helena Costa', '666.777.888-99', 'mhelena@email.com', '(11) 94567-8901', 'Rua Augusta, 2000', 'São Paulo', 'SP', '01412-100'),
]

clientes_obj = []
for nome, cpf, email, tel, end, cid, est, cep in clientes_data:
    c, created = Cliente.objects.get_or_create(
        cpf_cnpj=cpf,
        defaults={
            'nome_completo': nome, 'email': email, 'telefone': tel,
            'endereco': end, 'cidade': cid, 'estado': est, 'cep': cep,
            'empresa': empresa,
        }
    )
    clientes_obj.append(c)

print(f"[OK] {len(clientes_obj)} clientes")

# ─── EMPREENDIMENTOS / QUADRAS / LOTES ────────────────────
empreend_data = [
    ('Residencial Jardim das Acácias', 'Condomínio fechado com área verde e lazer completo', 'Rod. BR-153, Km 8 — Goiânia/GO'),
    ('Park Imperial I', 'Loteamento premium com infraestrutura completa', 'Av. das Palmeiras, s/n — Aparecida/GO'),
    ('Eco Village Cerrado', 'Loteamento sustentável com preservação ambiental', 'Estrada do Aeroporto, Km 3 — Senador Canedo/GO'),
]

all_lotes = []
for emp_nome, desc, loc in empreend_data:
    emp, _ = Empreendimento.objects.get_or_create(
        nome=emp_nome,
        defaults={'descricao': desc, 'localizacao': loc, 'empresa': empresa}
    )

    for q_num in range(1, 6):  # 5 quadras por empreendimento
        qname = f'Quadra {q_num}'
        quadra, _ = Quadra.objects.get_or_create(
            empreendimento=emp, nome=qname,
            defaults={'metragem': Decimal(str(random.randint(2000, 5000))), 'empresa': empresa}
        )

        for l_num in range(1, 11):  # 10 lotes por quadra
            preco = Decimal(str(random.randint(45000, 180000)))
            lote, created = Lote.objects.get_or_create(
                quadra=quadra, numero=l_num,
                defaults={
                    'metragem': str(random.randint(200, 600)),
                    'preco': preco,
                    'status': 'D',
                    'empresa': empresa,
                }
            )
            if created:
                all_lotes.append(lote)

print(f"[OK] {Empreendimento.objects.filter(empresa=empresa).count()} empreendimentos, "
      f"{Quadra.objects.filter(empresa=empresa).count()} quadras, "
      f"{Lote.objects.filter(empresa=empresa).count()} lotes")

# ─── VENDAS + PAGAMENTOS ──────────────────────────────────
lotes_disponiveis = list(Lote.objects.filter(empresa=empresa, status='D')[:12])
random.shuffle(lotes_disponiveis)

formas_pgto = ['Dinheiro', 'Pix', 'Transferência', 'Boleto', 'Cartão de Crédito']
vendas_criadas = 0

for i, lote in enumerate(lotes_disponiveis[:10]):
    cliente = clientes_obj[i % len(clientes_obj)]
    meses_atras = random.randint(0, 8)
    data_venda = date.today() - timedelta(days=meses_atras * 30 + random.randint(0, 25))
    valor = lote.preco + Decimal(str(random.randint(-5000, 15000)))

    venda = Vendas.objects.create(
        id_lote=lote,
        id_cliente=cliente,
        data_venda=datetime.combine(data_venda, datetime.min.time()),
        valor_venda=valor,
        empresa=empresa,
    )

    lote.status = 'V'
    lote.proprietario = cliente
    lote.save()

    # Parcelas de pagamento (2 a 6 pagamentos)
    num_parcelas = random.randint(2, 6)
    valor_parcela = valor / num_parcelas
    total_pago = Decimal('0')

    for p in range(num_parcelas):
        data_pgto = data_venda + timedelta(days=30 * p + random.randint(0, 5))
        if data_pgto > date.today():
            break
        pgto_valor = round(valor_parcela + Decimal(str(random.uniform(-500, 500))), 2)
        total_pago += pgto_valor

        Pagamento.objects.create(
            id_venda=venda,
            forma_pagamento=random.choice(formas_pgto),
            data_pagamento=data_pgto,
            valor=pgto_valor,
            observacao=f'Parcela {p+1}/{num_parcelas}',
            empresa=empresa,
        )

    if total_pago >= valor:
        venda.quitado = True
        venda.status_venda = 'Concluída'
    venda.save()
    vendas_criadas += 1

# Uma venda cancelada
if lotes_disponiveis and len(lotes_disponiveis) > 10:
    lote_cancel = lotes_disponiveis[10]
    venda_cancel = Vendas.objects.create(
        id_lote=lote_cancel,
        id_cliente=clientes_obj[0],
        valor_venda=lote_cancel.preco,
        status_venda='Cancelada',
        empresa=empresa,
    )
    vendas_criadas += 1

print(f"[OK] {vendas_criadas} vendas com pagamentos parciais")

# ─── CATEGORIAS DE DESPESAS ───────────────────────────────
cat_nomes = [
    'Material de Construção', 'Mão de Obra', 'Combustível', 'Energia Elétrica',
    'Água e Esgoto', 'Telefone e Internet', 'Aluguel', 'Seguros',
    'Impostos e Taxas', 'Marketing e Publicidade', 'Manutenção de Veículos',
    'Material de Escritório', 'Serviços Contábeis', 'Alimentação', 'Frete e Transporte'
]
categorias = []
for nome in cat_nomes:
    cat, _ = DespesasCategoria.objects.get_or_create(
        nome_categoria=nome, empresa=empresa
    )
    categorias.append(cat)

print(f"[OK] {len(categorias)} categorias de despesas")

# ─── CONTAS A PAGAR (DESPESAS) ────────────────────────────
despesas_desc = [
    ('Cimento Portland CP-II 50kg x 200 sacos', 'Material de Construção', 12000),
    ('Tijolos cerâmicos — lote 5.000 un', 'Material de Construção', 8500),
    ('Areia lavada — 30m³', 'Material de Construção', 4200),
    ('Brita nº 1 — 20m³', 'Material de Construção', 3600),
    ('Vergalhões CA-50 — lote', 'Material de Construção', 15800),
    ('Telhas de concreto — 2.000 un', 'Material de Construção', 9400),
    ('Folha pgto — pedreiros Jan', 'Mão de Obra', 28000),
    ('Folha pgto — pedreiros Fev', 'Mão de Obra', 28000),
    ('Folha pgto — pedreiros Mar', 'Mão de Obra', 32000),
    ('Folha pgto — encanadores', 'Mão de Obra', 12000),
    ('Folha pgto — eletricistas', 'Mão de Obra', 14000),
    ('Folha pgto — serventes', 'Mão de Obra', 18000),
    ('Diesel — frota caminhões Jan', 'Combustível', 6800),
    ('Diesel — frota caminhões Fev', 'Combustível', 7200),
    ('Gasolina — veículos administrativos', 'Combustível', 3400),
    ('Fatura ENEL — obra Quadra 1', 'Energia Elétrica', 4500),
    ('Fatura ENEL — obra Quadra 2', 'Energia Elétrica', 3800),
    ('Fatura ENEL — escritório', 'Energia Elétrica', 1200),
    ('SABESP — obras', 'Água e Esgoto', 2800),
    ('Fatura Vivo Empresas', 'Telefone e Internet', 890),
    ('Fatura NET/Claro escritório', 'Telefone e Internet', 450),
    ('Aluguel galpão — Jan', 'Aluguel', 8500),
    ('Aluguel galpão — Fev', 'Aluguel', 8500),
    ('Aluguel galpão — Mar', 'Aluguel', 8500),
    ('Seguro obras — trimestral', 'Seguros', 12000),
    ('Seguro veículos — semestral', 'Seguros', 6500),
    ('IPTU terrenos 2026', 'Impostos e Taxas', 18000),
    ('ISS — competência Jan', 'Impostos e Taxas', 5600),
    ('ISS — competência Fev', 'Impostos e Taxas', 5600),
    ('Campanha Google Ads — Jan', 'Marketing e Publicidade', 3200),
    ('Campanha Google Ads — Fev', 'Marketing e Publicidade', 3800),
    ('Faixas e placas obra', 'Marketing e Publicidade', 2200),
    ('Panfletagem regional', 'Marketing e Publicidade', 1500),
    ('Revisão caminhão Mercedes', 'Manutenção de Veículos', 4200),
    ('Troca pneus retroescavadeira', 'Manutenção de Veículos', 7800),
    ('Papel, toner, clips — escritório', 'Material de Escritório', 680),
    ('Honorários contábeis — Jan', 'Serviços Contábeis', 3500),
    ('Honorários contábeis — Fev', 'Serviços Contábeis', 3500),
    ('Honorários contábeis — Mar', 'Serviços Contábeis', 3500),
    ('Marmitex obra — Jan', 'Alimentação', 4800),
    ('Marmitex obra — Fev', 'Alimentação', 5100),
    ('Frete materiais SP → GO', 'Frete e Transporte', 6200),
    ('Frete vergalhões', 'Frete e Transporte', 3800),
]

formas_desp = ['D', 'B', 'T', 'P', 'C']
for idx, (desc, cat_nome, val_base) in enumerate(despesas_desc):
    cat = next((c for c in categorias if c.nome_categoria == cat_nome), categorias[0])
    meses_atras = idx % 9  # distribui nos últimos 9 meses
    data = date.today().replace(day=1) - timedelta(days=meses_atras * 30) + timedelta(days=random.randint(1, 25))
    if data > date.today():
        data = date.today() - timedelta(days=random.randint(1, 5))
    valor = Decimal(str(val_base)) + Decimal(str(random.randint(-500, 500)))
    pago = random.random() > 0.2  # 80% pagas

    ContaPagar.objects.create(
        descricao=desc,
        valor=valor,
        data_pagamento=data,
        forma_pagamento=random.choice(formas_desp),
        categoria=cat,
        pago=pago,
        empresa=empresa,
    )

print(f"[OK] {len(despesas_desc)} despesas (contas a pagar)")

# ─── CONTAS A RECEBER ─────────────────────────────────────
receber_data = [
    ('Sinal — Lote Quadra 1, Nº 5', 25000),
    ('Parcela 1/12 — contrato 001', 8500),
    ('Parcela 2/12 — contrato 001', 8500),
    ('Parcela 3/12 — contrato 001', 8500),
    ('Parcela 1/6 — contrato 002', 15000),
    ('Parcela 2/6 — contrato 002', 15000),
    ('Parcela 3/6 — contrato 002', 15000),
    ('Pagamento à vista — Lote Quadra 3', 95000),
    ('Taxa de corretagem — venda 003', 6800),
    ('Sinal — reserva Lote 12', 10000),
    ('Parcela 1/24 — contrato 004', 4200),
    ('Parcela 2/24 — contrato 004', 4200),
    ('Parcela 3/24 — contrato 004', 4200),
    ('Parcela 4/24 — contrato 004', 4200),
    ('Aluguel terreno — Jan', 3200),
    ('Aluguel terreno — Fev', 3200),
    ('Aluguel terreno — Mar', 3200),
    ('Multa contratual — desistência', 12000),
    ('Comissão indicação — cliente VIP', 4500),
    ('Diferença de metragem — ajuste contratual', 7800),
]

formas_rec = ['D', 'B', 'T', 'P', 'E']
for idx, (desc, val_base) in enumerate(receber_data):
    cliente = clientes_obj[idx % len(clientes_obj)]
    meses_atras = idx % 7
    data = date.today().replace(day=1) - timedelta(days=meses_atras * 30) + timedelta(days=random.randint(1, 25))
    if data > date.today():
        data = date.today() - timedelta(days=random.randint(1, 5))
    valor = Decimal(str(val_base)) + Decimal(str(random.randint(-300, 800)))
    recebido = random.random() > 0.3  # 70% recebidas

    ContaReceber.objects.create(
        cliente=cliente,
        descricao=desc,
        valor=valor,
        data_recebimento=data,
        recebido=recebido,
        forma_recebimento=random.choice(formas_rec),
        empresa=empresa,
    )

print(f"[OK] {len(receber_data)} contas a receber")

# ─── CHEQUES ──────────────────────────────────────────────
situacoes = ['E', 'C', 'C', 'C', 'G', 'R']  # maioria compensados
bancos = ['001', '104', '237', '341', '356', '748']

for i in range(15):
    num = f'{random.randint(100000, 999999)}'
    while Cheque.objects.filter(numero=num).exists():
        num = f'{random.randint(100000, 999999)}'

    meses_atras = random.randint(0, 6)
    data = date.today() - timedelta(days=meses_atras * 30 + random.randint(0, 25))
    valor = Decimal(str(random.randint(1500, 45000)))

    Cheque.objects.create(
        numero=num,
        nome_titular=random.choice(clientes_obj),
        nome_repassador=random.choice(['', '', 'João Construtor', 'Pedro Materiais', 'Silva & Cia'][:3]) or None,
        valor=valor,
        banco=random.choice(bancos),
        data_compensacao=data,
        situacao=random.choice(situacoes),
        empresa=empresa,
    )

print(f"[OK] 15 cheques")

# ─── FORNECEDORES ─────────────────────────────────────────
fornecedores_data = [
    ('Materiais Goiás Ltda', '11.222.333/0001-44', '(62) 3333-4444', 'vendas@materiaisgoias.com.br', 'Av. Anhanguera, 5000', 'Goiânia', 'GO', '74043-010'),
    ('Ferro & Aço Brasil', '22.333.444/0001-55', '(62) 3555-6666', 'contato@ferroacobrasil.com.br', 'Rod. BR-060, Km 12', 'Aparecida de Goiânia', 'GO', '74970-000'),
    ('Elétrica Nacional', '33.444.555/0001-66', '(62) 3777-8888', 'comercial@eletricanacional.com.br', 'Rua 44, nº 200', 'Goiânia', 'GO', '74023-070'),
    ('Hidráulica Center', '44.555.666/0001-77', '(62) 3999-0000', 'orcamento@hidraulicacenter.com.br', 'Av. Goiás, 3400', 'Goiânia', 'GO', '74063-010'),
    ('Madeireira Cerrado', '55.666.777/0001-88', '(62) 3111-2222', 'pedidos@madeireiracerrado.com.br', 'Setor Industrial, Q. 5', 'Senador Canedo', 'GO', '75250-000'),
    ('Concreto Express', '66.777.888/0001-99', '(62) 3444-5555', 'obras@concretoexpress.com.br', 'Rod. GO-020, Km 8', 'Goiânia', 'GO', '74673-000'),
    ('Tintas Premium', '77.888.999/0001-10', '(11) 4444-5555', 'vendas@tintaspremium.com.br', 'Rua da Indústria, 800', 'Osasco', 'SP', '06230-100'),
    ('Transporte Rápido Log', '88.999.000/0001-21', '(62) 3666-7777', 'frete@rapidolog.com.br', 'Terminal Rodoviário', 'Anápolis', 'GO', '75083-515'),
]

for nome, cnpj, tel, email, end, cid, est, cep in fornecedores_data:
    Fornecedor.objects.get_or_create(
        cnpj=cnpj,
        defaults={
            'nome': nome, 'telefone': tel, 'email': email,
            'endereco': end, 'cidade': cid, 'estado': est, 'cep': cep,
            'empresa': empresa,
        }
    )

print(f"[OK] {len(fornecedores_data)} fornecedores")

# ─── ESTOQUE: CATEGORIAS + PRODUTOS ──────────────────────
est_cats = ['Cimento', 'Areia e Brita', 'Ferragens', 'Elétrica', 'Hidráulica', 'Tintas', 'Madeira', 'EPI', 'Ferramentas']
est_cat_objs = []
for nome in est_cats:
    c, _ = EstoqueCategoria.objects.get_or_create(
        nome_categoria=nome, empresa=empresa
    )
    est_cat_objs.append(c)

produtos_data = [
    ('Cimento CP-II 50kg', 'Cimento', 350, 50, 32.50),
    ('Cimento CP-V 50kg', 'Cimento', 120, 30, 38.00),
    ('Areia lavada m³', 'Areia e Brita', 80, 20, 95.00),
    ('Brita nº 0', 'Areia e Brita', 60, 15, 110.00),
    ('Brita nº 1', 'Areia e Brita', 45, 10, 115.00),
    ('Vergalhão CA-50 8mm (12m)', 'Ferragens', 500, 100, 28.90),
    ('Vergalhão CA-50 10mm (12m)', 'Ferragens', 300, 80, 42.50),
    ('Vergalhão CA-50 12mm (12m)', 'Ferragens', 200, 60, 58.00),
    ('Arame recozido 18 (kg)', 'Ferragens', 150, 30, 12.80),
    ('Prego 17x27 (kg)', 'Ferragens', 80, 20, 14.50),
    ('Fio 2.5mm² (rolo 100m)', 'Elétrica', 40, 10, 185.00),
    ('Fio 4.0mm² (rolo 100m)', 'Elétrica', 25, 8, 295.00),
    ('Disjuntor 20A', 'Elétrica', 60, 15, 18.90),
    ('Tomada 2P+T', 'Elétrica', 200, 50, 8.50),
    ('Tubo PVC 100mm (6m)', 'Hidráulica', 90, 20, 42.00),
    ('Tubo PVC 50mm (6m)', 'Hidráulica', 120, 30, 24.00),
    ('Joelho PVC 100mm', 'Hidráulica', 150, 40, 7.80),
    ('Registro esfera 3/4"', 'Hidráulica', 45, 10, 32.00),
    ('Tinta acrílica 18L branca', 'Tintas', 35, 8, 289.00),
    ('Tinta acrílica 18L gelo', 'Tintas', 20, 5, 289.00),
    ('Selador acrílico 18L', 'Tintas', 25, 8, 145.00),
    ('Massa corrida 25kg', 'Tintas', 40, 10, 58.00),
    ('Tábua pinus 30x300cm', 'Madeira', 100, 20, 35.00),
    ('Sarrafo 5x5cm (3m)', 'Madeira', 200, 50, 12.00),
    ('Pontalete 7x7cm (3m)', 'Madeira', 80, 20, 22.00),
    ('Capacete segurança', 'EPI', 30, 10, 25.00),
    ('Bota de segurança', 'EPI', 25, 8, 85.00),
    ('Luva de proteção (par)', 'EPI', 50, 15, 18.00),
    ('Óculos de proteção', 'EPI', 40, 10, 12.50),
    ('Furadeira impacto', 'Ferramentas', 8, 2, 380.00),
    ('Serra circular 7.1/4"', 'Ferramentas', 5, 2, 520.00),
    ('Betoneira 400L', 'Ferramentas', 3, 1, 2800.00),
]

produto_objs = []
for nome, cat_nome, qtd, qtd_min, custo in produtos_data:
    cat = next((c for c in est_cat_objs if c.nome_categoria == cat_nome), est_cat_objs[0])
    p, _ = Produtos.objects.get_or_create(
        produto=nome,
        empresa=empresa,
        defaults={
            'qtd': qtd,
            'qtd_min': Decimal(str(qtd_min)),
            'custo': Decimal(str(custo)),
            'categoria': cat,
        }
    )
    produto_objs.append(p)

print(f"[OK] {len(produto_objs)} produtos no estoque")

# ─── MOVIMENTAÇÕES DE ESTOQUE ─────────────────────────────
empreendimentos = list(Empreendimento.objects.filter(empresa=empresa))
quadras = list(Quadra.objects.filter(empresa=empresa))

motivos_entrada = [
    'Compra fornecedor — Materiais Goiás',
    'Compra fornecedor — Ferro & Aço Brasil',
    'Reposição de estoque mensal',
    'Transferência entre obras',
    'Compra emergencial',
    'Entrega programada — pedido 2024',
]

motivos_saida = [
    'Uso obra — Quadra 1 alvenaria',
    'Uso obra — Quadra 2 fundação',
    'Uso obra — acabamento lotes',
    'Uso obra — infraestrutura elétrica',
    'Uso obra — rede hidráulica',
    'Manutenção — galpão central',
]

motivos_devolucao = [
    'Material com defeito — troca garantia',
    'Sobra de obra — Quadra 3',
    'Devolução fornecedor — divergência pedido',
]

for i in range(25):
    tipo = random.choices(['Entrada', 'Saida', 'Devolucao'], weights=[45, 45, 10])[0]
    if tipo == 'Entrada':
        motivo = random.choice(motivos_entrada)
    elif tipo == 'Saida':
        motivo = random.choice(motivos_saida)
    else:
        motivo = random.choice(motivos_devolucao)

    emp_rand = random.choice(empreendimentos) if empreendimentos else None
    q_rand = random.choice(quadras) if quadras else None

    mov = Movimentacao.objects.create(
        tipo=tipo,
        motivo=motivo,
        empreendimento=emp_rand,
        quadra=q_rand,
        empresa=empresa,
    )

    # 2 a 5 itens por movimentação
    prods_sample = random.sample(produto_objs, min(random.randint(2, 5), len(produto_objs)))
    for prod in prods_sample:
        qtd = random.randint(5, 50)
        MovimentacaoItem.objects.create(
            movimentacao=mov,
            produto=prod,
            qtd=qtd,
            empresa=empresa,
        )

        # Atualizar estoque
        if tipo == 'Entrada' or tipo == 'Devolucao':
            prod.qtd = (prod.qtd or 0) + qtd
        elif tipo == 'Saida':
            prod.qtd = max(0, (prod.qtd or 0) - qtd)
        prod.save()

print(f"[OK] 25 movimentações de estoque")

# ─── NOTIFICAÇÕES DE ESTOQUE BAIXO ───────────────────────
for prod in produto_objs:
    if prod.qtd is not None and prod.qtd_min is not None and prod.qtd <= int(prod.qtd_min):
        Notificacao.objects.get_or_create(
            produto=prod,
            empresa=empresa,
            visualizado=False,
            defaults={'mensagem': f'Estoque baixo: {prod.produto} — {prod.qtd} un (mín: {int(prod.qtd_min)})'}
        )

notif_count = Notificacao.objects.filter(empresa=empresa, visualizado=False).count()
print(f"[OK] {notif_count} notificações de estoque baixo")

# ─── NOTIFICAÇÕES GERAIS ─────────────────────────────────
notifs_gerais = [
    'Bem-vindo ao Império ERP! Sistema configurado com sucesso.',
    'Novo empreendimento "Eco Village Cerrado" cadastrado.',
    'Venda do lote Q1-05 concluída — cliente Ana Paula Ferreira.',
    'Alerta: 3 cheques vencem esta semana.',
    'Relatório financeiro mensal disponível no módulo Caixa.',
    'Backup automático realizado com sucesso.',
]

for msg in notifs_gerais:
    NotificacoesGeral.objects.get_or_create(
        empresa=empresa,
        mensagem=msg,
        defaults={'visualizado': False}
    )

print(f"[OK] {len(notifs_gerais)} notificações gerais")

# ─── RESUMO FINAL ─────────────────────────────────────────
print()
print("=" * 60)
print("  RESUMO DA INGESTÃO")
print("=" * 60)
print(f"  Empresa:         {empresa.nome}")
print(f"  Usuários:        {Users.objects.filter(empresa=empresa).count()}")
print(f"  Clientes:        {Cliente.objects.filter(empresa=empresa).count()}")
print(f"  Empreendimentos: {Empreendimento.objects.filter(empresa=empresa).count()}")
print(f"  Quadras:         {Quadra.objects.filter(empresa=empresa).count()}")
print(f"  Lotes:           {Lote.objects.filter(empresa=empresa).count()}")
print(f"    - Disponíveis: {Lote.objects.filter(empresa=empresa, status='D').count()}")
print(f"    - Vendidos:    {Lote.objects.filter(empresa=empresa, status='V').count()}")
print(f"  Vendas:          {Vendas.objects.filter(empresa=empresa).count()}")
print(f"  Pagamentos:      {Pagamento.objects.filter(empresa=empresa).count()}")
print(f"  Despesas:        {ContaPagar.objects.filter(empresa=empresa).count()}")
print(f"  Contas Receber:  {ContaReceber.objects.filter(empresa=empresa).count()}")
print(f"  Cheques:         {Cheque.objects.filter(empresa=empresa).count()}")
print(f"  Fornecedores:    {Fornecedor.objects.filter(empresa=empresa).count()}")
print(f"  Produtos:        {Produtos.objects.filter(empresa=empresa).count()}")
print(f"  Movimentações:   {Movimentacao.objects.filter(empresa=empresa).count()}")
print(f"  Notificações:    {notif_count}")
print("=" * 60)
print("  Todos os usuários usam senha: admin123")
print("  admin / gerente_maria / vendedor_joao / estoquista_carlos")
print("=" * 60)
