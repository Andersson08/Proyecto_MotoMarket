import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('catalogo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pago',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metodo', models.CharField(choices=[('tarjeta', 'Tarjeta de crédito/débito'), ('pse', 'PSE'), ('efectivo', 'Efectivo en sede')], max_length=20, verbose_name='método')),
                ('monto', models.DecimalField(decimal_places=0, max_digits=14)),
                ('estado', models.CharField(choices=[('aprobado', 'Aprobado'), ('rechazado', 'Rechazado')], max_length=20)),
                ('referencia', models.CharField(editable=False, max_length=40, unique=True)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('estado', models.CharField(choices=[('pendiente', 'Pendiente de pago'), ('pagado', 'Pagado'), ('en_preparacion', 'En preparación'), ('entregado', 'Entregado'), ('cancelado', 'Cancelado')], default='pendiente', max_length=20)),
                ('total', models.DecimalField(decimal_places=0, default=0, max_digits=14)),
                ('direccion_entrega', models.CharField(max_length=200, verbose_name='dirección de entrega')),
                ('ciudad', models.CharField(max_length=80)),
                ('telefono', models.CharField(max_length=20, verbose_name='teléfono')),
                ('notas', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['-fecha'],
            },
        ),
        migrations.CreateModel(
            name='DetallePedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField()),
                ('precio_unitario', models.DecimalField(decimal_places=0, max_digits=12)),
                ('moto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='catalogo.moto')),
            ],
            options={
                'verbose_name': 'detalle de pedido',
                'verbose_name_plural': 'detalles de pedido',
            },
        ),
    ]
