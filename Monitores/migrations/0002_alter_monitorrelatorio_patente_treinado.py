# Generated by Django 5.0.4 on 2024-11-26 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Monitores', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monitorrelatorio',
            name='patente_treinado',
            field=models.CharField(blank=True, choices=[('', 'Selecione a Patente'), ('Soldado', 'Soldado'), ('Soldado Estrela', 'Soldado Estrela'), ('Cabo', 'Cabo'), ('Aluno', 'Aluno'), ('Terceiro Sargento', 'Terceiro Sargento'), ('Segundo Sargento', 'Segundo Sargento'), ('Primeiro Sargento', 'Primeiro Sargento'), ('Subtenente', 'Subtenente'), ('Cadete', 'Cadete')], max_length=50, null=True),
        ),
    ]
