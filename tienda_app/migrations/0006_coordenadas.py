# Generated by Django 5.1.7 on 2025-03-21 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda_app', '0005_alter_carrito_cantidad'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coordenadas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitud', models.FloatField()),
                ('longitud', models.FloatField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
