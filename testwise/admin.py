from django.contrib import admin
from testwise.models import InterviewQuestion, DepartmentInfo
# Register your models here.

class InterviewQuestionadmin(admin.ModelAdmin):
  list_display = ('id','department_name','question_text','answer_text')
  list_filter = ('id','department_name') #篩選
  search_fields = ('id','department_name') #可搜尋

admin.site.register(InterviewQuestion, InterviewQuestionadmin)

class DepartmentInfoadmin(admin.ModelAdmin):
  list_display = ('id','department_name','compulsory_courses','graduation_requirements')
  list_filter = ('id','department_name') #篩選
  search_fields = ('id','department_name') #可搜尋

admin.site.register(DepartmentInfo, DepartmentInfoadmin)