from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import permissions
from django.http import JsonResponse
from django.db import IntegrityError
from attempts.models import Attempt
from problems.models import ArchiveProblem
import datetime
import requests
from home.models import TimeLine
import json
from .serailizers import UserSerializer, ArchiveProblemSerializer, AttemptSerializer

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, ]

class ArchiveProblemViewSet(ModelViewSet):
    queryset = ArchiveProblem.objects.all()
    serializer_class = ArchiveProblemSerializer
    permission_classes = [permissions.IsAuthenticated, ]

class AttemptViewSet(ModelViewSet):
    queryset = Attempt.objects.all()
    serializer_class = AttemptSerializer    
    permission_classes = [permissions.IsAuthenticated, ]

    def create(self, request, *args, **kwargs):
        request.POST._mutable = True
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
        request.data["date"] = datetime.datetime.now().date()
        request.data["author"] = request.user.id
        request.data["problem"] = problem.id
        request.data["code"] = code
        request.data["language"] = language
        request.data["time"] = time*1000
        request.data["output"] = output
        request.data["status"] = status
        request.data["cases"] = action_tests
        request.data["lengthcode"] = len(code)
        request.data._mutable = False
        return super().create(request, *args, **kwargs)

@csrf_exempt
def sign_up(request):
    if request.method == "POST":
        try:
            data = dict(request.POST)
            user = User.objects.create_user(data['username'][0], password=data['password'][0])
            user.save()
            token = Token.objects.create(user=user)
            return JsonResponse({"token": str(token)}, status=201)
        except IntegrityError:
            return JsonResponse({"xatolik": "Bu foydalanuvchi nomi oldin olingan!"})
    return JsonResponse({"signup": 200})
@csrf_exempt
def login(request):
    if request.method == "POST":
        data = dict(request.POST)
        user = authenticate(request, username=data['username'][0], password=data['password'][0])
        if user is None:
            return JsonResponse({"xatolik": "Foydalanuvchi nomi yoki kalit so'zi noto'g'ri"}, status=404)
        else:
            try:
                token = Token.objects.get(user=user)
            except:
                token = Token.objects.create(user=user)
            return JsonResponse({"token": str(token)}, status=200)
    return JsonResponse({"login": 200})