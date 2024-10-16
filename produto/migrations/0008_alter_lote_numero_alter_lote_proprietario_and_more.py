# Generated by Django 5.0.2 on 2024-10-16 05:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0004_alter_cliente_cpf_cnpj'),
        ('produto', '0007_rename_foto_empreendimento_imagem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lote',
            name='numero',
            field=models.IntegerField(auto_created=True),
        ),
        migrations.AlterField(
            model_name='lote',
            name='proprietario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Lotes', to='cliente.cliente'),
        ),
        migrations.AlterField(
            model_name='lote',
            name='status',
            field=models.BooleanField(choices=[('Disponível', 'Disponível'), ('Vendido', 'Vendido'), ('Reservado', 'Reservado')], default=True),
        ),
    ]