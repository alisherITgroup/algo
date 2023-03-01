from django.shortcuts import render
from django.views import generic
from .models import Contest, ContestProblem, ContestRating
from .forms import ContestForm, ContestProblemForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from problemsets.models import Problem
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.messages import constants
from attempts.models import ContestAttempt
import requests, datetime, pytz, time
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

@login_required(login_url="login")
def contest_attempt(request, pk, letter, integer):
    attempt = ContestAttempt.objects.get(id=int(integer))
    return render(request, "contests/attempt.html", {"attempt": attempt})

@login_required(login_url="login")
def send_p(request, pk, problem, letter):
    data = dict(request.POST)
    url = "http://algorithmshubapi.pythonanywhere.com/submit/code/"
    status = ""
    time = 0
    code = ""
    language = ""
    output = ""
    action_tests = []
    problem = ContestProblem.objects.get(id=int(problem))
    try:
        tests = eval(problem.tests)
    except:
        tests = {"1": "Kechirasiz masala testlarida xatolik bor ekan!"}
    user = request.user
    if request.method == "POST":
        code = request.POST.get("code")
        language = request.POST.get("lang")
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
                    ms = messages.constants.ERROR
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
                ms = messages.constants.SUCCESS
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
                    ms = messages.constants.ERROR
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
                    ms = messages.constants.ERROR
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
                    ms = messages.constants.ERROR
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
        messages.add_message(request, ms, status)
        contest = Contest.objects.get(id=problem.contest.id)
        ContestAttempt.objects.create(
            author=user,
            problem=problem,
            contest=contest,
            code=code,
            time=float(time)*1000,
            language=language,
            output=output,
            status=status,
            cases=action_tests,
            lengthcode=len(code),
            memory=1
            )
        if "Acc" in status and (request.user not in problem.solvers.all()):
            rating = None
            rating = ContestRating.objects.get(author=request.user, contest=contest)
            if rating:
                stat = eval(str(rating.status))
                if isinstance(stat, dict):
                    try:
                        count = int(stat[f"{letter}"])
                    except:
                        count = -1
                    stat[f"{letter}"] = f"{count+1}"
                    stat[f"status{letter}"] = "acc"
                else:
                    stat = {}
                    count = -1
                    stat[f"{letter}"] = f"{stat}"
                    stat = str(stat)
                rating.rating += problem.difficulty*100-time*1000
                rating.status = stat
                rating.save()
            try:
                problem.errors.remove(request.user)
            except:
                pass
            problem.solvers.add(request.user)
        elif ("W" in status or "T" in status or "C" in status) and request.user not in problem.errors.all():
            rating = None
            rating = ContestRating.objects.get(author=request.user, conntest=contest)
            if rating:
                stat = eval(rating.status)
                if isinstance(stat, dict):
                    try:
                        count = int(stat[f"{letter}"])
                    except:
                        count = -1
                    h = None
                    try:
                        h = stat[f"status{letter}"]
                    except:
                        h = None
                    if not h:
                        stat[f"{letter}"] = f"{count+1}"
                else:
                    stat = {}
                    count = -1
                    stat[f"{letter}"] = f"{stat}"
                    stat = str(stat)
                rating.status = stat
                rating.rating -= problem.difficulty
                if rating.rating >= 0:
                    pass
                else:
                    rating.rating = 0
                rating.save()
            problem.errors.add(request.user)
        elif ("W" in status or "T" in status or "C" in status):
            rating = None
            rating = ContestRating.objects.get(author=request.user, contest=contest)
            if rating:
                stat = eval(rating.status)
                if isinstance(stat, dict):
                    try:
                        count = int(stat[f"{letter}"])
                    except:
                        count = -1
                    h = None
                    try:
                        h = stat[f"status{letter}"]
                    except:
                        h = None
                    if not h:
                        stat[f"{letter}"] = f"{count+1}"
                else:
                    stat = {}
                    count = 0
                    stat[f"{letter}"] = f"{stat}"
                    stat = str(stat)
                rating.status = stat
                rating.rating -= problem.difficulty*10
                if rating.rating >= 0:
                    pass
                else:
                    rating.rating = 0
                rating.save()
        return HttpResponseRedirect(reverse('contest_problem', args=[int(pk), str(letter)]))
    return render(request, "contests/contest.html", {
        "status": status,
        "problem": problem,
        "tests": list(tests)
    })


class CreateContestView(LoginRequiredMixin, generic.CreateView):
    model = Contest
    form_class = ContestForm
    template_name = "contests/create.html"
    login_url = reverse_lazy("login")

    def form_invalid(self, form):
        return super().form_invalid(form)

class EditContestView(LoginRequiredMixin, generic.UpdateView):
    model = Contest
    form_class = ContestForm
    template_name = "contests/edit.html"
    login_url = reverse_lazy("login")

    def form_invalid(self, form):
        print(form.errors.as_data)
        return super().form_invalid(form)
    def get_success_url(self) -> str:
        return reverse("contest", args=[self.kwargs['pk']])
    
class EditContestProblemView(LoginRequiredMixin, generic.UpdateView):
    model = ContestProblem
    form_class = ContestProblemForm
    template_name = "contests/problem_edit.html"
    login_url = reverse_lazy("login")
    context_object_name = "problem"

    def form_invalid(self, form):
        return super().form_invalid(form)
    def get_success_url(self) -> str:
        return reverse_lazy("contests")

class ContestView(LoginRequiredMixin, generic.DetailView):
    model = Contest
    template_name = "contests/contest.html"
    login_url = reverse_lazy("login")

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        user = User.objects.get(id=int(self.request.user.id))
        problemset = Problem.objects.all().filter(author=user, isContest=False)
        contest = Contest.objects.get(id=self.kwargs["pk"])
        problems = ContestProblem.objects.all().filter(contest=contest)
        context["letter"] = "A"
        langs = ""
        for lang in contest.langs.all():
            langs += f"<span class='badge rounded-pill badge-soft-info'>{lang.name}</span>" +" "
        authors = ""
        for author in contest.authors.all():
            authors += author.username + " "
        context["problems"] = problemset
        context["problems_count"] = problems.count()
        context["users_count"] = contest.users.count()
        context["langs"] = langs
        context["authors"] = authors
        context["cproblems"] = problems

        startdate = contest.startdate.split("-")
        starttime = contest.starttime.split(":")
        startmonth = int(startdate[-2])
        startday = int(startdate[-1])
        starthour = int(starttime[0])
        startminute = int(starttime[1])

        enddate = contest.enddate.split("-")
        endtime = contest.endtime.split(":")
        endmonth = int(enddate[-2])
        endday = int(enddate[-1])
        endhour = int(endtime[0])
        endminute = int(endtime[1]) 

        now = datetime.datetime.now()
        nowdate = str(now.date()).split("-")
        nowtime = str(now.time()).split(":")
        month = int(nowdate[-2])
        day = int(nowdate[-1])
        hour = int(nowtime[0])
        minute = int(nowtime[1])
        constat = "notstarted"
        
        if startmonth > month:
            constat = "notstarted"
            contest.isContinued = constat
            contest.save()
        elif startmonth < month:
            constat = "ended"
            contest.isContinued = constat
            contest.save() 
        else:
            if startday > day: # boshlanish kuni hozirgi kundan katta.
                constat = "notstarted" 
                contest.isContinued = constat
                contest.save()
            elif startday < day: # boshlanish kuni hozirgi kundan kichik
                if endday < day: # tugash kuni hozirgi kundan kichik
                    constat = "ended"
                    contest.isContinued = constat
                    contest.save()
                elif endday > day: # tugash kuni hozirgi kundan katta
                    constat = "started"
                    contest.isContinued = constat
                    contest.save()
                else: # agar ular teng bulsa
                    if hour > endhour:  # agar hozirgi soat tugash soatidan katta
                        constat = "ended"
                        contest.isContinued = constat
                        contest.save()
                    elif hour == endhour: # agar soatlar teng bulsa
                        if minute > endminute: # agar minute tugash minutidan katta bulsa
                            constat = "ended"
                            contest.isContinued = constat
                            contest.save()
                        else: # agar minute tugash minutidan kichik bulsa
                            constat = "started"
                            contest.isContinued = constat
                            contest.save()
                    else: # aks holda
                        constat = "started"
                        contest.isContinued = constat
                        contest.save()
            else: # startday hozir ga teng.
                if hour < starthour: # agar soat boshlanishidan kichik bulsa
                    constat = "notstarted"
                    contest.isContinued = constat
                    contest.save()
                else: # starthour <= hour
                    if starthour < hour: # agar boshlanishi hozirdan kichik va tugashi katta bulsa
                        if endday == day:
                            if startminute > minute:
                                constat = "notstarted"
                                contest.isContinued = constat
                                contest.save()
                            elif startminute <= minute and endminute >= minute:
                                constat = "started"
                                contest.isContinued = constat
                                contest.save()
                        elif endday > day:
                            constat = "started"
                            contest.isContinued = constat
                            contest.save()
                        if starthour < hour and endhour < hour:
                            constat = "ended"
                            contest.isContinued = constat
                            contest.save()
                        else:
                            constat = "started"
                            contest.isContinued = constat
                            contest.save()
                    else:
                        if starthour == hour:
                            if startminute <= minute:
                                constat = 'started'
                                contest.isContinued = constat
                                contest.save()   
                        else:
                            constat = 'notstarted'
                            contest.isContinued = constat
                            contest.save()
        users = contest.users.all()
        if self.request.user in users:
            isAbonent = True
        else:
            isAbonent = False
        context["isAbonent"] = isAbonent
        context["constat"] = constat
        context["conteststatus"] = "active"
        return context

@login_required(login_url="login")
def ContestProblemView(request, pk, problem):
    contest = Contest.objects.get(id=int(pk))
    names = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    count = ContestProblem.objects.all().filter(contest=contest).count()
    letters = names[:count:]
    problems = list(ContestProblem.objects.all().filter(contest=contest))
    problemm = problems[ord(str(problem))-65]
    attempts = ContestAttempt.objects.all().filter(contest=contest, author=request.user, problem=problemm)
    return render(request, "contests/contest_problem.html", {"problem": problemm, "letter": problem, "letters": letters, "attempts": attempts, "conteststatus": "active"})

@login_required(login_url="login")
def AddProblemToContest(request, pk):
    if request.method == "POST":
        problems = list(map(int, list(request.POST)[1::]))
        contest = Contest.objects.get(id=int(pk))
        author = User.objects.get(id=int(request.user.id))
        for id_ in problems:
            problem = Problem.objects.get(id=id_)
            ContestProblem.objects.create(
                nanoid="1",
                contest=contest,
                author=author,
                name=problem.name,
                problem=problem.problem,
                timelimit=problem.timelimit,
                memorylimit=problem.memorylimit,
                difficulty=problem.difficulty,
                infoin=problem.infoin,
                infoout=problem.infoout,
                comment=problem.comment,
                simpletests=problem.simpletests,
                tests=problem.tests,
                solution=problem.solution
            )
            problem.isContest = True
            problem.save()
        messages.add_message(request, constants.SUCCESS, "Masalalar muvaqqiyatli qo'shildi")
    user = User.objects.get(id=int(request.user.id))
    problemset = Problem.objects.all().filter(author=user)
    return HttpResponseRedirect(reverse("contest", args=[str(pk)]))

class ContestProblemCreateView(LoginRequiredMixin, generic.CreateView):
    model = ContestProblem
    form_class = ContestProblemForm
    template_name = "contests/create_problem.html"
    login_url = reverse_lazy("login")

    def get_success_url(self):
        return reverse("contest", args=[self.kwargs['pk']])

    def form_invalid(self, form):
        return super().form_invalid(form)
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        contest = Contest.objects.get(id=int(self.kwargs['pk']))
        context["contest"] = contest
        context["conteststatus"] = "active"
        return context

class ContestsView(LoginRequiredMixin, generic.ListView):
    model = Contest
    template_name = "contests/contests.html"
    context_object_name = "contests"
    login_url = reverse_lazy("login")

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        cons = Contest.objects.all().filter(isContinued__in=['started', 'notstarted']).order_by('-id')
        context["cons"] = cons
        const = Contest.objects.all().filter(isContinued__icontains='ended').order_by('-id')
        context["const"] = const
        context["conteststatus"] = "active"
        return context

def results(request, pk):
    contest = Contest.objects.get(id=int(pk))
    names = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    count = ContestProblem.objects.all().filter(contest=contest).count()
    lproblems = names[:count:]
    results = ContestRating.objects.all().filter(contest=contest).order_by("-rating")
    return render(request, "contests/results.html", {"contest": contest, "results": results, "problems": lproblems, "conteststatus": "active"})

@login_required(login_url="login")
def follow(request, pk):
    contest = Contest.objects.get(id=int(pk))
    users = contest.users.all()
    rating = None
    if request.user in users:
        contest.users.remove(request.user)
        contest.save()
    elif request.user not in users and contest.isPublic == True:
        contest.users.add(request.user)
        contest.save()
        rating = None
        try:
            rating = ContestRating.objects.get(author=request.user, contest=contest)
        except:
            rating = None
        if not rating:
            ContestRating.objects.create(
                author=request.user,
                contest=contest
                )
    print(rating)
    return HttpResponseRedirect(reverse("contests"))

def follow_hide_contest(request, pk):
    contest = Contest.objects.get(id=int(pk))
    if request.method == "POST":
        pin = request.POST.get("password")
        if pin == contest.password:
            contest.users.add(request.user)
            messages.add_message(request, messages.SUCCESS, "Musobaqaga qo'shildingiz.")
            return HttpResponseRedirect(reverse("contest", args=[str(pk)])) 
    messages.add_message(request, messages.ERROR, "Musobaqa uchun PIN noto'g'ri")       
    return HttpResponseRedirect(reverse_lazy("contests"))
