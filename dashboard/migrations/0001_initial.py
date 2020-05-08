# Generated by Django 3.0 on 2020-05-03 16:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import image_optimizer.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_title', models.CharField(max_length=256)),
                ('course_code', models.CharField(max_length=10)),
                ('credit_unit', models.IntegerField()),
                ('is_elective', models.BooleanField()),
                ('slug', models.SlugField(blank=True)),
                ('level', models.IntegerField(choices=[(100, 100), (200, 200), (300, 300), (400, 400)])),
                ('department', models.CharField(blank=True, choices=[('computer science', 'Computer Science')], max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=6)),
                ('department', models.CharField(choices=[('computer science', 'Computer Science')], max_length=200)),
                ('phone_number', models.CharField(max_length=20)),
                ('matric_number', models.CharField(max_length=20, unique=True)),
                ('level', models.IntegerField(choices=[(100, 100), (200, 200), (300, 300), (400, 400)])),
                ('year_enrolled', models.IntegerField(choices=[(2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2016), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023), (2024, 2024)])),
                ('profile_pic', image_optimizer.fields.OptimizedImageField(upload_to='student_profile_pic')),
                ('age', models.IntegerField(blank=True)),
                ('address', models.CharField(choices=[('urban', 'Urban'), ('rural', 'rural')], max_length=5)),
                ('reason', models.CharField(choices=[('close to home', 'Close to home'), ('school reputation', 'School Reputation'), ('course preference', 'Course Preference'), ('other', 'Other')], max_length=18)),
                ('mother_job', models.CharField(choices=[('teacher', 'Teacher'), ('health', 'Health Care Related'), ('services', 'Civil Services'), ('at_home', 'Home'), ('other', 'Other')], max_length=20)),
                ('father_job', models.CharField(choices=[('teacher', 'Teacher'), ('health', 'Health Care Related'), ('services', 'Civil Services'), ('at_home', 'Home'), ('other', 'Other')], max_length=20)),
                ('guardian', models.CharField(choices=[('father', 'Father'), ('mother', 'Mother'), ('other', 'Other')], max_length=6)),
                ('user', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SchoolAdmin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=6)),
                ('phone_number', models.CharField(max_length=20)),
                ('schooladmin_access', models.BooleanField(default=True)),
                ('profile_pic', image_optimizer.fields.OptimizedImageField(upload_to='admin_profile_pic')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Lecturer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=6)),
                ('department', models.CharField(choices=[('computer science', 'Computer Science')], max_length=200)),
                ('position', models.CharField(max_length=200)),
                ('phone_number', models.CharField(max_length=20)),
                ('lecturer_access', models.BooleanField(blank=True, default=True, null=True)),
                ('profile_pic', image_optimizer.fields.OptimizedImageField(upload_to='lecturer_profile_pic')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CourseTaken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ManyToManyField(help_text='Hold down “Ctrl” on Windows, or “Command” on a Mac, to select more than one.', to='dashboard.Course')),
                ('student', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.Student')),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='lecturer',
            field=models.ManyToManyField(help_text='Hold down “Ctrl” on Windows, or “Command” on a Mac, to select more than one.', to='dashboard.Lecturer'),
        ),
    ]