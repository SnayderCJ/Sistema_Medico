# Generated by Django 5.1.3 on 2024-11-22 13:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attention', '0021_detalleatencion_examen_solicitado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detalleatencion',
            name='examen_solicitado',
        ),
    ]
