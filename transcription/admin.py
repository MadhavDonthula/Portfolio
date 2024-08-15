from django.contrib import admin

from .models import Assignment, QuestionAnswer, ClassCode

admin.site.register(Assignment)
admin.site.register(QuestionAnswer)
admin.site.register(ClassCode)