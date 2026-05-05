from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_notificacoesgeral'),
    ]

    operations = [
        migrations.AddField(
            model_name='empresa',
            name='plano',
            field=models.CharField(
                choices=[
                    ('obra',          'Obra — R$ 97/mês'),
                    ('loteadora',     'Loteadora — R$ 197/mês'),
                    ('incorporadora', 'Incorporadora — R$ 397/mês'),
                ],
                default='obra',
                help_text='Plano contratado pela empresa',
                max_length=20,
                verbose_name='Plano',
            ),
        ),
    ]
