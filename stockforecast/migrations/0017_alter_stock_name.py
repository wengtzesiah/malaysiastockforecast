# Generated by Django 4.2 on 2023-05-16 01:36

from django.db import migrations, models
import django_cryptography.fields


class Migration(migrations.Migration):

    dependencies = [
        ('stockforecast', '0016_mlpforecastedvalue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='name',
            field=django_cryptography.fields.encrypt(models.CharField(default='NA', max_length=255)),
        ),
    ]
