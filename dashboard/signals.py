from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.exceptions import MultipleObjectsReturned

from score.models import G1, G2, G3, G3_prediction
from .models import Student, Course, Lecturer, SchoolAdmin, CourseTaken

from django.utils.text import slugify


@receiver(m2m_changed, sender=CourseTaken.course.through)
def create_student_assessment(sender, instance, action, model, **kwargs):

    if action == "post_add":
        for course in instance.course.all():

            # g1 = G1.objects.filter(course = course)
            student_g1, created = G1.objects.get_or_create(student = instance.student, course = course, )
            if created:
                    student_g1.save() 

            student_g2, created = G2.objects.get_or_create(student = instance.student, course = course, )
            if created:
                    student_g2.save() 

            student_g3, created = G3.objects.get_or_create(student = instance.student, course = course, )
            if created:
                    student_g3.save() 

            student_g3_prediction, created = G3_prediction.objects.get_or_create(student = instance.student, course = course, )
            if created:
                    student_g3_prediction.save()  


        # deletes G1, G2, G3 and G3_predictions objects for courses not registered
        all_student_g1 = G1.objects.filter(student = instance.student)
        all_student_g2 = G2.objects.filter(student = instance.student)
        all_student_g3 = G3.objects.filter(student = instance.student)
        all_student_g3_prediction = G3_prediction.objects.filter(student = instance.student)

        for g1_obj in all_student_g1:
            if not g1_obj.course in instance.course.all(): 
                g1_obj.delete()

        for g2_obj in all_student_g2:
            if not g2_obj.course in instance.course.all(): 
                g2_obj.delete()

        for g3_obj in all_student_g3:
            if not g3_obj.course in instance.course.all(): 
                g3_obj.delete()

        for g3_prediction_obj in all_student_g3_prediction:
            if not g3_prediction_obj.course in instance.course.all(): 
                g3_prediction_obj.delete()
