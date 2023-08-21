from django.contrib import admin
from .models import Polls      # Question, Choice

# Register your models here
@admin.register(Polls)
class PollsAdmin(admin.ModelAdmin):
    list_display = list_display = ['question', 'option1', 'option2', 'option3',]
    search_fields = ['question',]
    list_filter = ['question']

# class ChoiceAdmin(admin.ModelAdmin):
#     list_display = ['option1', 'option2', 'option3', 'option4']

# admin.site.register(Choice, ChoiceAdmin)

# @admin.register(Question)
# class QuestionAdmin(admin.ModelAdmin):
#     list_display = ['question', 'created', 'author', 'status']

