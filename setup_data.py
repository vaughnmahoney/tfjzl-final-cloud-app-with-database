import os
import django

# Setup env if running standalone (not needed if via shell, but good for safety)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.contrib.auth import get_user_model
from onlinecourse.models import Course, Lesson, Question, Choice, Instructor, Enrollment

User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'password123')
    print("Superuser created.")
else:
    print("Superuser already exists.")

admin_user = User.objects.get(username='admin')

# Create Instructor
inst, created = Instructor.objects.get_or_create(user=admin_user, defaults={'total_learners': 0})

# Create Course
c, created = Course.objects.get_or_create(
    name='Django Application Development with SQL and Databases', 
    defaults={
        'description': 'Learn Django',
        'image': 'course_images/django.png'
    }
)
c.instructors.add(inst)
c.save()

# Create Lesson
l1, _ = Lesson.objects.get_or_create(title='Introduction to Django', course=c, content='Django is a web framework.')
l2, _ = Lesson.objects.get_or_create(title='Django Models', course=c, content='Models map to database tables.')

# Create Question 1
q1, _ = Question.objects.get_or_create(course=c, content='What is Django?', grade=50)
Choice.objects.get_or_create(question=q1, content='A web framework', is_correct=True)
Choice.objects.get_or_create(question=q1, content='A video game', is_correct=False)
Choice.objects.get_or_create(question=q1, content='A planet', is_correct=False)

# Create Question 2
q2, _ = Question.objects.get_or_create(course=c, content='Which file is used for URL routing?', grade=50)
Choice.objects.get_or_create(question=q2, content='urls.py', is_correct=True)
Choice.objects.get_or_create(question=q2, content='views.py', is_correct=False)
Choice.objects.get_or_create(question=q2, content='models.py', is_correct=False)

# Create Enrollment
Enrollment.objects.get_or_create(user=admin_user, course=c)

print("Data populated.")
