from django.contrib import admin
from .models import Question, Choice, Submission, Course, Lesson, Instructor, Learner

# Register your models here.

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 5


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 5


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ['content']


class LessonAdmin(admin.ModelAdmin):
    list_display = ['title']


class CourseAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ('name', 'pub_date')
    list_filter = ['pub_date']
    search_fields = ['name', 'description']


admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)
