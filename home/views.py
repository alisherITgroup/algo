from django.shortcuts import render
from django.views import generic
from django.contrib.auth.models import User
from problems.models import ArchiveProblem
from home.models import TimeLine
from problems.models import ArchiveProblem
from posts.models import Post
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy


class HomeView(generic.TemplateView):
    template_name = "home/home.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["homestatus"] = "active"
        users_count = User.objects.all().count()
        problems_count = ArchiveProblem.objects.all().count()
        posts_count = Post.objects.all().count()
        teachers_count = User.objects.all().filter(isTeacher=True).count()
        context["users_count"] = users_count
        context["problems_count"] = problems_count
        context["posts_count"] = posts_count
        context["teachers_count"] = teachers_count
        return context

@login_required(login_url="login")
def ProfileView(request, username):
    problems = ArchiveProblem.objects.all()
    profile = User.objects.all().filter(username=str(username)).first()
    timeline = TimeLine.objects.all().filter(author=profile).order_by("-id")
    return render(request, "home/profile.html", {"profile": profile, "problems": problems, "timelines": timeline})


class UsersView(LoginRequiredMixin, generic.ListView):
    model = User
    template_name = "home/users.html"
    context_object_name = "users"
    paginate_by = 50
    ordering = ['-rating']
    login_url = reverse_lazy("login")

    def get_context_data(self, *args, **kwargs):
        username = self.request.GET.get("search")
        city = self.request.GET.get("city")
        town = self.request.GET.get("town")
        if username:
            pass
        else:
            username = ""
        if city:
            pass
        else:
            city = ""
        if town:
            pass
        else:
            town = ""
        context = super().get_context_data(*args, **kwargs)
        try:
            active = int(self.request.GET.get("page"))
        except:
            active = 1
        context["username"] = username
        context["city"] = city
        context["town"] = town
        context["check"] = not username and not city and not town
        if len(username) > 0 or len(city) > 0 or len(town) > 0:
            if len(city) > 0 and len(town) == 0 and len(username) == 0:
                context["users"] = User.objects.all().filter(city__icontains=city)
            elif len(city) > 0 and len(town) > 0 and len(username) == 0:
                context["users"] = User.objects.all().filter(city__icontains=city, town__icontains=town)
            elif len(username) > 0 and len(town) == 0 and len(city) == 0:
                context["users"] = User.objects.all().filter(username__icontains=username)
            elif len(city) > 0 and len(town) == 0 and len(username) > 0:
                context["users"] = User.objects.all().filter(city__icontains=city, username__icontains=username)
            elif len(city) > 0 and len(town) > 0 and len(username) > 0:
                context["users"] = User.objects.all().filter(city__icontains=city, username__icontains=username, town__icontains=town)
        context['num_pages'] = generic.ListView.paginator_class(User.objects.all().filter(username__icontains=username), 50).num_pages * "a"
        context["active"] = int(active)
        context["last"] = len(context["num_pages"])
        context["userstatus"] = "active"
        return context
