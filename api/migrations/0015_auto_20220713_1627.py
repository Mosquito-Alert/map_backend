# Generated by Django 3.2.9 on 2022-07-13 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_gadm'),
    ]

    operations = [
        migrations.AddField(
            model_name='mapauxreport',
            name='bite_time',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='mapauxreport',
            name='lau_code',
            field=models.CharField(default=None, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='mapauxreport',
            name='lau_name',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='mapauxreport',
            name='nuts0_code',
            field=models.CharField(default=None, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='mapauxreport',
            name='nuts0_name',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
    ]
