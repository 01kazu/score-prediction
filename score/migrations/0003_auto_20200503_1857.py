# Generated by Django 3.0 on 2020-05-03 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('score', '0002_auto_20200503_1756'),
    ]

    operations = [
        migrations.AlterField(
            model_name='g1',
            name='score',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='g2',
            name='score',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='g3',
            name='score',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='g3_prediction',
            name='score',
            field=models.IntegerField(default=0),
        ),
    ]