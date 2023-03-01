from django.shortcuts import render
from django.urls import reverse_lazy
from .models import ArchiveProblem
from django.views import generic
from .forms import ArchiveProblemForm
from problemsets.models import Category
from django.contrib.messages import constants
from django.contrib import messages
from attempts.models import Attempt
import json
import re
from home.models import TimeLine
import requests
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

class ArchiveProblemsView(generic.ListView):
    model = ArchiveProblem
    template_name = "problems/problems.html"
    context_object_name = "problems"
    paginate_by = 20

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        categories = Category.objects.all().count()
        category = self.request.GET.get("category")
        difficulty = self.request.GET.get("difficulty")
        sort = self.request.GET.get("sort")
        if sort == "off":
            sort = "down"
            context["bool"] = "down"
            context["boolicon"] = "fas fa-angle-double-down"
            context["problems"] = ArchiveProblem.objects.all()
        elif sort == "down":
            sort = "up"
            context["bool"] = "up"
            context["boolicon"] = "fas fa-angle-double-up"
            context["problems"] = ArchiveProblem.objects.all().order_by('difficulty')
        elif sort == "up":
            sort = "off"
            context["bool"] = "off"
            context["boolicon"] = "fas fa-equals"
            context["problems"] = ArchiveProblem.objects.all().order_by('-difficulty')
        if category:
            category = int(category)
        else:
            category = ""
        if difficulty:
            difficulty = int(difficulty)
        else:
            difficulty = "a"
        try:
            active = int(self.request.GET.get("page"))
        except:
            active = 1
        if category != "" or difficulty != "a":
            context["problems"] = ArchiveProblem.objects.all().filter(category__in=[category] if category else [i for i in range(1, categories+1)], difficulty__lte=difficulty if isinstance(difficulty, int) else 100, difficulty__gte=difficulty if isinstance(difficulty, int) else 0)
        context['num_pages'] = generic.ListView.paginator_class(ArchiveProblem.objects.all(), 20).num_pages * "a"
        context["active"] = int(active)
        context["problemstatus"] = "active"
        context["last"] = len(context["num_pages"])
        context["check"] = (category == "" and difficulty == "a")
        return context

class ArchiveProblemView(generic.DetailView):
    model = ArchiveProblem
    template_name = "problems/problem.html"
    context_object_name = "problem"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        problem = ArchiveProblem.objects.get(id=self.kwargs["pk"])
        try:
            attempts = Attempt.objects.all().filter(problem=problem, author=self.request.user).order_by('-id')
        except:
            attempts = None
        context["attempts"] = attempts
        return context

class ArchiveProblemCreateView(LoginRequiredMixin, generic.CreateView):
    model = ArchiveProblem
    form_class = ArchiveProblemForm
    template_name = "problems/create.html"
    login_url = reverse_lazy("login")

    def form_invalid(self, form):
        messages.add_message(self.request, constants.ERROR, "Iltimos kerakli maydonlarni to'ldiring!")
        return super().form_invalid(form)
    def form_valid(self, form):
        messages.add_message(self.request, constants.SUCCESS, "Masala yaratish muvaffaqqiyatli amalga oshirildi!")
        return super().form_valid(form)

class ArchiveProblemUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = ArchiveProblem
    form_class = ArchiveProblemForm
    template_name = "problems/update.html"
    success_url = reverse_lazy("problems")
    login_url = reverse_lazy("login")

    def form_invalid(self, form):
        messages.add_message(self.request, constants.ERROR, "Iltimos kerakli maydonlarni to'ldiring!")
        return super().form_invalid(form)
    def form_valid(self, form):
        messages.add_message(self.request, constants.SUCCESS, "Masala muvaffaqqiyatli tahrirlandi!")
        return super().form_valid(form)

@login_required(login_url="login")
def send(request, pk:int):
    data = dict(request.POST)
    url = "http://algorithmshubapi.pythonanywhere.com/submit/code/"
    status = ""
    time = 0
    code = ""
    language = ""
    output = ""
    action_tests = []
    problem = ArchiveProblem.objects.get(id=pk)
    try:
        tests = eval(problem.tests)
    except:
        tests = {"1": "Kechirasiz masala testlarida xatolik bor ekan!"}
    user = request.user
    if request.method == "POST":
        code = data["code"][0]
        language = data["lang"][0]
        count = 0
        for i in tests.keys():
            testin = list(tests.keys())[count]
            data = {
                "code": code,
                "language": language,
                "status": "p",
                "user_input": f"{i}",
                "user": 1
            }
            post_to_api = requests.post(
                url,
                data,
                headers={"Authorization": "Token 3ccc2fda440ec8d03aae3d000127ee23c728f343"},
            ).json()
            time = round(float(post_to_api["time"]), 2)
            if post_to_api["language"] == "c" or post_to_api["language"] == "cpp" or post_to_api["language"] == "java":
                time = (time*1000 - (time*1000)%100)/100000
            if(str(post_to_api["output"]) == tests[i]):
                if time > float(problem.timelimit):
                    status = f"TimeLimit({index})"
                    alert = constants.ERROR
                    output = ""
                    action_tests.append(
                    {
                        "time": f"{time}ms",
                        "test": index,
                        "input": testin,
                        "test_result": tests[i],
                        "your_result": post_to_api['output'],
                        "status": "TimeLimit"
                    }
                )
                    count += 1
                    break
                index = list(tests).index(i) + 1
                time = time
                status = "Accepted"
                alert = constants.SUCCESS
                output = ""
                action_tests.append(
                    {
                        "time": f"{time*1000}ms",
                        "test": index,
                        "input": testin,
                        "test_result": tests[i],
                        "your_result": post_to_api['output'],
                        "status": "Accepted"
                    }
                )
                count += 1
                continue
            else:
                index = list(tests).index(i) + 1
                if post_to_api["status"] == "e":
                    status = f"CompilationError({index})"
                    alert = constants.ERROR
                    output = post_to_api["output"]
                    action_tests.append(
                    {
                        "time": f"{time*1000}ms",
                        "test": index,
                        "input": testin,
                        "test_result": tests[i],
                        "your_result": "error",
                        "status": "CompilationError"
                    }
                )
                    count += 1
                    break
                elif post_to_api["output"] == "TimeLimit":
                    status = f"TimeLimit({index})"
                    alert = constants.ERROR
                    output = ""
                    time = round(float(post_to_api['time']), 2)
                    action_tests.append(
                    {
                        "time": f"{round(float(post_to_api['time']), 2)}ms",
                        "test": index,
                        "input": testin,
                        "test_result": tests[i],
                        "your_result": post_to_api['output'],
                        "status": "TimeLimit"
                    }
                )
                    count += 1
                    break
                else:
                    status = f"WrongAnswer({index})"
                    alert = constants.ERROR
                    action_tests.append(
                    {
                        "time": f"{time*1000}ms",
                        "test": index,
                        "input": testin,
                        "test_result": tests[i],
                        "your_result": post_to_api['output'],
                        "status": "WrongAnswer"
                    }
                )   
                    count += 1
                    break
        messages.add_message(request, alert, status)
        Attempt.objects.create(
            author=user,
            problem=problem,
            code=code,
            time=float(time)*1000,
            language=language,
            output=output,
            status=status,
            cases=action_tests,
            lengthcode=len(code),
            memory=1
            )
        if "Acc" in status:
            try:
                problem.errors.remove(request.user)
            except:
                ...
            solvers = problem.solvers.all()
            isSolver = request.user in solvers
            if not isSolver:
                problem.solvers.add(request.user)
                problem.save()
                request.user.rating += int(problem.difficulty*100-time*1000) if int(problem.difficulty*100-time*1000) > 0 else 10
                request.user.save()
                request.user.coins += int(problem.difficulty)
                request.user.save()
                if int(problem.difficulty*100-time*1000) >= 1000:
                    TimeLine.objects.create(
                        author=request.user,
                        title=f"Ajoyib! Ratingingiz ko'tarilayapti.",
                        body=f"Siz {problem.difficulty}% qiyinchilikdagi masalani {time*1000}ms da yechib, {int(problem.difficulty*100-time*1000)} ballga ega bo'ldingiz. Ratingingiz: {request.user.rating}",
                        status="success",
                        icon="check"
                    )
                if int(problem.difficulty*5) >= 300:
                    TimeLine.objects.create(
                        author=request.user,
                        title=f"Ajoyib! AlgoCoin ingiz ko'payayapti.",
                        body=f"Siz {problem.difficulty}% qiyinchilikdagi masalani {time*1000}ms da yechib, {int(problem.difficulty*5)} AlgoCoin ga ega bo'ldingiz. Hisobingiz: {request.user.coins} AlgoCoin",
                        status="success",
                        icon="check"
                    )
        else:
            res = request.user.rating - abs(int(problem.difficulty*100-time*1000))
            if res < 0:
                request.user.rating = 0
                request.user.save()
            else:
                request.user.rating - abs(int(problem.difficulty*100-time*1000))
                request.user.save()
            solvers = problem.solvers.all()
            isSolver = request.user in solvers
            if request.user.rating < 0:
                TimeLine.objects.create(
                    author=request.user,
                    title=f"Afsus! Ratingingiz tushib ketyabdi.",
                    body=f"Sizning ratingingiz {request.user.rating} ga tushib ketti. Iltimos ratingingizni ko'tarishga harakat qiling.",
                    status="danger",
                    icon="times"
                )
            if not isSolver:
                problem.errors.add(request.user)
                request.user.rating -= int(abs(int(problem.difficulty*100-time*1000))/100)
                request.user.save()
        return HttpResponseRedirect(reverse('problem', args=[problem.id]))
    return render(request, "problems/problem.html", {
        "status": status,
        "problem": problem,
        "tests": list(tests)
    })
