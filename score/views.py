from django.contrib import messages
# from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ValidationError , ObjectDoesNotExist
from django.forms import CheckboxSelectMultiple, CheckboxInput, DateInput,  Select
from django.shortcuts import render, reverse, redirect
from django.urls import reverse_lazy
from django.utils.datastructures import MultiValueDictKeyError
from django.utils import timezone

from .models import G1, G2, G3, G3_prediction
from dashboard.models import Student, Course, Lecturer, CourseTaken

from .tasks import classification_g1, classification_g2, preprocessing_g1, preprocessing_g2


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
        
        messages.success(request, "G1 scores saved")
        print(students)

        g1_df = preprocessing_g1(students)
        input_df = g1_df.drop('matric_number', axis=1)
        predictions = classification_g1(input_df) 

        # creates or updates the predicted scores for the students
        for g1_obj, category in zip(students, predictions):
            g3_obj, created = G3_prediction.objects.get_or_create(
                student = g1_obj.student,
                course  = course,
            )
            print('G3_obj', g3_obj, created)
            if not created:
                g3_obj.category = category
                g3_obj.save()

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
        print(students)

        # transforms the student data to a format that can machine learning model can use to produce output
        g2_df = preprocessing_g2(students, g1_scores)

        input_df = g2_df.drop('matric_number', axis=1)
        print(g2_df['G1'])
        # the predictions of the class
        predictions = classification_g2(input_df) 

        # creates or updates the predicted scores for the students 
        for g2_obj, category in zip(students, predictions):
            g3_obj, created = G3_prediction.objects.get_or_create(
                student = g2_obj.student,
                course  = course,
            )
            print('G3_obj', g3_obj, created)
            if not created:
                g3_obj.category = category
                g3_obj.save()

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

    predictions = G3_prediction.objects.filter(course__slug = course_slug ).order_by('category')
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
    
