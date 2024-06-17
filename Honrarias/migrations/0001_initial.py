# Generated by Django 5.0.4 on 2024-06-07 00:29

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HonrariasRegistro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.TextField(max_length=30, null=True)),
                ('descricao', models.TextField(max_length=70, null=True)),
                ('datatime', models.DateTimeField(default=django.utils.timezone.now)),
                ('icone', models.ImageField(upload_to='imagens/')),
                ('imagem', models.ImageField(upload_to='imagens/')),
                ('solicitante', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='solicitantehonraria', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
