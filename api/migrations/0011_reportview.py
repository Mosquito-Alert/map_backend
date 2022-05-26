# Generated by Django 3.2.9 on 2022-05-22 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_alter_mapview_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportView',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=8, unique=True)),
                ('view', models.TextField(blank=True, null=True)),
                ('date', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]