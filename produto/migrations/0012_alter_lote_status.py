# Generated by Django 5.0.2 on 2024-11-19 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0011_alter_lote_data_aquisicao_alter_lote_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lote',
            name='status',
            field=models.CharField(choices=[('R', 'Reservado'), ('V', 'Vendido'), ('D', 'Disponível')], default=True, max_length=1),
        ),
    ]