from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import SchoolAdmin, Student, Lecturer, Course, CourseTaken


class SchoolAdminForm(forms.ModelForm):
    """Form For Creating School Admins"""
    class Meta:
        model = SchoolAdmin
        fields = ( 'phone_number', 'date_of_birth', 'gender', 'profile_pic')
        widgets = {
            'date_of_birth' : forms.DateInput(attrs= {'type': 'date'}),
        }


class LecturerForm(forms.ModelForm):
    """Form For Creating Lecturers"""
    class Meta:
        model = Lecturer
        fields = ('phone_number', 'date_of_birth', 'gender', 'department', 'position', 'profile_pic', )
        widgets = {
            'date_of_birth' : forms.DateInput(attrs= {'type': 'date'}),
        }


class StudentForm(forms.ModelForm):
    """Form For Creating Students"""
    class Meta:
        model = Student
        fields = ('phone_number', 'date_of_birth', 'address', 'reason', 'mother_job', 'father_job', 'guardian', 'gender', 'department', 'level', 'profile_pic', 'year_enrolled', )
        widgets = {
            'date_of_birth' : forms.DateInput(attrs= {'type': 'date'}),
        }

class SignUpForm(UserCreationForm):
    """Form For Creating Users (Student, Lecturer, School Admin)"""
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name','password1', 'password2', )


class CourseForm(forms.ModelForm):
    """Form For Creating Courses"""
    class Meta:
        model = Course
        fields = ('course_title', 'course_code', 'credit_unit', 'lecturer', 'is_elective', 'department','level')


class UpdateUserForm(UserChangeForm):
    """Form For Updating Users (Student, Lecturer, School Admin)"""
    class Meta:
        model = User
        fields = ('username','email', 'first_name', 'last_name')


class CourseTakenForm(forms.ModelForm):
    """Form For Registered Courses"""
    class Meta:
        model = CourseTaken
        fields = ('course',)
        
        






        