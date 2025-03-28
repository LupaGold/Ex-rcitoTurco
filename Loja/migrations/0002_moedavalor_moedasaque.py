# Generated by Django 5.0.4 on 2024-06-15 08:42

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Loja', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MoedaValor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.TextField(max_length=30, null=True)),
                ('moedas', models.FloatField(default=0.0)),
                ('datatime', models.DateTimeField(default=django.utils.timezone.now)),
                ('icone', models.ImageField(upload_to='imagens/')),
                ('solicitante', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='solicitantesaque', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MoedaSaque',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('solicitante', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='militarsaque', to=settings.AUTH_USER_MODEL)),
                ('icone', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Loja.moedavalor')),
            ],
        ),
    ]
