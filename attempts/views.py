from django.shortcuts import render
from .models import Attempt, Attempt2
from django.views import generic

class AttemptsView(generic.ListView):
    model = Attempt
    template_name = "attempts/attempts.html"
    context_object_name = "attempts"
    paginate_by = 50

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        try:
            active = str(self.request.get_full_path())[list(str(self.request.get_full_path())).index('=')+1::]
        except:
            active = 1
        context['num_pages'] = generic.ListView.paginator_class(Attempt.objects.all(), 50).num_pages * "a"
        context["active"] = int(active)
        context["attemptstatus"] = "active"
        return context

class AttemptView(generic.DetailView):
    model = Attempt
    template_name = "attempts/attempt.html"
    context_object_name = "attempt"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["attemptstatus"] = "active"
        return context

class AttemptsView2(generic.ListView):
    model = Attempt2
    template_name = "attempts/attempts2.html"
    context_object_name = "attempts"

class AttemptView2(generic.DetailView):
    model = Attempt2
    template_name = "attempts/attempt2.html"
    context_object_name = "attempt"