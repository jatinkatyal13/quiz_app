from django.contrib import admin
from .models import Choice, Question, QuestionResult
# Register your models here.

admin.site.register(Choice)
admin.site.register(Question)
admin.site.register(QuestionResult)