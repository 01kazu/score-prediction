# Generated by Django 3.0 on 2020-05-03 16:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='G3_prediction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Course')),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Student')),
            ],
        ),
        migrations.CreateModel(
            name='G3',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Course')),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Student')),
            ],
        ),
        migrations.CreateModel(
            name='G2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Course')),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Student')),
            ],
        ),
        migrations.CreateModel(
            name='G1',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(max_length=20)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Student')),
            ],
        ),
    ]
