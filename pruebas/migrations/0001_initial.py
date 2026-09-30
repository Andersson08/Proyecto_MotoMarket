import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('catalogo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SolicitudPrueba',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(verbose_name='fecha deseada')),
                ('hora', models.TimeField(verbose_name='hora deseada')),
                ('licencia', models.CharField(max_length=30, verbose_name='número de licencia de conducción')),
                ('comentario', models.TextField(blank=True)),
                ('estado', models.CharField(choices=[('pendiente', 'Pendiente'), ('aprobada', 'Aprobada'), ('rechazada', 'Rechazada'), ('realizada', 'Realizada')], default='pendiente', max_length=20)),
                ('respuesta_admin', models.TextField(blank=True, verbose_name='respuesta del concesionario')),
                ('creada', models.DateTimeField(auto_now_add=True)),
                ('moto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solicitudes_prueba', to='catalogo.moto')),
            ],
            options={
                'verbose_name': 'solicitud de prueba de manejo',
                'verbose_name_plural': 'solicitudes de prueba de manejo',
                'ordering': ['-creada'],
            },
        ),
    ]
