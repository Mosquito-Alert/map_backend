# Generated by Django 4.0.4 on 2022-05-25 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_reportview'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mapauxreport',
            name='municipality',
        ),
        migrations.AddField(
            model_name='mapauxreport',
            name='bite_count',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='mapauxreport',
            name='bite_location',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='mapauxreport',
            name='ia_value',
            field=models.FloatField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='mapauxreport',
            name='larvae',
            field=models.BooleanField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='mapauxreport',
            name='nuts3_code',
            field=models.CharField(default=None, max_length=5, null=True),
        ),
        migrations.AddField(
            model_name='mapauxreport',
            name='nuts3_name',
            field=models.CharField(default=None, max_length=155, null=True),
        ),
        migrations.AddField(
            model_name='mapauxreport',
            name='s_a_1',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='mapauxreport',
            name='s_a_2',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='mapauxreport',
            name='s_a_3',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='mapauxreport',
            name='s_a_4',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='mapauxreport',
            name='s_q_1',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='mapauxreport',
            name='s_q_2',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='mapauxreport',
            name='s_q_3',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='mapauxreport',
            name='s_q_4',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='mapauxreport',
            name='t_a_1',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='mapauxreport',
            name='t_a_2',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='mapauxreport',
            name='t_a_3',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='mapauxreport',
            name='t_q_1',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='mapauxreport',
            name='t_q_2',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='mapauxreport',
            name='t_q_3',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='mapauxreport',
            name='validation',
            field=models.IntegerField(default=None, null=True),
        ),
    ]
