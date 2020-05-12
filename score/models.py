from django.db import models
from dashboard.models import Student, Course


# Create your models here.
class G1(models.Model):
    """This Model Represents The G1 Score Of The Student"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.student} {self.course}'


class G2(models.Model):
    """This Model Represents The G2 Score Of The Student"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.student} {self.course}'


class G3(models.Model):
    """This Model Represents The G3 Score Of The Student"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.student} {self.course}'


class G3_prediction(models.Model):
    """This Model Represents The Prediction Of G3 Score Of The Student"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    # category = models.CharField(max_length=4, default='pass')
    group = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return f'{self.student} {self.course}'

    class Meta:
        unique_together = ('student', 'course')

    # def save(self, *args, **kwargs):
    #     if self.score <= 10:
    #         self.group = 'fail'
    #     else:
    #         self.group = 'pass'
    #     super(G3_prediction, self).save(*args, **kwargs)
    
    # def save(self, *args, **kwargs): 
    #     """Slugifies The Course Title Before Saving The Object"""
    #     self.slug = slugify(self.course_title) 
    #     super(Course, self).save(*args, **kwargs) 