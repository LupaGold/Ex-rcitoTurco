# Generated by Django 5.0.4 on 2024-06-07 01:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Militares', '0003_militarusuario_patente_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='militarusuario',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]
