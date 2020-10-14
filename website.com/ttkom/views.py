from django.shortcuts import render
from .models import Post
from django.utils import timezone

# Create your views here.

def index(request):
    posts = Post.objects.filter(date_post__lt=timezone.now()).order_by('-date_post')
    msg = "HI"
    if request.user.is_authenticated:
        msg = "HI " + request.user.username
    data = {
        "posts": posts,
        "msg": msg,
    }
    return render(request, "ttkom/home.html", context=data)
