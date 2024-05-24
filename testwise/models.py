from django.db import models

# Create your models here.
class InterviewQuestion(models.Model):
  id = models.CharField(max_length = 20, null = False, primary_key = True)
  department_name = models.CharField(max_length = 30, null = False, default='') #科系名稱
  question_text = models.TextField(max_length = 200, null = False, default='') #面試問題內容
  answer_text = models.TextField(max_length = 200, null = False, default='') #問題的建議回答
  def __str__(self):
    return self.id
      
class DepartmentInfo(models.Model):
  id = models.CharField(max_length = 20, null = False, primary_key = True)
  department_name = models.CharField(max_length = 30, null = False, default='') #科系名稱
  compulsory_courses = models.TextField(max_length = 200, null = False, default='') #必修科目
  graduation_requirements = models.TextField(max_length = 150, null = False, default='') #畢業門檻
  def __str__(self):
    return self.id