# Generated by Django 4.2 on 2023-05-04 01:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stockforecast', '0013_delete_stockpriceprediction'),
    ]

    operations = [
        migrations.CreateModel(
            name='LstmForecastedValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('next_five_days_values', models.JSONField()),
                ('next_five_weeks_values', models.JSONField()),
                ('next_five_months_values', models.JSONField()),
                ('next_five_years_values', models.JSONField()),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stockforecast.stock')),
            ],
        ),
    ]
