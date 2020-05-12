from django.shortcuts import render, redirect, get_object_or_404
from .forms import SchoolAdminForm, LecturerForm, StudentForm, SignUpForm, CourseForm, UpdateUserForm, CourseTakenForm
from .models import SchoolAdmin, Lecturer, Student, Course, CourseTaken
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from django.views.generic import ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.utils.datastructures import MultiValueDictKeyError

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import (PasswordResetView,PasswordResetDoneView,
                                       PasswordResetConfirmView, PasswordResetCompleteView)
from django.core.paginator import Paginator


@user_passes_test(lambda user: not user.is_anonymous and user.schooladmin.schooladmin_access, login_url='lecturer-admin-login')
def home(request):
    """School Admin Dashboard"""
    no_of_students = Student.objects.all().count()
    no_of_courses  = Course.objects.all().count()
    no_of_lecturers = Lecturer.objects.all().count()
    no_of_admins = SchoolAdmin.objects.all().count()

    no_of_male_students = Student.objects.filter(gender ='male').count()
    no_of_female_students = no_of_students - no_of_male_students

    no_of_100_level = Student.objects.filter(level=100).count()
    no_of_200_level = Student.objects.filter(level=200).count()
    no_of_300_level = Student.objects.filter(level=300).count()
    no_of_400_level = Student.objects.filter(level=400).count()

    context = {
        'students'  :   no_of_students,
        'courses'   :   no_of_courses,
        'lecturers' :   no_of_lecturers,
        'admins'    :   no_of_admins,
        'male_students'  : no_of_male_students,
        'female_students': no_of_female_students,
        '100_level' : no_of_100_level,
        '200_level' : no_of_200_level,
        '300_level' : no_of_300_level,
        '400_level' : no_of_400_level,
    
    }
    return render(request, 'dashboard/school-admin/base.html', context)


def student_login(request):
    """Login To Systems For Students"""
    if request.method == "POST":
        try:
            student = Student.objects.get(matric_number = request.POST['matric_number'] )

        except ObjectDoesNotExist:
             student = None

        if student != None:
            username  = student.user.username.lower()
            password = request.POST.get('password')

            student = authenticate(username=username, password=password)
            if student:
                if student.is_active:
                    login(request, student)
                    return redirect("course-reg")
                else:
                    return render(request, 'dashboard/accounts/login.html')
            else:
                messages.warning(request, "Username or Password is invalid")

        else:
            messages.warning(request, "Username or Password is invalid")

    return render(request, 'dashboard/accounts/student-login.html')
            
        
def lecturer_admin_login(request):
    """Lecturer And School Admin Log In"""
    if request.method == "POST":
        try:
            username = request.POST['username'].lower()
        except MultiValueDictKeyError:
            username = None
            
        if  username != None:
            username  = username.lower()
            password = request.POST.get('password')

            lecturer_admin = authenticate(username=username, password=password)
            if lecturer_admin:
                try:
                    lecturer = Lecturer.objects.get(user = lecturer_admin)
                except ObjectDoesNotExist:
                    lecturer = None
                if lecturer:
                    if lecturer.lecturer_access == True:

                        if lecturer_admin.is_active:
                            login(request, lecturer_admin)
                            return redirect("scores:dashboard")
                        else:
                            return render(request, 'dashboard/accounts/login.html')
                try:
                    admin = SchoolAdmin.objects.get(user = lecturer_admin)
                except ObjectDoesNotExist:
                    admin = None
                if admin:
                    if admin.schooladmin_access:
                    
                        if lecturer_admin.is_active:
                            login(request, lecturer_admin)
                            return redirect("home")
                        else:
                            return render(request, 'dashboard/accounts/login.html')
            else:
                messages.warning(request, "Username or Password is invalid")
        else:
            messages.warning(request, "Username or Password is invalid")
                

    return render(request, 'dashboard/accounts/lecturer-admin-login.html')

    
@user_passes_test(lambda user: not user.is_anonymous and user.schooladmin.schooladmin_access, login_url='lecturer-admin-login')
def create_student(request):
    """Function To Create Student"""
    userform = SignUpForm(request.POST)
    studentinfo = StudentForm(request.POST, request.FILES)
      
    if request.method == "POST":
        userform = SignUpForm(request.POST)
        studentinfo = StudentForm(data=request.POST, files=request.FILES)
        if userform.is_valid() and studentinfo.is_valid():
            userform.save(commit=False)
            userform.username = userform.cleaned_data['username'].lower()
            userform.save()

            student = User.objects.get(username = userform.cleaned_data['username'])
            studentinfo.save(commit=False)

            last_student = Student.objects.all().last()
            if last_student == None:
                # if there is no student in the database, make his matric number end in '0001'
                matric_number = 'BHU/'+ str ((studentinfo.cleaned_data['year_enrolled'] - 2000)) +'/04/05/0001'
            else:
                # else get the last student's matric number and add one(1) to it
                matric_number = int(last_student.matric_number[-4:]) + 1
                matric_number = 'BHU/'+ str ((studentinfo.cleaned_data['year_enrolled'] - 2000)) +'/04/05/'+ str(matric_number).zfill(4)
            
            Student.objects.create(user=student, 
                                    date_of_birth = studentinfo.cleaned_data['date_of_birth'], 
                                    gender        = studentinfo.cleaned_data['gender'], 
                                    department    = studentinfo.cleaned_data['department'], 
                                    matric_number = matric_number,
                                    phone_number  = studentinfo.cleaned_data['phone_number'],
                                    profile_pic   = studentinfo.cleaned_data['profile_pic'],
                                    level         = studentinfo.cleaned_data['level'],
                                    year_enrolled = studentinfo.cleaned_data['year_enrolled'],
                                    address = studentinfo.cleaned_data['address'],
                                    reason = studentinfo.cleaned_data['reason'],
                                    mother_job = studentinfo.cleaned_data['mother_job'],
                                    father_job = studentinfo.cleaned_data['father_job'],
                                    guardian = studentinfo.cleaned_data['guardian'],

                                     )
            messages.success(request, f"{userform.cleaned_data['first_name'].title()} with Matric number: {matric_number} created")  

    context = {'userform': userform, 
               'studentinfo': studentinfo
               }  
    return render(request, 'dashboard/school-admin/create-student.html', context)


class AllStudents(UserPassesTestMixin, ListView):
    """Lists All Students In The Database"""
    model = Student
    context_object_name = 'students'
    template_name = 'dashboard/school-admin/all-students.html'
    paginate_by = 10
    ordering = 'matric_number'

    def test_func(self):
        """Allows Only The School Admin To See This Page"""
        return lambda user: not user.is_anonymous and user.schooladmin.schooladmin_access

    def get_queryset(self):
        try:
            matric_number = self.request.GET['matric_number'].upper()
            print(matric_number)
        except:
            matric_number = ''

        if (matric_number != ''):
            object_list = self.model.objects.filter(matric_number = matric_number)
        else:
            object_list = self.model.objects.all()
        return object_list


# Decorator that allows only the School Admin to see this page
@user_passes_test(lambda user: not user.is_anonymous and user.schooladmin.schooladmin_access, login_url='lecturer-admin-login')
def update_student(request, pk):
    """Updates The Student's Information In The Database"""
    student     = get_object_or_404(Student, pk = pk)
    userform    = UpdateUserForm(request.POST or None, instance = student.user)
    studentinfo = StudentForm(data = request.POST or None, files = request.FILES or None, instance=student)
      
    if request.method == "POST":
        userform = UpdateUserForm(request.POST, instance = student.user) 
        studentinfo = StudentForm(data=request.POST, files=request.FILES, instance = student)
        if userform.is_valid() and studentinfo.is_valid():
            userform.save(commit=False)
            userform.username = userform.cleaned_data['username'].lower()
            userform.save()    

            studentinfo.save(commit=False)
            studentinfo.save()

            if studentinfo.cleaned_data['gender'] == "female":               
                messages.success(request, f"Mrs/Miss {userform.cleaned_data['first_name']}'s Account Has Been Updated") 

            elif studentinfo.cleaned_data['gender'] == 'male':
                messages.success(request, f"Mr {userform.cleaned_data['first_name']}'s Account Has Been Updated") 

            else:
                 messages.success(request, f"Account Updated") 

    context = {'userform'   : userform, 
               'studentinfo': studentinfo,
               'student'    : student,
               }    
    return render(request, 'dashboard/school-admin/update-student.html', context)


@user_passes_test(lambda user: not user.is_anonymous and user.schooladmin.schooladmin_access, login_url='lecturer-admin-login')
def delete_student(request, pk):
    """Deletes The Student Data From The Database"""
    student = Student.objects.get(pk=pk)
    print(request.POST)
    if request.method == 'POST':
        student.delete()
        messages.success(request, "Account Deleted") 
        redirect('all-students')
    return render(request, 'dashboard/school-admin/delete-student.html', {'student' : student})


@user_passes_test(lambda user: not user.is_anonymous and user.student.student_access, login_url='student-login')
def student_course_registration(request):
    """Allows The Student To Register Their Courses"""
    student = Student.objects.get(user = request.user)
    try:
        student_courses = CourseTaken.objects.get(student = student)
    except ObjectDoesNotExist:
        student_courses = None

    if student_courses:
        form = CourseTakenForm(request.POST, instance= student_courses)
    else:
        form = CourseTakenForm(request.POST or None)
    if request.method == "POST":
        
        # Update The Courses Registered
        if student_courses:
            if form.is_valid():
                print(form.cleaned_data)
                student_courses.course.clear()
                for course in form.cleaned_data['course']:
                    student_courses.course.add(course)
                student_courses.student = student
                student_courses.save()
                messages.success(request, "Courses Registration Updated")

        # Student Registering The Courses For The First Time
        else:
            form = CourseTakenForm(request.POST)
            print(request.POST)
            if form.is_valid(): 
                print(form.cleaned_data)
                course_taken = CourseTaken.objects.create(student = student)
                course_taken.save()
                for course in form.cleaned_data['course']:
                    course_taken.course.add(course)
                messages.success(request, "Courses Registered")
    
    context = {
        'form' :form,
        'student' : student,
    }

    return render(request, "dashboard/student/course_registration.html", context)


@user_passes_test(lambda user: not user.is_anonymous and user.schooladmin.schooladmin_access, login_url='lecturer-admin-login')
def create_lecturer(request):
    """Function To Create Lecturer"""
    userform = SignUpForm()
    lecturer_info_form = LecturerForm()
    
    if request.method == "POST":
        userform = SignUpForm(request.POST)
        lecturer_info_form = LecturerForm(data=request.POST, files=request.FILES)
        if userform.is_valid() and lecturer_info_form.is_valid():
            userform.save(commit=False)
            userform.is_staff = True
            userform.username = userform.cleaned_data['username'].lower()
            userform.save()

            lecturer = User.objects.get(username = userform.cleaned_data['username'])
            lecturer_info_form.save(commit=False)
            Lecturer.objects.create(user=lecturer, 
                                    date_of_birth = lecturer_info_form.cleaned_data['date_of_birth'], 
                                    gender        = lecturer_info_form.cleaned_data['gender'], 
                                    department    = lecturer_info_form.cleaned_data['department'], 
                                    position      = lecturer_info_form.cleaned_data['position'],
                                    phone_number  = lecturer_info_form.cleaned_data['phone_number'],
                                    profile_pic   = lecturer_info_form.cleaned_data['profile_pic']
                                     )
            lecturer = Lecturer.objects.get(user__username = userform.cleaned_data['username'].lower())
            lecturer.user.is_staff = True
            lecturer.save()
            print(lecturer)
            print(lecturer.user.is_staff)
            messages.success(request, "Lecturer created")   

    context = {'userform': userform, 
               'lecturerinfo': lecturer_info_form
              }   
    return render(request, 'dashboard/school-admin/create-lecturer.html', context)


class AllLecturers(UserPassesTestMixin, ListView):
    """Lists All Lecturers In The Database"""
    model = Lecturer
    context_object_name = 'lecturers'
    template_name = 'dashboard/school-admin/all-lecturers.html'
    paginate_by = 10
    ordering = "user__username"

    def test_func(self):
        return lambda user: not user.is_anonymous and user.schooladmin.schooladmin_access

    def get_queryset(self):
        try:
            username = self.request.GET['username']
        except:
            username = ''

        if (username != ''):
            object_list = self.model.objects.filter(user__username = username)
        else:
            object_list = self.model.objects.all()
        return object_list

    


@user_passes_test(lambda user: not user.is_anonymous and user.schooladmin.schooladmin_access, login_url='lecturer-admin-login')
def update_lecturer(request, pk):
    """Function That Updates The Lecturer's Information"""

    lecturer    = get_object_or_404(Lecturer, pk = pk)
    userform    = UpdateUserForm(request.POST or None, instance = lecturer.user)
    
    lecturer_info_form = LecturerForm(data = request.POST or None, files = request.FILES or None, instance=lecturer)
        
    if request.method == "POST":
        userform = UpdateUserForm(request.POST, instance=lecturer.user)
        lecturer_info_form = LecturerForm(data=request.POST, files=request.FILES, instance=lecturer)        

        if userform.is_valid() and lecturer_info_form.is_valid():
            userform.save(commit=False)
            userform.username = userform.cleaned_data['username'].lower()
            userform.save()

            lecturer_info_form.save() 

            if lecturer_info_form.cleaned_data['gender'] == "female":               
                messages.success(request, f"Mrs/Miss {lecturer.user.first_name}'s Account Has Been Updated") 

            elif lecturer_info_form.cleaned_data['gender'] == 'male':
                messages.success(request, f"Mr {lecturer.user.first_name}'s Account Has Been Updated") 

            else:
                 messages.success(request, f"Account Updated") 

    context = {'userform'    : userform, 
               'lecturerinfo': lecturer_info_form,
               'lecturer'    : lecturer,
               }   
              
    return render(request, 'dashboard/school-admin/update-lecturer.html', context)


@user_passes_test(lambda user: not user.is_anonymous and user.schooladmin.schooladmin_access, login_url='lecturer-admin-login')
def delete_lecturer(request, pk):
    """Deletes The Lecturer From The Database"""
    lecturer = Lecturer.objects.get(pk=pk)
    if request.method == 'POST':
        lecturer.delete()
        messages.success(request, "Account Deleted") 
        redirect('all-lecturers')

    return render(request, 'dashboard/school-admin/delete-lecturer.html', {'lecturer' : lecturer})


@user_passes_test(lambda user: not user.is_anonymous and user.schooladmin.schooladmin_access, login_url='lecturer-admin-login')
def create_schooladmin(request):
    """Function To Create School Admin"""
    userform = SignUpForm()
    schooladmininfo = SchoolAdminForm()
      
    if request.method == "POST":
        userform = SignUpForm(request.POST)
        schooladmininfo = SchoolAdminForm(data=request.POST, files=request.FILES)
        if userform.is_valid() and schooladmininfo.is_valid():
            userform.save(commit=False)
            userform.is_superuser = True
            userform.username = userform.cleaned_data['username'].lower()
            userform.save()
        

            schooladmin = User.objects.get(username = userform.cleaned_data['username'])
            schooladmininfo.save(commit=False)
            SchoolAdmin.objects.create(user=schooladmin, 
                                    date_of_birth = schooladmininfo.cleaned_data['date_of_birth'], 
                                    gender        = schooladmininfo.cleaned_data['gender'], 
                                    phone_number  = schooladmininfo.cleaned_data['phone_number'],
                                    profile_pic   = schooladmininfo.cleaned_data['profile_pic']
                                     )
            messages.success(request, "School Admin created")

    context = {'userform': userform, 
               'schooladmininfo': schooladmininfo
               }      
    return render(request, 'dashboard/school-admin/create-schooladmin.html', context)


class AllSchoolAdmin(UserPassesTestMixin, ListView):
    """List All School Admin In The Database"""
    model  = SchoolAdmin
    template_name = 'dashboard/school-admin/all-schooladmins.html'
    context_object_name  = 'schooladmins'
    paginate_by = 10
    ordering = 'user__username'

    def test_func(self):
        return lambda user: not user.is_anonymous and user.schooladmin.schooladmin_access

    def get_queryset(self):
        try:
            username = self.request.GET['username']
        except:
            username = ''

        if (username != ''):
            object_list = self.model.objects.filter(user__username = username)
        else:
            object_list = self.model.objects.all()
        return object_list


@user_passes_test(lambda user: not user.is_anonymous and user.schooladmin.schooladmin_access, login_url='lecturer-admin-login')
def create_course(request):
    """Function To Create Courses"""
    form = CourseForm()
    if request.method == "POST":
        form = CourseForm(request.POST)

        if form.is_valid():
            form.save(commit=False)
            form.course_title = form.cleaned_data['course_title'].lower()
            form.course_code  = form.cleaned_data['course_code'].upper()
            form.save()
            messages.success(request, "Course Created")

    template = 'dashboard/school-admin/create-course.html'
    context = {'form': form}
        
    return render (request, template,  context)


class AllCourses(UserPassesTestMixin, ListView):
    """List Of All Of Courses"""
    model  = Course
    template_name = 'dashboard/school-admin/all-courses.html'
    context_object_name  = 'courses'
    paginate_by = 10
    ordering = 'course_title'

    def test_func(self):
        return lambda user: not user.is_anonymous and user.schooladmin.schooladmin_access
    
    def get_queryset(self):
        try:
            course = self.request.GET['course'].upper()
        except:
            course = ''

        if (course != ''):
            object_list = self.model.objects.filter(course_code = course)
        else:
            object_list = self.model.objects.all()
        return object_list


class UpdateCourse(UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    """Updates Course's Information In The Database"""
    model  = Course
    template_name = 'dashboard/school-admin/update-course.html'
    fields = ('course_title', 'course_code', 'credit_unit', 'lecturer', 'is_elective', 'level', 'department')
    success_message = "Course Updated"
    success_url = '/all-courses'

    def test_func(self):
        return lambda user: not user.is_anonymous and user.schooladmin.schooladmin_access


class DeleteCourse(UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    """Deletes Course From The Database"""
    model = Course
    template_name = 'dashboard/school-admin/delete-course.html'
    success_url = '/all-courses'
    context_object_name = 'course'
    success_message = "Course Deleted"

    def test_func(self):
        return lambda user: not user.is_anonymous and user.schooladmin.schooladmin_access


@user_passes_test(lambda user: not user.is_anonymous and user.schooladmin.schooladmin_access, login_url='lecturer-admin-login')
def lecturer_profile_page(request):
    """Function That Allows Lecturers To View Their Information"""
    lecturer = Lecturer.objects.get(user = request.user)
    lecturer_courses = request.user.lecturer.course_set.all()
    context  = {
        'lecturer' : lecturer,
        'courses'  : lecturer_courses,
    }

    return render(request, 'dashboard/lecturer/profile.html', context)


@user_passes_test(lambda user: not user.is_anonymous and user.schooladmin.schooladmin_access, login_url='lecturer-admin-login')
def admin_profile_page(request):
    """Function That Allows School Admin To View Their Information"""
    admin = SchoolAdmin.objects.get(user = request.user)

    context  = {
        'admin' : admin,
    }

    return render(request, 'dashboard/school-admin/profile.html', context)


@user_passes_test(lambda user: not user.is_anonymous and user.student.student_access, login_url='student-login')
def student_profile_page(request):
    """Function That Allows Student To View Their Information"""
    student = Student.objects.get(user = request.user)
    
    context  = {
        'student' : student,
    }
    return render(request, 'dashboard/student/profile.html', context)


def student_logout(request):
    """Logouts Student From The System"""
    logout(request)
    return redirect('student-login')


def lecturer_admin_logout(request):
    """Logouts Lecturer And School Admin From The System"""
    logout(request)
    return redirect('lecturer-admin-login')







