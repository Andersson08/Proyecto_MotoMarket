import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=60, unique=True)),
                ('descripcion', models.TextField(blank=True, verbose_name='descripción')),
            ],
            options={
                'verbose_name': 'categoría',
                'verbose_name_plural': 'categorías',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='Marca',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=60, unique=True)),
                ('pais_origen', models.CharField(blank=True, max_length=60, verbose_name='país de origen')),
                ('logo', models.ImageField(blank=True, upload_to='marcas/')),
            ],
            options={
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='Moto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modelo', models.CharField(max_length=100)),
                ('slug', models.SlugField(blank=True, max_length=140, unique=True)),
                ('anio', models.PositiveIntegerField(verbose_name='año')),
                ('cilindraje', models.PositiveIntegerField(default=0, verbose_name='cilindraje (cc)')),
                ('potencia_hp', models.DecimalField(decimal_places=1, default=0, max_digits=6, verbose_name='potencia (HP)')),
                ('combustible', models.CharField(choices=[('gasolina', 'Gasolina'), ('electrica', 'Eléctrica')], default='gasolina', max_length=20)),
                ('transmision', models.CharField(choices=[('manual', 'Manual'), ('automatica', 'Automática'), ('semiautomatica', 'Semiautomática')], default='manual', max_length=20, verbose_name='transmisión')),
                ('color', models.CharField(blank=True, max_length=40)),
                ('precio', models.DecimalField(decimal_places=0, max_digits=12, verbose_name='precio (COP)')),
                ('stock', models.PositiveIntegerField(default=0)),
                ('descripcion', models.TextField(blank=True, verbose_name='descripción')),
                ('destacada', models.BooleanField(default=False)),
                ('activa', models.BooleanField(default=True)),
                ('creada', models.DateTimeField(auto_now_add=True)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='motos', to='catalogo.categoria', verbose_name='categoría')),
                ('marca', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='motos', to='catalogo.marca')),
            ],
            options={
                'ordering': ['-creada'],
            },
        ),
        migrations.CreateModel(
            name='ImagenMoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(blank=True, upload_to='motos/')),
                ('url', models.CharField(blank=True, max_length=500, verbose_name='URL de la imagen')),
                ('credito', models.CharField(blank=True, max_length=200, verbose_name='crédito de la foto')),
                ('principal', models.BooleanField(default=False)),
                ('moto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imagenes', to='catalogo.moto')),
            ],
            options={
                'verbose_name': 'imagen de moto',
                'verbose_name_plural': 'imágenes de motos',
            },
        ),
        migrations.CreateModel(
            name='Resena',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calificacion', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='calificación')),
                ('comentario', models.TextField(blank=True)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('moto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resenas', to='catalogo.moto')),
            ],
            options={
                'verbose_name': 'reseña',
                'verbose_name_plural': 'reseñas',
                'ordering': ['-fecha'],
            },
        ),
    ]
