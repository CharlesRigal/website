from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from .models import Post, Comment
from django.contrib.sites.shortcuts import get_current_site
from .tokens import account_activation_token
from django.utils.encoding import force_bytes, force_text
from django.utils import timezone
from .forms import CommentForm, RegisterForm, ChangeForm
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import reverse
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


@login_required(login_url="/connextion/")
def account(request):
    form = ChangeForm(request.POST or None, instance=request.user)
    if request.POST and form.is_valid():
        form.save()

    context = {
        'form': form,
    }
    return render(request, "ttkom/account/edit_account.html", context=context)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'registration/account_activation_invalid.html')


def account_activation_send(request):
    return render(request, 'registration/account_activation_send.html')


def register_view(request):
    form = RegisterForm(request.POST or None)

    if request.POST and form.is_valid():
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(request)
        subject = 'Activer votre compte'
        message = render_to_string('registration/account_activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        user.email_user(subject, message)
        return redirect(account_activation_send)
    context = {
        'form': form
    }
    return render(request, 'registration/register.html', context=context)


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
