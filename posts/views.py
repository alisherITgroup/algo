from django.shortcuts import render
from .models import Post, PostComment
from .forms import PostForm
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    form_class = PostForm
    template_name = "posts/create.html"
    login_url = reverse_lazy("login")

    def form_invalid(self, form):
        print(form.errors.as_text())
        messages.add_message(self.request, messages.ERROR, "Iltimos maydonlarni to'g'ri to'ldiring.")
        return super().form_invalid(form)
    
    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, "Maqola muvaqqiyatli yataildi!")
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Post
    form_class = PostForm
    template_name = "posts/update.html"
    login_url = reverse_lazy("login")

    def form_invalid(self, form):
        print(form.errors.as_text())
        messages.add_message(self.request, messages.ERROR, "Iltimos maydonlarni to'g'ri to'ldiring.")
        return super().form_invalid(form)
    
    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, "Maqola muvaqqiyatli tahrirlandi!")
        return super().form_valid(form)

class PostsView(generic.ListView):
    model = Post
    template_name = "posts/posts.html"
    context_object_name = "posts"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["poststatus"] = "active"
        return context

class PostDetailView(generic.DetailView):
    model = Post
    template_name = "posts/post.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["poststatus"] = "active"
        post = Post.objects.get(id=self.kwargs["pk"])
        comments = PostComment.objects.all().filter(post=post).order_by('-id')
        count_comments = comments.count()
        context["comments"] = comments
        isLiked = False
        if self.request.user in post.likes.all():
            isLiked = True
        else:
            isLiked = False
        context["liked"] = isLiked
        context["count_comments"] = count_comments
        return context

@login_required(login_url="login")
def comment(request, pk):
    post = Post.objects.get(id=int(pk))
    PostComment.objects.create(
        author=request.user,
        post=post,
        body=request.POST.get("comment")
    )
    messages.add_message(request, messages.SUCCESS, "Izox qoldirish muvaqqiyatli amalga oshirildi.")
    return HttpResponseRedirect(reverse("post", args=[str(pk)]))

@login_required(login_url="login")
def like(request, pk):
    post = Post.objects.get(id=int(pk))
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return HttpResponseRedirect(reverse("post", args=[str(pk)]))
    
