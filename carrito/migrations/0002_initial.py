import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('carrito', '0001_initial'),
        ('catalogo', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='carrito',
            name='usuario',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='carrito', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='itemcarrito',
            name='carrito',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='carrito.carrito'),
        ),
        migrations.AddField(
            model_name='itemcarrito',
            name='moto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogo.moto'),
        ),
        migrations.AddConstraint(
            model_name='itemcarrito',
            constraint=models.UniqueConstraint(fields=('carrito', 'moto'), name='moto_unica_en_carrito'),
        ),
    ]
