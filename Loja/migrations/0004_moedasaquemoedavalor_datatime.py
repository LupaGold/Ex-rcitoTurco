# Generated by Django 5.0.4 on 2024-06-15 08:56

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Loja', '0003_moedasaquemoedavalor_delete_moedasaque'),
    ]

    operations = [
        migrations.AddField(
            model_name='moedasaquemoedavalor',
            name='datatime',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
