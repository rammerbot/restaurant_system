# Generated by Django 5.1.8 on 2025-04-17 00:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creado')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Actualizado')),
                ('employee', models.CharField(blank=True, max_length=100, null=True, verbose_name='Employee')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
