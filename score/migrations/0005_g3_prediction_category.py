# Generated by Django 3.0 on 2020-05-03 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('score', '0004_auto_20200503_2218'),
    ]

    operations = [
        migrations.AddField(
            model_name='g3_prediction',
            name='category',
            field=models.CharField(default='pass', max_length=4),
            preserve_default=False,
        ),
    ]