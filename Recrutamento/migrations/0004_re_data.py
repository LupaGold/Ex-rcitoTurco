# Generated by Django 5.0.4 on 2024-08-01 02:05

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Recrutamento', '0003_remove_re_status_re_militar_alter_logre_re'),
    ]

    operations = [
        migrations.AddField(
            model_name='re',
            name='data',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
