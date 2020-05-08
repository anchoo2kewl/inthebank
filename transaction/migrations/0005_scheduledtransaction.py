# Generated by Django 3.0.5 on 2020-04-30 12:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0004_auto_20200422_0955'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScheduledTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('repeat_every', models.CharField(blank=True, choices=[('AM', 'Repeat Monthly on Approx. Specific Date'), ('AB', 'Repeat Bi-Weekly on Approx. Specific Date'), ('SM', 'Repeat Monthly on Specific Date'), ('B', 'Repeat Bi-Weekly based on Initial Date')], max_length=2, null=True)),
                ('working_date', models.DateField(blank=True, null=True)),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transaction.Transaction')),
            ],
        ),
    ]
