from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from .models import Post, Comment
from django.utils import timezone
from .forms import CommentForm
from django.urls import reverse

# Create your views here.


def like_view(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    post.likes.add(request.user)
    return HttpResponseRedirect(reverse('post_detail', args=[str(pk)]))


def post_detail_view(request, pk):
    form = CommentForm(request.POST or None)
    post = Post.objects.get(pk=pk)
    comments = Comment.objects.filter(fk_post=post).order_by("-date_comment")
    if request.POST and form.is_valid():
        Comment.objects.create(fk_post=post, fk_author=request.user, content=form.cleaned_data["content"])
        form = CommentForm(None)
    context = {
        "form": form,
        "post": post,
        "comments": comments,
    }
    return render(request, "ttkom/post/post_detail.html", context=context)


def index(request):
    posts = Post.objects.filter(date_post__lt=timezone.now()).order_by('-date_post')
    msg = "HI"
    if request.user.is_authenticated:
        msg = "HI " + request.user.username
    data = {
        "posts": posts,
        "msg": msg,
    }
    return render(request, "ttkom/post/home.htm", context=data)
