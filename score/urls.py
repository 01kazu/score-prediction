from django.urls import path

from . import views

app_name = "scores"

urlpatterns = [
    path('lecturer-dashboard/', views.dashboard, name='dashboard'),

    path('<course_slug>/g1_score/', views.g1_scores, name='course-g1-score'),

    path('<course_slug>/g2_score/', views.g2_scores, name='course-g2-score'),

    path('<course_slug>/g3_score/', views.g3_scores, name='course-g3-score'),

    path('scores/', views.student_scores, name='student-scores'),

    path('<course_slug>/predictions/', views.g3_predictions, name='predictions'),

]
