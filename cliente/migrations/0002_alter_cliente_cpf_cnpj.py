# Generated by Django 5.0.2 on 2024-05-21 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='cpf_cnpj',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
