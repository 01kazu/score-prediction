from django.contrib import admin
from .models import SchoolAdmin, Lecturer, Student, Course, CourseTaken

admin.site.register(SchoolAdmin)
admin.site.register(Lecturer)
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(CourseTaken)
