# Generated by Django 3.0 on 2020-05-11 15:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_auto_20200511_1526'),
        ('score', '0010_auto_20200511_1628'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='g3_prediction',
            unique_together={('student', 'course')},
        ),
    ]
