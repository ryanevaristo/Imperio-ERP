# Generated by Django 5.0.2 on 2024-10-17 15:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0010_alter_lote_proprietario_alter_lote_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lote',
            name='data_aquisicao',
            field=models.DateField(blank=True, default=datetime.datetime(1900, 1, 1, 0, 0), null=True),
        ),
        migrations.AlterField(
            model_name='lote',
            name='status',
            field=models.CharField(choices=[('D', 'Disponível'), ('V', 'Vendido'), ('R', 'Reservado')], default=True, max_length=1),
        ),
    ]
