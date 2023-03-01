from django.shortcuts import render
from django.views import generic
from .models import Problem, Category
from django.contrib.auth.models import User
from .forms import ProblemForm
from django.http import HttpResponseRedirect
from django.contrib.messages import constants
from django.urls import reverse
from problems.models import ArchiveProblem
from django.shortcuts import get_object_or_404
from django.contrib import messages
import json, requests
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from attempts.models import Attempt2
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


class ProblemCreateView(LoginRequiredMixin, generic.CreateView):
    model = Problem
    form_class = ProblemForm
    template_name = "problemsets/create.html"
    login_url = reverse_lazy("login")

    def form_invalid(self, form):
        messages.add_message(self.request, constants.ERROR, "Iltimos kerakli maydonlarni to'ldiring!")
        return super().form_invalid(form)
    def form_valid(self, form):
        messages.add_message(self.request, constants.SUCCESS, "Masala yaratish muvaffaqqiyatli amalga oshirildi!")
        return super().form_valid(form)

class ProblemUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Problem
    form_class = ProblemForm
    template_name = "problemsets/update.html"
    login_url = reverse_lazy("loginawu")

    def form_invalid(self, form):
        messages.add_message(self.request, constants.ERROR, "Iltimos kerakli maydonlarni to'ldiring!")
        return super().form_invalid(form)
    def form_valid(self, form):
        messages.add_message(self.request, constants.SUCCESS, "Masala muvaffaqqiyatli tahrirlandi!")
        return super().form_valid(form)

@login_required(login_url="login")
def ProblemSetView(request, author):
    user = User.objects.all().filter(username__startswith=str(author)).first()
    problems = Problem.objects.all().filter(author=user)
    return render(request, "problemsets/problems.html", {"problems": problems})

@login_required(login_url="login")
def ProblemView(request, string):
    problem = Problem.objects.get(nanoid=str(string))
    attempts = Attempt2.objects.all().filter(problem=problem)
    return render(request, "problemsets/problem.html", {"problem": problem, "attempts": attempts})

@login_required(login_url="login")
def archive(request, pk, username):
    author = User.objects.get(id=int(request.user.id))
    category = Category.objects.all()
    problem = get_object_or_404(Problem, id=request.POST.get("problem_id"))
    ArchiveProblem.objects.create(
        author=author,
        name=problem.name,
        problem=problem.problem,
        timelimit = problem.timelimit,
        memorylimit=problem.memorylimit,
        difficulty=problem.difficulty,
        comment=problem.comment,
        infoin=problem.infoin,
        infoout=problem.infoout,
        simpletests=problem.simpletests,
        tests=problem.tests,
    )
    problem.isArchive = True
    problem.save()
    messages.add_message(request,constants.SUCCESS, "Masala arxivga muvaffaqqiyatli qo'shildi!")
    return HttpResponseRedirect(reverse("problemsets", args=[str(username)]))
    
@login_required(login_url="login")
def send2(request, pk:int):
    data = dict(request.POST)
    url = "http://algorithmshubapi.pythonanywhere.com/submit/code/"
    status = ""
    time = 0
    code = ""
    language = ""
    output = ""
    action_tests = []
    problem = Problem.objects.get(id=pk)
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
            # print("--->", post_to_api)
            if(str(post_to_api["output"]) == tests[i]):
                if time > float(problem.timelimit):
                    status = f"TimeLimit({index})"
                    output = ""
                    mcode = constants.ERROR
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
                output = ""
                mcode = constants.SUCCESS
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
                    output = post_to_api["output"]
                    mcode = constants.ERROR
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
                    output = ""
                    mcode = constants.ERROR
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
                    mcode = constants.ERROR
                    break
        messages.add_message(request, mcode, status)
        Attempt2.objects.create(
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
        return HttpResponseRedirect(reverse('problemset', args=[problem.nanoid]))
    return render(request, "attempts/attempt.html", {
        "status": status,
        "problem": problem,
        "tests": list(tests)
    })
