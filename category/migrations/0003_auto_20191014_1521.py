# Generated by Django 2.2.6 on 2019-10-14 19:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0002_auto_20191014_1521'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='category.CategoryGroup'),
        ),
    ]
