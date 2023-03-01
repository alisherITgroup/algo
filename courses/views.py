from django.shortcuts import render
from django.views import generic
from .models import Course, CourseRating, Lesson, LessonComment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import CourseForm
from django.urls import reverse_lazy

class CourseCreateView(LoginRequiredMixin, generic.CreateView):
    model = Course
    form_class = CourseForm
    template_name = "courses/create.html"
    login_url = reverse_lazy("login")

class CourseEditView(LoginRequiredMixin, generic.UpdateView):
    model = Course
    form_class = CourseForm
    template_name = "courses/update.html"
    login_url = reverse_lazy("login")

class CourseDetailView(generic.DetailView):
    model = Course
    template_name = "courses/course.html"
    context_object_name = "course"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        course = Course.objects.get(id=int(self.kwargs["pk"]))
        lessons = Lesson.objects.all().filter(course=course)
        context["lessons"] = lessons
        context["coursestatus"] = "active"
        return context

class CoursesListView(generic.ListView):
    model = Course
    template_name = "courses/courses.html"
    context_object_name = "courses"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["coursestatus"] = "active"
        return context
@login_required(login_url="login")
def LessonDetailView(request, pk, integer):
    lesson = Lesson.objects.get(id=int(integer))
    return render(request, "courses/lesson.html", {"lesson": lesson})

