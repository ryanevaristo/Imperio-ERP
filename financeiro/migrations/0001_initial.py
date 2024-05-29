# Generated by Django 5.0.2 on 2024-05-21 17:05

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cliente', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContaPagar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=100)),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10)),
                ('data_vencimento', models.DateField(blank=True, default=datetime.datetime(1900, 1, 1, 0, 0), null=True)),
                ('data_pagamento', models.DateField(blank=True, default=datetime.datetime(1900, 1, 1, 0, 0), null=True)),
                ('forma_pagamento', models.CharField(blank=True, choices=[('D', 'Dinheiro'), ('B', 'Boleto'), ('T', 'Banco'), ('C', 'Cheque'), ('P', 'PIX')], default='D', max_length=1, null=True)),
                ('pago', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Fornecedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('cnpj', models.CharField(max_length=20)),
                ('telefone', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=100)),
                ('endereco', models.CharField(max_length=100)),
                ('cidade', models.CharField(max_length=100)),
                ('estado', models.CharField(max_length=2)),
                ('cep', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Cheque',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(blank=True, max_length=20, null=True, unique=True)),
                ('nome_repassador', models.CharField(blank=True, max_length=100, null=True)),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10)),
                ('banco', models.CharField(blank=True, choices=[('001', 'Banco do Brasil'), ('104', 'Caixa Econômica Federal'), ('237', 'Bradesco'), ('341', 'Itaú'), ('356', 'Santander'), ('033', 'Banco Santander (Brasil)'), ('745', 'Citibank'), ('399', 'HSBC'), ('422', 'Safra'), ('389', 'Mercantil do Brasil'), ('633', 'Rendimento'), ('652', 'Itaú Unibanco Holding'), ('745', 'Banco Citibank'), ('748', 'Sicredi'), ('756', 'Sicoob')], default='001', max_length=3, null=True)),
                ('data_compensacao', models.DateField(blank=True, default=datetime.datetime(1900, 1, 1, 0, 0), null=True)),
                ('situacao', models.CharField(blank=True, choices=[('E', 'Emitido'), ('C', 'Compensado'), ("G", 'Vencido'), ('S', 'Sem Fundo'), ('D', 'Devolvido'), ('R', 'Repassado')], default='E', max_length=1, null=True)),
                ('nome_titular', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cliente.cliente')),
            ],
        ),
        migrations.CreateModel(
            name='ContaReceber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.TextField(blank=True, null=True)),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10)),
                ('data_vencimento', models.DateField(blank=True, default=datetime.datetime(1900, 1, 1, 0, 0), null=True)),
                ('data_recebimento', models.DateField(blank=True, default=datetime.datetime(1900, 1, 1, 0, 0), null=True)),
                ('recebido', models.BooleanField(default=False)),
                ('forma_recebimento', models.CharField(blank=True, choices=[('D', 'Dinheiro'), ('E', 'Cartão de Crédito'), ('B', 'Boleto'), ('T', 'Transferência Bancária'), ('C', 'Cheque')], default='D', max_length=1, null=True)),
                ('cliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cliente.cliente')),
            ],
        ),
        migrations.CreateModel(
            name='DespesasCategoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_categoria', models.CharField(max_length=100)),
                ('conta_pagar', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='financeiro.contapagar')),
            ],
        ),
        migrations.AddField(
            model_name='contapagar',
            name='categoria',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='financeiro.despesascategoria'),
        ),
    ]
