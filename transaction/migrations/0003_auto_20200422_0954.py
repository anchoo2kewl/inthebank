# Generated by Django 3.0.5 on 2020-04-22 13:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0006_auto_20200422_0952'),
        ('transaction', '0002_auto_20200422_0952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='category',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.SET_DEFAULT, to='category.Category'),
        ),
    ]
