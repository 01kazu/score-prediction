from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('dashboard/', views.home, name='home'),
    path('create-student', views.create_student, name='create-student' ),
    path('all-students', views.AllStudents.as_view(), name='all-students'),
    path('delete-student/<pk>', views.delete_student, name='delete-student'),
    path('update-student/<pk>', views.update_student, name='update-student'),
    path('course-registration/', views.student_course_registration, name='course-reg'),

    path('create-lecturer', views.create_lecturer, name='create-lecturer'),
    path('all-lecturers', views.AllLecturers.as_view(), name='all-lecturers'),
    path('delete-lecturer/<pk>', views.delete_lecturer, name='delete-lecturer'),
    path('update-lecturer/<pk>', views.update_lecturer, name='update-lecturer'),

    path('create-schooladmin', views.create_schooladmin, name='create-schooladmin'),
    path('all-schooladmins', views.AllSchoolAdmin.as_view(), name='all-schooladmins'),

    path('all-courses', views.AllCourses.as_view(), name='all-courses'),
    path('create-course', views.create_course, name='create-course'),
    path('delete-course/<pk>', views.DeleteCourse.as_view(), name='delete-course'),
    path('update-course/<pk>', views.UpdateCourse.as_view(), name='update-course'),

    path('lecturer/profile', views.lecturer_profile_page, name="lecturer-profile-page"),
    path('admin/profile', views.admin_profile_page, name="admin-profile-page"),
    path('student/profile', views.student_profile_page, name='student-profile-page'),
    
   
    path('', views.student_login, name='student-login'),
    path('login', views.lecturer_admin_login, name='lecturer-admin-login'),
    path('logout', views.student_logout, name='student-logout'),
    path('user-logout', views.lecturer_admin_logout, name='lecturer-admin-logout'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="dashboard/accounts/password_reset_form.html"), 
        name='password_reset', ), 
    path( 'password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="dashboard/accounts/password_reset_done.html"), 
        name='password_reset_done', ), 
    path( 'reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="dashboard/accounts/user_password_reset.html"), name='password_reset_confirm', ), 
    path( 'reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="dashboard/accounts/password_reset_complete.html"), 
        name='password_reset_complete', ),
    path('password-change/',auth_views.PasswordChangeView.as_view(template_name="dashboard/accounts/password_change.html"), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(template_name="dashboard/accounts/password_change_done.html"), name="password_change_done"),

]

