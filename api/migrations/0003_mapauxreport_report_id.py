# Generated by Django 3.2.9 on 2022-03-29 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_mapauxreport_responses_json'),
    ]

    operations = [
        migrations.AddField(
            model_name='mapauxreport',
            name='report_id',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]