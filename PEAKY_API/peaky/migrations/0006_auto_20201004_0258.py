# Generated by Django 3.1.2 on 2020-10-04 02:58

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('peaky', '0005_auto_20201003_2319'),
    ]

    operations = [
        migrations.CreateModel(
            name='PeakModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('altitude', models.FloatField()),
                ('name', models.CharField(max_length=100)),
                ('location', django.contrib.gis.db.models.fields.PointField(help_text='the location of the peak', srid=4326)),
            ],
        ),
        migrations.RenameModel(
            old_name='AttempsFailModel',
            new_name='AttemptFailModel',
        ),
    ]
