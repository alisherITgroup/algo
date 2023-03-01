from django.shortcuts import render
from django.views import generic
from .models import Project
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.urls import reverse
from random import randint

def generate():
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    digits = "0123456789"
    name = ""
    for i in range(4):
        name += letters[randint(0, 25)]
        name += digits[randint(0, 9)]
    return name

def create(request):
    return render(request, "projects/create.html")

def projects(request, username):
    user = request.user
    projects = Project.objects.all().filter(author=user)
    if request.method == "POST":
        name = request.POST.get("name")
        password = request.POST.get("password")
        language = request.POST.get("language")
        subname = generate()
        if language == "python":
            code = "print('Salom dunyo!')"
        if language == "cpp":
            code = "#include <iostream>\nusing namespace std;\nint main(){\n\tcout << \"Salom dunyo!\";\n}"
        if language == "java":
            code = "class Main{\n\tpublic static void main(String args[]){\n\t\tSystem.out.println(\"Salom dunyo!\");\n\t}\n}"
        Project.objects.create(
            author=request.user,
            name=name,
            subname=subname,
            password=password,
            language=language,
            code=code
        )
        project = Project.objects.get(author=request.user, name=name, password=password, language=language)
    return render(request, "projects/projects.html", {"projects": projects, "projectstatus": "active"})

def project(request, subname):
    project = Project.objects.get(subname=subname)
    if request.user.id != project.author.id:
        project = None
    return render(request, "projects/project.html", {"project": project, "projectstatus": "active"})

@api_view(http_method_names=['POST'])
def run(request, subname):
    if request.method == 'POST':
        code = request.data['code']
        project = Project.objects.get(subname=subname)
        project.code = code
        project.save()
        return Response({"save": "true"})
    return Response({
        "save": "true"
    })