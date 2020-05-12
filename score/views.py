from django.contrib import messages
# from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ValidationError , ObjectDoesNotExist
from django.core import serializers
from django.forms import CheckboxSelectMultiple, CheckboxInput, DateInput,  Select
from django.shortcuts import render, reverse, redirect
from django.urls import reverse_lazy
from django.utils.datastructures import MultiValueDictKeyError
from django.utils import timezone

from .models import G1, G2, G3, G3_prediction
from dashboard.models import Student, Course, Lecturer, CourseTaken

from .tasks import classification_g1, classification_g2


@user_passes_test(lambda user: not user.is_anonymous and  user.lecturer.lecturer_access, login_url='lecturer-admin-login')
def dashboard(request):
    """Dashboard For Lecturers"""
    
    user = request.user
    lecturer_courses = user.lecturer.course_set.all()

    courses_taken = lecturer_courses.count()
    # number of students failing a particular courses
    predict_fail = []

    for course in lecturer_courses:
        course_predict_fail = G3_prediction.objects.filter(course = course, category="fail").count()
        predict_fail.append(course_predict_fail)

    predict_fail = zip(predict_fail, lecturer_courses)

    context = {
        'courses'   : lecturer_courses,
        'no_courses': courses_taken,
        'no_of_students_failed': predict_fail
    }

    return render(request, 'dashboard/lecturer/base.html', context)


@user_passes_test(lambda user: not user.is_anonymous and  user.lecturer.lecturer_access, login_url='lecturer-admin-login')
def g1_scores(request, course_slug):
    """Function For Taking Student's G1 Score"""
    students    = G1.objects.filter(course__slug = course_slug).order_by('student__matric_number')
    user        = request.user
    lecturer_courses = user.lecturer.course_set.all()
    course = Course.objects.get(slug = course_slug)

    if request.method == 'POST':
        for student in students:
            # When the submit button is clicked, all student's scores are updated
            student.score = request.POST.get(f'{student.student.matric_number}-g1')
            student.save()

        student_serialized = serializers.serialize("json", students)
        course_serialized = serializers.serialize("json", [course, ])

        classification_g1.delay(student_serialized, course_serialized)

        messages.success(request, "G1 scores saved")

    context = {
        'students'  : students,
        'courses'   : lecturer_courses,
        'course'    : course,
    }
    return render(request, 'dashboard/lecturer/g1_score.html', context)


@user_passes_test(lambda user: not user.is_anonymous and  user.lecturer.lecturer_access, login_url='lecturer-admin-login')
def g2_scores(request, course_slug):
    """Function For Taking Student's G2 Score"""
    students    = G2.objects.filter(course__slug = course_slug).order_by('student__matric_number')
    user        = request.user
    lecturer_courses = user.lecturer.course_set.all()
    course = Course.objects.get(slug = course_slug)

    g1_scores = G1.objects.filter(course__slug = course_slug).order_by('student__matric_number')

    if request.method == 'POST':
        for student in students:
            # When the submit button is clicked, all student's scores are updated
            student.score = request.POST.get(f'{student.student.matric_number}-g2')
            student.save()
        
        messages.success(request, "G2 scores saved")

        student_serialized = serializers.serialize("json", students)
        g1_scores_serialized = serializers.serialize('json', g1_scores)
        course_serialized = serializers.serialize("json", [course, ])

        classification_g2.delay(student_serialized, g1_scores_serialized, course_serialized)

    context = {
        'students'  : students,
        'courses'   : lecturer_courses,
        'course'    : course,
    }
    return render(request, 'dashboard/lecturer/g2_score.html', context)


@user_passes_test(lambda user: not user.is_anonymous and  user.lecturer.lecturer_access, login_url='lecturer-admin-login')
def g3_scores(request, course_slug):
    """Function For Taking Student's G3 Score"""
    students    = G3.objects.filter(course__slug = course_slug).order_by('student__matric_number')
    user        = request.user
    lecturer_courses = user.lecturer.course_set.all()
    course = Course.objects.get(slug=course_slug)

    if request.method == 'POST':
        for student in students:
            # When the submit button is clicked, all student's scores are updated
            student.score = request.POST.get(f'{student.student.matric_number}-g3')
            student.save()
        
        messages.success(request, "G3 scores saved")

    context = {
        'students'  : students,
        'courses'   : lecturer_courses,
        'course'    : course,
    }
    return render(request, 'dashboard/lecturer/g3_score.html', context)


@user_passes_test(lambda user: not user.is_anonymous and  user.lecturer.lecturer_access, login_url='lecturer-admin-login')
def g3_predictions(request, course_slug):
    """Function For predicting students' G3 category(pass/fail)"""
    lecturer_courses = request.user.lecturer.course_set.all()
    course = Course.objects.get(slug = course_slug)

    predictions = G3_prediction.objects.filter(course__slug = course_slug ).order_by('group')
    context = {
        'predictions' : predictions,
        'courses'   : lecturer_courses,
        'course'    : course,
    }

    return render(request, 'dashboard/lecturer/predictions.html', context)


@user_passes_test(lambda user: not user.is_anonymous and user.student.student_access, login_url='student-login')
def student_scores(request):
    student = Student.objects.get(user = request.user)

    student_courses = Course.objects.filter(department = student.department, level = student.level).order_by('course_title')

    student_g1 = G1.objects.filter(student = student).order_by('course__course_title')
    student_g2 = G2.objects.filter(student = student).order_by('course__course_title')
    student_g3 = G3.objects.filter(student = student).order_by('course__course_title')

    print(student_g1)
    print(student_g2)
    print(student_g3)

    student_score = zip(student_courses, student_g1, student_g2, student_g3)

    context ={
        'student_score' : student_score,
    }
    
    return render(request, 'dashboard/student/home.html', context )
    
