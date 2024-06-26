# Generated by Django 4.0.4 on 2022-10-06 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_expiratingviews'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(blank=True, max_length=254, unique=True)),
                ('value', models.CharField(blank=True, max_length=254)),
            ],
            options={
                'verbose_name': 'App settings',
                'verbose_name_plural': 'App settings',
            },
        ),
        migrations.DeleteModel(
            name='ExpiratingViews',
        ),
    ]
