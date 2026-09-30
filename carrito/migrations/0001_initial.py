from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Carrito',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actualizado', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ItemCarrito',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField(default=1)),
            ],
            options={
                'verbose_name': 'ítem del carrito',
                'verbose_name_plural': 'ítems del carrito',
            },
        ),
    ]
