# Generated by Django 4.2 on 2023-04-23 14:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stockforecast', '0005_rename_symbols_stockprice_symbol'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockprice',
            name='stock',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stockprice', to='stockforecast.stock'),
        ),
    ]
