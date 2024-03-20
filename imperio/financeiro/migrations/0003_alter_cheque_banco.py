# Generated by Django 5.0.2 on 2024-03-20 00:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0002_cheque_banco_alter_cheque_data_compensacao_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cheque',
            name='banco',
            field=models.CharField(blank=True, choices=[('001', 'Banco do Brasil'), ('104', 'Caixa Econômica Federal'), ('237', 'Bradesco'), ('341', 'Itaú'), ('356', 'Santander'), ('033', 'Banco Santander (Brasil)'), ('745', 'Citibank'), ('399', 'HSBC'), ('422', 'Safra'), ('389', 'Mercantil do Brasil'), ('633', 'Rendimento'), ('652', 'Itaú Unibanco Holding'), ('745', 'Banco Citibank'), ('748', 'Sicredi'), ('756', 'Sicoob')], default='001', max_length=3, null=True),
        ),
    ]
