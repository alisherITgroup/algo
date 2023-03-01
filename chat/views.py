from django.shortcuts import render
from .models import Chat, Message
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required


@login_required(login_url="login")
def follow(request, pk, integer):
    abonent1 = User.objects.get(id=int(pk))
    abonent2 = User.objects.get(id=int(integer))
    try:
        try:
            chat = Chat.objects.get(abonent1=abonent1, abonent2=abonent2)
        except:
            chat = Chat.objects.get(abonent1=abonent2, abonent2=abonent1)
    except:
        Chat.objects.create(
            abonent1=abonent1,
            abonent2=abonent2,
        )
        chat = Chat.objects.get(abonent1=abonent1, abonent2=abonent2)
    return HttpResponseRedirect(reverse("chat", args=[str(pk), str(integer)]))

@login_required(login_url="login")
def chat(request, pk, integer):
    try:
        abonent1 = User.objects.get(id=int(pk))
        abonent2 = User.objects.get(id=int(integer))
        try:
            chat = Chat.objects.get(abonent1=abonent1, abonent2=abonent2)
        except:
            chat = Chat.objects.get(abonent1=abonent2, abonent2=abonent1)
    except:
        chat = None
    if chat:
        messages = Message.objects.all().filter(chat=chat)
    else:
        messages = None
    if chat and request.method == "POST":
        Message.objects.create(
            chat=chat,
            from_user=request.user,
            message=request.POST.get("message")
        )
    return render(request, "chat/chat.html", {"chat": chat, "messages": messages})