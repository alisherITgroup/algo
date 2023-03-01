from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import generic
from .models import Quiz, Question, QuizRating
from .forms import QuizForm, QuestionForm
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants

class QuizCreateView(generic.CreateView):
    model = Quiz
    form_class = QuizForm
    template_name = "quizzes/create.html"

class QuizEditView(generic.UpdateView):
    model = Quiz
    form_class = QuizForm
    template_name = "quizzes/edit.html"


class EditQuestionView(generic.UpdateView):
    model = Question
    form_class = QuestionForm
    template_name = "quizzes/edit_question.html"
    context_object_name = "question"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        question = Question.objects.get(id=int(self.kwargs['pk']))
        context["quiz"] = question.quiz
        return context

def question_create(request, pk):
    form = QuestionForm()
    quiz = Quiz.objects.get(id=int(pk))
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, constants.SUCCESS, f"Savol muvaqqiyatli yaratildi!")
            return HttpResponseRedirect(reverse("quiz", args=[str(pk)]))
        else:
            messages.add_message(request, constants.ERROR, f"{form.errors.as_json()}")
    return render(request, "quizzes/create_question.html", {"form": form, "quiz": quiz})

class Quizzes(generic.ListView):
    model = Quiz
    context_object_name = "quizzes"
    template_name = "quizzes/quizzes.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["quizstatus"] = "active"
        return context
def follow_quiz(request, pk):
    if request.method == "POST":
        pin = request.POST.get("password")
        quiz = Quiz.objects.get(id=int(pk))
        if quiz.password == pin:
            messages.add_message(request, messages.SUCCESS, "Siz test sinoviga qatnashayabsiz")
            if request.user not in quiz.users.all():
                quiz.users.add(request.user)
            return HttpResponseRedirect(reverse("quiz", args=[str(pk)]))
        else:
            messages.add_message(request, messages.ERROR, "Pin noto'g'ri kiritildi")
            return HttpResponseRedirect(reverse_lazy("quizzes"))
    return HttpResponseRedirect(reverse_lazy("quizzes"))

def quiz_ratings(request, pk):
    quiz = Quiz.objects.get(id=int(pk))
    ratings = QuizRating.objects.all().filter(quiz=quiz).order_by("-rating")
    return render(request, "quizzes/results.html", {"ratings": ratings, "quiz": quiz})

def quiz(request, pk):
    quiz = Quiz.objects.get(id=int(pk))
    if quiz.isPublished == True and quiz.isPublic == True:
        pass
    if quiz.isPublished == False and request.user.id != quiz.author.id:
        messages.add_message(request, messages.WARNING, "Kechirasiz bu test sinovi hali chop etilmagan")
        return HttpResponseRedirect(reverse_lazy("quizzes"))
    if quiz.isPublished and request.user in quiz.users.all():
        pass
    if quiz.isPublic == False and request.user not in quiz.users.all():
        messages.add_message(request, messages.WARNING, "Kechirasiz bu test sinovi yopiq va siz bu test sinovi ishtirokchisi emassiz")
        return HttpResponseRedirect(reverse_lazy("quizzes"))

    user = request.user
    if not (user in quiz.solvers.all()):
        questions = Question.objects.all().filter(quiz=quiz)
        status = "Siz hali bu testni ishlamagansiz!"
    else:
        questions = False
        if request.user.id != quiz.author.id:
            result = QuizRating.objects.get(quiz=quiz, author=user)
            status = f"Siz bu testdan {result.rating} ball olgansiz!"
        else:
            status = "Siz bu testni muallifi"
    if request.user.id == quiz.author.id:
        questions = Question.objects.all().filter(quiz=quiz)
    return render(request, "quizzes/quiz.html", {"quiz": quiz, "questions": questions, "users": quiz.users.count(), "status": status, "quizstatus": "active"})

def publish(request, pk):
    quiz = Quiz.objects.get(id=int(pk))
    quiz.isPublished = True
    quiz.save()
    messages.add_message(request, messages.SUCCESS, "Test chop etildi(Ommaga taqdim etildi)")
    return HttpResponseRedirect(reverse("quiz", args=[str(pk)]))

def check(request, pk, username):
    author = User.objects.all().filter(username=username).first()
    quiz = Quiz.objects.get(id=int(pk))
    status = ""
    rating = 0
    if request.method == "POST":
        results = dict(request.POST)
        results_keys = list(results.keys())[1::]
        summ = len(results_keys)
        count = 1
        print(results_keys)
        for test in results_keys:
            question = Question.objects.get(id=int(test))
            status += f"<p>{count}. {question.question}</p>"
            print(test)
            if question.true == results[test][0]:
                status += f"&nbsp;&nbsp;&nbsp;&nbsp;<p><span class='fas fa-check text-success'></span></p><br><hr>"
                rating += question.level
            else:
                status += f"&nbsp;&nbsp;&nbsp;&nbsp;<p><span class='fas fa-times text-danger'></span></p><br><hr>"
            count += 1
        quizrating = None
        try:
            quizrating = QuizRating.objects.get(author=request.user, quiz=quiz)
        except:
            quizrating = None
        if not quizrating and int(request.user.id) != int(quiz.author.id):
            QuizRating.objects.create(
                author=request.user,
                quiz=quiz,
                rating=rating,
                status=status
            )
        quiz.solvers.add(author)
    try:
        result = QuizRating.objects.get(quiz=quiz, author=author)
    except:
        result = None
    return render(request, "quizzes/result.html", {"result": result, "rating": rating, "quiz": quiz})
