# Generated by Django 4.0.4 on 2023-04-21 13:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_wmsserver_wmsmaplayers'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='WmsMapLayers',
            new_name='WmsMapLayer',
        ),
    ]
