from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfilusuario',
            name='tipo_documento',
            field=models.CharField(
                choices=[('run', 'RUN'), ('pasaporte', 'Pasaporte')],
                default='run',
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name='perfilusuario',
            name='rut',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
