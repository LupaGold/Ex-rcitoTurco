# Generated by Django 5.0.4 on 2024-06-15 11:46

import django.db.models.deletion
import django.utils.timezone
import django_ckeditor_5.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PalestraSupervisores',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.TextField(max_length=30, null=True)),
                ('palestra', django_ckeditor_5.fields.CKEditor5Field(default=' ', verbose_name='palestrasup')),
            ],
        ),
        migrations.CreateModel(
            name='GuiaSupervisores',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guia', django_ckeditor_5.fields.CKEditor5Field(verbose_name='Guia')),
                ('datatime', models.DateTimeField(default=django.utils.timezone.now)),
                ('solicitante', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='solicitantesup', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SupervisorRelatorio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datatime', models.DateTimeField(default=django.utils.timezone.now)),
                ('patente_treinado', models.CharField(blank=True, choices=[('', 'Selecione a Patente'), ('Soldado', 'Soldado'), ('Soldado Estrela', 'Soldado Estrela'), ('Cabo', 'Cabo'), ('Aluno', 'Aluno'), ('Terceiro Sargento', 'Terceiro Sargento'), ('Segundo Sargento', 'Segundo Sargento'), ('Primeiro Sargento', 'Primeiro Sargento'), ('Subtenente', 'Subtenente'), ('Cadete', 'Cadete'), ('Aspirante-a-Oficial', 'Aspirante-a-Oficial'), ('Segundo Tenente', 'Segundo Tenente'), ('Primeiro Tenente', 'Primeiro Tenente'), ('Capitão', 'Capitão'), ('Major', 'Major'), ('Tenente-Coronel', 'Tenente-Coronel'), ('Coronel ★', 'Coronel ★'), ('General-de-Brigada ★★', 'General-de-Brigada ★★'), ('General-de-Divisão ★★★', 'General-de-Divisão ★★★'), ('General-de-Exército ★★★★', 'General-de-Exército ★★★★'), ('Marechal ★★★★★', 'Marechal ★★★★★')], max_length=50, null=True)),
                ('treinados', models.TextField(blank=True, max_length=50, null=True)),
                ('treinador', models.TextField(blank=True, max_length=20, null=True)),
                ('status', models.TextField(default='Em análise...', max_length=50, null=True)),
                ('palestra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Supervisores.palestrasupervisores')),
                ('solicitante', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
