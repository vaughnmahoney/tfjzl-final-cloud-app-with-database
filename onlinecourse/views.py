from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .models import Course, Enrollment, Submission, Question, Choice

class CourseListView(generic.ListView):
    template_name = 'onlinecourse/course_list.html'
    context_object_name = 'course_list'

    def get_queryset(self):
        return Course.objects.order_by('-pub_date')[:5]

class CourseDetailsView(generic.DetailView):
    model = Course
    template_name = 'onlinecourse/course_details_bootstrap.html'

def submit(request, course_id):
    model = Course
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        submission = Submission(enrollment=Enrollment.objects.filter(course=course).first())
        submission.save()
        
        question_ids = [q.id for q in course.question_set.all()]
        for q_id in question_ids:
            choice_ids = request.POST.getlist(f"choice_{q_id}")
            for c_id in choice_ids:
                try:
                    choice = Choice.objects.get(pk=c_id)
                    submission.choices.add(choice)
                except Choice.DoesNotExist:
                    pass
        
        submission.save()
        return render(request, 'onlinecourse/exam_result_bootstrap.html', {'course': course, 'submission': submission, 'test': True}) \
            if not submission.pk else redirect('onlinecourse:show_exam_result', course_id=course.id, submission_id=submission.id)
    return render(request, 'onlinecourse/course_details_bootstrap.html', {'course': course})

def show_exam_result(request, course_id, submission_id):
    context = {}
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    context['course'] = course
    context['submission'] = submission
    
    # Calculate score
    grade = 0
    possible_grade = 0
    for question in course.question_set.all():
        possible_grade += question.grade
        selected_ids = [c.id for c in submission.choices.filter(question=question)]
        if question.is_get_score(selected_ids):
            grade += question.grade
            
    context['grade'] = grade
    context['possible'] = possible_grade
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
