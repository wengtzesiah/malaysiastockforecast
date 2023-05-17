# Generated by Django 4.2 on 2023-05-16 01:40

from django.db import migrations, models
import django_cryptography.fields


class Migration(migrations.Migration):

    dependencies = [
        ('stockforecast', '0018_alter_stock_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='exchange',
            field=django_cryptography.fields.encrypt(models.CharField(max_length=50)),
        ),
        migrations.AlterField(
            model_name='stock',
            name='lastprice',
            field=django_cryptography.fields.encrypt(models.CharField(max_length=255)),
        ),
    ]