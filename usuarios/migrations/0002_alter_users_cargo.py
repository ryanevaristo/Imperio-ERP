# Generated by Django 5.0.2 on 2024-05-21 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='cargo',
            field=models.CharField(choices=[('A', 'Administrador'), ('U', 'Usuario'), ('V', 'vendedor')], default='A', max_length=1),
        ),
    ]
