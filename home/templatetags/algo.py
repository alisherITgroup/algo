from django.template import Library
from django.contrib.auth.models import User
from problemsets.models import Problem, Category
from quizzes.models import Question, Quiz
from problems.models import ArchiveProblem
from attempts.models import Attempt, Attempt2, ContestAttempt
from contests.models import Contest, ContestProblem
from posts.models import Post
import datetime

register = Library()

@register.filter()
def quiz_user(user_id, quiz_id):
    user = User.objects.get(id=int(user_id))
    quiz = Quiz.objects.get(id=int(quiz_id))
    if user in quiz.users.all():
        return True
    return False

@register.filter()
def check_problem(user_id, problem_id):
    user = User.objects.get(id=int(user_id))
    problem = ArchiveProblem.objects.get(id=int(problem_id))
    if user in problem.solvers.all():
        return "<span class='fas fa-check text-success'></span>"
    if user in problem.errors.all():
        return "<span class='fas fa-times text-danger'></span>"
    return ""

@register.filter()
def pro_letter(problem):
    pro_letter = chr(64+problem)
    return pro_letter

@register.filter()
def contest_status(contest_id):
    contest = Contest.objects.get(id=int(contest_id))
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
    elif startmonth < month:
        constat = "ended"
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
        
    return constat

@register.filter()
def isAbonent(contest_id, user_id):
    contest = Contest.objects.get(id=int(contest_id))
    user = User.objects.get(id=int(user_id))
    users = contest.users.all()
    if user in users:
        return True
    return False

@register.filter()
def is_adder(contest_id, user_id):
    contest = Contest.objects.get(id=contest_id)
    user = User.objects.get(id=user_id)
    if user in contest.authors.all():
        return True
    return False

@register.filter()
def td(problem, status):

    status = eval(status)
    try:
        r = f"+{status[problem]}"
    except:
        r = ""
    class_ = ""
    try:
        class_ = status[f"status{problem}"]
        class_ = "bg-success"
    except:
        if r == "" or r == "-1":
            class_ = ""
        else:
            class_ = "bg-danger"
            r = r.replace("+", "-")
    if r == '+0' or r == "-0":
        if r == "-0":
            r = "-"
        else:
            r = "+"
    return f"<td class='{class_} fw-bold' style='border: 1px solid #ccc;'><center>{r}</center></td>"

@register.filter()
def tags_as_p(post_id):
    post = Post.objects.get(id=int(post_id))
    tags = post.tags.all()
    rtags = ""
    for tag in tags:
        rtags += f"<span class='badge badge-soft-info'>{tag.tag}</span> "
    return rtags

@register.filter()
def isOdd(number):
    if int(number)%2==0:
        return False
    return True

@register.filter()
def last_attempt_code(user_id, problem_id):
    user = User.objects.get(id=int(user_id))
    problem = ArchiveProblem.objects.get(id=int(problem_id))
    attempt = Attempt.objects.all().filter(author=user, problem=problem).last()
    try:
        return attempt.code
    except:
        return ""

@register.filter()
def last_attempt_code2(user_id, problem_id):
    user = User.objects.get(id=int(user_id))
    problem = Problem.objects.get(id=int(problem_id))
    attempt = Attempt2.objects.all().filter(author=user, problem=problem).last()
    try:
        return attempt.code
    except:
        return ""
    
@register.filter()
def last_attempt_code3(user_id, problem_id):
    user = User.objects.get(id=int(user_id))
    problem = ContestProblem.objects.get(id=int(problem_id))
    attempt = ContestAttempt.objects.all().filter(author=user, problem=problem).last()
    try:
        return attempt.code
    except:
        return ""

@register.filter()
def count_solved_problems(user_id):
    user = User.objects.get(id=int(user_id))
    problems = ArchiveProblem.objects.all().filter(solvers=user)
    allproblems = ArchiveProblem.objects.all().count()
    return f"{allproblems} / {problems.count()}"

@register.filter()
def check_problem_status(user_id, problem_id):
    user = User.objects.get(id=int(user_id))
    problem = ArchiveProblem.objects.get(id=int(problem_id))
    if user in problem.solvers.all():
        return "success"
    if user in problem.errors.all():
        return "danger"
    return "default"

@register.filter()
def cases2(attempt_id):
    attempt = Attempt2.objects.get(id=int(attempt_id))
    cases = attempt.cases
    acase = ''''''
    counter = 1
    for case in eval(cases):
        if "Acc" in case["status"]:
            class_ = "text-success"
        else:
            class_ = "text-danger"
        rcase = f'''<div class="accordion-item">
                        <h2 class="accordion-header" id="heading1">
                            <button class="fw-bold accordion-button collapsed {class_}" type="button" data-bs-toggle="collapse" data-bs-target="#collapse{counter}" aria-expanded="true" aria-controls="collapse1">Test {counter}</button>
                        </h2>
                        <div class="accordion-collapse collapse" id="collapse{counter}" aria-labelledby="heading1" data-bs-parent="#accordion{counter}">
                            <div class="accordion-body">
                                <div class="table-responsive">
                                    <table class="table table-hover">
                                        <tr style="boder: 1px solid #ccc;">
                                            <td style="boder: 1px solid #ccc;">Vaqt</td>
                                            <td style="boder: 1px solid #ccc;">{case["time"]}</td>
                                        </tr>
                                        <tr style="boder: 1px solid #ccc;">
                                            <td style="boder: 1px solid #ccc;">Kirish oqimi</td>
                                            <td style="boder: 1px solid #ccc;">{case["input"]}</td>
                                        </tr>
                                        <tr style="boder: 1px solid #ccc;">
                                            <td style="boder: 1px solid #ccc;">Chiqish oqimi</td>
                                            <td class="{class_}">{case["test_result"]}</td>
                                        </tr>
                                        <tr style="boder: 1px solid #ccc;">
                                            <td style="boder: 1px solid #ccc;">Sizning javobingiz</td>
                                            <td class="{class_}">{case["your_result"]}</td>
                                        </tr>
                                        <tr style="boder: 1px solid #ccc;">
                                            <td style="boder: 1px solid #ccc;">Holati</td>
                                            <td class="{class_}">{case["status"]}</td>
                                        </tr>
                                    </table>
                                </div>
                            </div>
                        </div>
                    </div>'''
        acase += rcase
        counter += 1
    return acase


@register.filter()
def cases(attempt_id):
    attempt = Attempt.objects.get(id=int(attempt_id))
    cases = attempt.cases
    acase = ''''''
    counter = 1
    for case in eval(cases):
        if "Acc" in case["status"]:
            class_ = "text-success"
        else:
            class_ = "text-danger"
        rcase = f'''<div class="accordion-item">
                        <h2 class="accordion-header" id="heading1">
                            <button class="fw-bold accordion-button collapsed {class_}" type="button" data-bs-toggle="collapse" data-bs-target="#collapse{counter}" aria-expanded="true" aria-controls="collapse1">Test {counter}</button>
                        </h2>
                        <div class="accordion-collapse collapse" id="collapse{counter}" aria-labelledby="heading1" data-bs-parent="#accordion{counter}">
                            <div class="accordion-body">
                                <div class="table-responsive">
                                    <table class="table table-hover">
                                        <tr style="boder: 1px solid #ccc;">
                                            <td style="boder: 1px solid #ccc;">Vaqt</td>
                                            <td style="boder: 1px solid #ccc;">{case["time"]}</td>
                                        </tr>
                                        <tr style="boder: 1px solid #ccc;">
                                            <td style="boder: 1px solid #ccc;">Kirish oqimi</td>
                                            <td style="boder: 1px solid #ccc;">{case["input"]}</td>
                                        </tr>
                                        <tr style="boder: 1px solid #ccc;">
                                            <td style="boder: 1px solid #ccc;">Chiqish oqimi</td>
                                            <td class="{class_}">{case["test_result"]}</td>
                                        </tr>
                                        <tr style="boder: 1px solid #ccc;">
                                            <td style="boder: 1px solid #ccc;">Sizning javobingiz</td>
                                            <td class="{class_}">{case["your_result"]}</td>
                                        </tr>
                                        <tr style="boder: 1px solid #ccc;">
                                            <td style="boder: 1px solid #ccc;">Holati</td>
                                            <td class="{class_}">{case["status"]}</td>
                                        </tr>
                                    </table>
                                </div>
                            </div>
                        </div>
                    </div>'''
        acase += rcase
        counter += 1
    return acase

@register.filter()
def contestcases(attempt_id):
    attempt = ContestAttempt.objects.get(id=int(attempt_id))
    cases = attempt.cases
    acase = ''''''
    counter = 1
    for case in eval(cases):
        if "Acc" in case["status"]:
            class_ = "text-success"
        else:
            class_ = "text-danger"
        rcase = f'''<div class="accordion-item">
                        <h2 class="accordion-header" id="heading1">
                            <button class="fw-bold accordion-button collapsed {class_}" type="button" data-bs-toggle="collapse" data-bs-target="#collapse{counter}" aria-expanded="true" aria-controls="collapse1">Test {counter}</button>
                        </h2>
                        <div class="accordion-collapse collapse" id="collapse{counter}" aria-labelledby="heading1" data-bs-parent="#accordion{counter}">
                            <div class="accordion-body">
                                <div class="table-responsive">
                                    <table class="table table-hover">
                                        <tr style="boder: 1px solid #ccc;">
                                            <td style="boder: 1px solid #ccc;">Vaqt</td>
                                            <td style="boder: 1px solid #ccc;">{case["time"]}</td>
                                        </tr>
                                        <tr style="boder: 1px solid #ccc;">
                                            <td style="boder: 1px solid #ccc;">Kirish oqimi</td>
                                            <td style="boder: 1px solid #ccc;">{case["input"]}</td>
                                        </tr>
                                        <tr style="boder: 1px solid #ccc;">
                                            <td style="boder: 1px solid #ccc;">Chiqish oqimi</td>
                                            <td class="{class_}">{case["test_result"]}</td>
                                        </tr>
                                        <tr style="boder: 1px solid #ccc;">
                                            <td style="boder: 1px solid #ccc;">Sizning javobingiz</td>
                                            <td class="{class_}">{case["your_result"]}</td>
                                        </tr>
                                        <tr style="boder: 1px solid #ccc;">
                                            <td style="boder: 1px solid #ccc;">Holati</td>
                                            <td class="{class_}">{case["status"]}</td>
                                        </tr>
                                    </table>
                                </div>
                            </div>
                        </div>
                    </div>'''
        acase += rcase
        counter += 1
    return acase


@register.filter()
def questions_count(quiz_id):
    quiz = Quiz.objects.get(id=int(quiz_id))
    count = Question.objects.all().filter(quiz=quiz).count()
    return count

@register.filter()
def category_as_p(problem_id):
    problem = Problem.objects.get(id=int(problem_id))
    categories = problem.category.all()
    c = ""
    for category in categories:
        c += category.name + " "
    return c

@register.filter()
def category_as_p2(problem_id):
    problem = ArchiveProblem.objects.get(id=int(problem_id))
    categories = problem.category.all()
    c = ""
    for category in categories:
        c += category.name + " "
    return c

@register.filter()
def categories(user_id):
    categories = Category.objects.all()
    return categories

@register.filter()
def langs_as_options(user_id, problem_id):
    user = User.objects.get(id=int(user_id))
    problem = Problem.objects.get(id=int(problem_id))
    attempt = Attempt2.objects.all().filter(author=user, problem=problem).last()
    selectedlang = ""
    try:
        lang_name = ""
        if attempt.language == "csharp":
            lang_name = "C#"
        elif attempt.language == "cpp":
            lang_name = "C++"
        else:
            lang_name = str(attempt.language).title()
        selectedlang =  f"<option value='{attempt.language}'>{lang_name}</option>"
    except:
        selectedlang = f"<option value=''>--Tanlang--</option>"
    langs = problem.allowedlangs.all()
    html = selectedlang
    for lang in langs:
        if lang.name == "csharp":
            lang_name = "C#"
        elif lang.name == "cpp":
            lang_name = "C++"
        else:
            lang_name = str(lang.name).title()
        plus = f"<option value='{lang.name}'>{lang_name}</option>"
        if plus != selectedlang:
            html += plus
    return html

@register.filter()
def langs_as_option(contest_id):
    contest = Contest.objects.get(id=int(contest_id))
    langs = contest.langs.all()
    html = ""
    for lang in langs:
        if lang.name == "csharp":
            lang_name = "C#"
        elif lang.name == "cpp":
            lang_name = "C++"
        else:
            lang_name = str(lang.name).title()
        html += f"<option value='{lang.name}'>{lang_name}</option>"
    return html

@register.filter()
def langs_as_options2(user_id, problem_id):
    user = User.objects.get(id=int(user_id))
    problem = ArchiveProblem.objects.get(id=int(problem_id))
    attempt = Attempt.objects.all().filter(author=user, problem=problem).last()
    selectedlang = ""
    try:
        lang_name = ""
        if attempt.language == "csharp":
            lang_name = "C#"
        elif attempt.language == "cpp":
            lang_name = "C++"
        else:
            lang_name = str(attempt.language).title()
        selectedlang =  f"<option value='{attempt.language}'>{lang_name}</option>"
    except:
        selectedlang = f"<option value=''>--Tanlang--</option>"
    langs = problem.allowedlangs.all()
    html = selectedlang
    for lang in langs:
        if lang.name == "csharp":
            lang_name = "C#"
        elif lang.name == "cpp":
            lang_name = "C++"
        else:
            lang_name = str(lang.name).title()
        plus = f"<option value='{lang.name}'>{lang_name}</option>"
        if plus != selectedlang:
            html += plus
    return html

@register.filter()
def tests_as_table3(problem_id):
    problem = ContestProblem.objects.get(id=int(problem_id))
    simpletests = problem.simpletests
    html = ""
    simpletests = dict(eval(simpletests))
    index = 1
    for test in simpletests:
        input_ = str(test).replace("\n", "<br>")
        output = str(simpletests[test]).replace("\n", "<br>")
        html += f"<tr style=\"border: 0.1px solid #ccc\"><td style=\"border: 0.1px solid #ccc\">{index}</td><td style=\"border: 0.1px solid #ccc\">{input_}</td><td style=\"border: 0.1px solid #ccc\">{output}</td></tr>"
        index += 1
    return html

@register.filter()
def tests_as_table(problem_id):
    problem = Problem.objects.get(id=int(problem_id))
    simpletests = problem.simpletests
    html = ""
    simpletests = dict(eval(simpletests))
    index = 1
    for test in simpletests:
        input_ = str(test).replace("\n", "<br>")
        output = str(simpletests[test]).replace("\n", "<br>")
        html += f"<tr style=\"border: 0.1px solid #ccc\"><td style=\"border: 0.1px solid #ccc\">{index}</td><td style=\"border: 0.1px solid #ccc\">{input_}</td><td style=\"border: 0.1px solid #ccc\">{output}</td></tr>"
        index += 1
    return html

@register.filter()
def tests_as_table2(problem_id):
    problem = ArchiveProblem.objects.get(id=int(problem_id))
    simpletests = problem.simpletests
    html = ""
    simpletests = dict(eval(simpletests))
    index = 1
    for test in simpletests:
        input_ = str(test).replace("\n", "<br>")
        output = str(simpletests[test]).replace("\n", "<br>")
        html += f"<tr style=\"border: 0.1px solid #ccc\"><td style=\"border: 0.1px solid #ccc\">{index}</td><td style=\"border: 0.1px solid #ccc\">{input_}</td><td style=\"border: 0.1px solid #ccc\">{output}</td></tr>"
        index += 1
    return html

@register.filter()
def as_avatar(user):
    user = User.objects.get(id=int(user))
    username = user.username
    return f"{str(username)[0].upper()}"
