# Generated by Django 3.0 on 2020-05-03 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('score', '0005_g3_prediction_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='g3_prediction',
            name='category',
            field=models.CharField(blank=True, max_length=4),
        ),
    ]
