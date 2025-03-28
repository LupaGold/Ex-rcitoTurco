# Generated by Django 5.0.4 on 2024-06-17 01:36

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
            name='Destaque3CIA',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datatime', models.DateTimeField(default=django.utils.timezone.now)),
                ('militar', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='militardestaque3cia', to=settings.AUTH_USER_MODEL)),
                ('solicitante', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='solicitantedest3cia', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Doação3CIA',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField(default=django.utils.timezone.now)),
                ('valor', models.TextField(blank=True, max_length=250, null=True)),
                ('doador', models.TextField(blank=True, max_length=250, null=True)),
                ('pagamento', models.CharField(choices=[('', 'Selecione o tipo de pagamento'), ('Moeda', 'Moeda'), ('Mobi', 'Mobi')], max_length=50, null=True)),
                ('solicitante', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Relatório3CIA',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField(default=django.utils.timezone.now)),
                ('tipoevento', models.CharField(blank=True, choices=[('', 'Selecione o tipo de evento'), ('Evento rápido', 'Evento rápido'), ('Evento interno', 'Evento interno'), ('Evento externo', 'Evento externo')], max_length=250, null=True)),
                ('vencedores', models.TextField(blank=True, max_length=250, null=True)),
                ('doacao', models.TextField(blank=True, max_length=250, null=True)),
                ('obs', models.TextField(blank=True, max_length=250, null=True)),
                ('resp', models.ForeignKey(limit_choices_to={'groups__name': 'M3CIA'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('solicitante', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='solicitanterelt3cia', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
