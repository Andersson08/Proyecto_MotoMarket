import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('catalogo', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='resena',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resenas', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name='resena',
            constraint=models.UniqueConstraint(fields=('moto', 'usuario'), name='una_resena_por_moto'),
        ),
    ]
