# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-12 14:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Identidade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.SlugField(unique=True)),
                ('pubkey', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Mensagem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.TextField()),
                ('data', models.DateTimeField(auto_now_add=True)),
                ('validade', models.IntegerField(default=3)),
                ('destinatario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='caixa_de_entrada', to='api.Identidade')),
                ('remetente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='caixa_de_saida', to='api.Identidade')),
            ],
        ),
    ]
