from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify 
from image_optimizer.fields import OptimizedImageField
from datetime import date

#
#
#  CHANGE LECTURER TO TEACHER
#
#

GENDER_CHOICES = (('male', 'Male'),
                ('female', 'Female')
                )
LEVEL_CHOICES = (
                (100,100),
                (200,200),
                (300,300),
                (400,400),
                (500,500)
                )
YEAR_CHOICES = (
                (2014, 2014),
                (2015, 2015),
                (2016, 2016),
                (2017, 2017),
                (2018, 2018),
                (2019, 2019),
                (2020, 2020),
                (2021, 2021),
                (2022, 2022),
                (2023, 2023),
                (2024, 2024),
                )
DEPARTMENT_CHOICES = (
                ('computer science', 'Computer Science'),
                    )
ADDRESS_CHOICES = (
                    ('urban', 'Urban'),
                    ('rural', 'Rural')
                )
REASON_CHOICES = (
                    ('close to home', 'Close to home'),
                    ('school reputation', 'School Reputation'),
                    ('course preference', 'Course Preference'),
                    ('other', 'Other')
                )
JOB_CHOICES = (
                ('teacher', 'Teacher'),
                ('health', 'Health Care Related'),
                ('services', 'Civil Services'),
                ('at_home', 'Home'),
                ('other', 'Other')

            )
GUARDIAN_CHOICES = (
                    ('father', 'Father'),
                    ('mother', 'Mother'),
                    ('other', 'Other')
                    )




class SchoolAdmin(models.Model):
    """Model That Represents The School Admin"""
    user                =   models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth       =   models.DateField()
    gender              =   models.CharField(max_length=6, choices=GENDER_CHOICES)
    phone_number        =   models.CharField(max_length=20)
    schooladmin_access  =   models.BooleanField(default=True)
    profile_pic = OptimizedImageField(
                    upload_to='admin_profile_pic',
                    optimized_image_output_size=(400, 300),
                    optimized_image_resize_method='cover'  # 'thumbnail', 'cover' or None
                )

    def __str__(self):
        """Returns The School Admin's First And Last Name When The Object Is Called"""
        return f'{self.user.first_name} {self.user.last_name}'

    
class Lecturer(models.Model):
    """Model That Represents The Lecturer"""
    user                =   models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth       =   models.DateField()
    gender              =   models.CharField(max_length=6, choices=GENDER_CHOICES)
    department          =   models.CharField(max_length=200, choices=DEPARTMENT_CHOICES)
    position            =   models.CharField(max_length=200)
    phone_number        =   models.CharField(max_length=20)
    lecturer_access     =   models.BooleanField(default=True, blank=True, null=True)
    profile_pic = OptimizedImageField(
                    upload_to='lecturer_profile_pic',
                    optimized_image_output_size=(400, 300),
                    optimized_image_resize_method='cover'  
                    # 'thumbnail', 'cover' or None
                )

    def __str__(self):
        """Returns The Lecturer's First And Last Name When The Object Is Called"""
        return f'{self.user.first_name} {self.user.last_name}'


class Student(models.Model):
    """Model That Represents The Student"""
    user                =   models.OneToOneField(User, on_delete=models.CASCADE, blank=True)
    date_of_birth       =   models.DateField()
    gender              =   models.CharField(max_length=6, choices=GENDER_CHOICES)
    department          =   models.CharField(max_length=200, choices=DEPARTMENT_CHOICES)
    phone_number        =   models.CharField(max_length=20)
    matric_number       =   models.CharField(max_length=20, unique=True)
    level               =   models.IntegerField(choices=LEVEL_CHOICES)
    year_enrolled       =   models.IntegerField(choices=YEAR_CHOICES)
    profile_pic = OptimizedImageField(
                    upload_to='student_profile_pic',
                    optimized_image_output_size=(400, 300),
                    optimized_image_resize_method='cover'  # 'thumbnail', 'cover' or None
                )
    age                 =   models.IntegerField(blank=True)
    address             =   models.CharField(max_length=5, choices=ADDRESS_CHOICES)
    reason              =   models.CharField(max_length=18, choices=REASON_CHOICES)
    mother_job          =   models.CharField(max_length=20, choices=JOB_CHOICES)
    father_job          =   models.CharField(max_length=20, choices=JOB_CHOICES)
    guardian            =   models.CharField(max_length=6, choices=GUARDIAN_CHOICES)
    student_access      =   models.BooleanField(default=True)

    def __str__(self):
        """Returns The Student's Matric Number When The Object Is Called""" 
        return f'{self.matric_number}'

    def save(self, *args, **kwargs):
        """ Saves the Age of the Student """
        days_in_year = 365.2425    
        age = int((date.today() - self.date_of_birth).days / days_in_year) 
        self.age = age
        self.matric_number = self.matric_number.upper()
        super(Student, self).save(*args, **kwargs)

    
class Course(models.Model):
    """Model That Represents The Course"""
    course_title        =   models.CharField(max_length=256)
    course_code         =   models.CharField(max_length=10)
    credit_unit         =   models.IntegerField()
    lecturer            =   models.ManyToManyField(Lecturer, help_text ="Hold down “Ctrl” on Windows, or “Command” on a Mac, to select more than one." )
    is_elective         =   models.BooleanField()
    slug                =   models.SlugField(blank=True)
    level               =   models.IntegerField(choices=LEVEL_CHOICES)
    department          =   models.CharField(max_length=256, blank=True, choices = DEPARTMENT_CHOICES)

    def __str__(self):
        """Returns The Name Of The Course When The Object Is Retrieved"""
        return f'{self.course_title}'

    def save(self, *args, **kwargs): 
        """Slugifies The Course Title Before Saving The Object"""
        self.slug = slugify(self.course_title) 
        self.title = self.title.upper()
        super(Course, self).save(*args, **kwargs) 


class CourseTaken(models.Model):
    """Model That Represents The Courses Registered By The Student"""
    course = models.ManyToManyField(Course, help_text = "Hold down “Ctrl” on Windows, or “Command” on a Mac, to select more than one.")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank =True)

    def __str__(self):
        """Returns The Student's Matric Number When The Object Is Retrieved"""
        return f'{self.student.matric_number}'







