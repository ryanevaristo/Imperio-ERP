# Generated by Django 5.0.2 on 2025-07-10 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0010_alter_movimentacao_tipo_notificacao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produtos',
            name='custo',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True),
        ),
    ]
