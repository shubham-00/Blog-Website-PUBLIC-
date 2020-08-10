from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models.functions import Now
from .models import Post, Like, Follower
from .forms import PostCreationForm


def home(request):
    # posts = Post.objects.all().order_by("-date_posted")[:6]
    posts = Post.objects.filter()
    context = {"posts": posts}
    return render(request, "blog/home.html", context)


def about(request):
    return render(request, "blog/about.html")


def contact(request):
    return render(request, "blog/contact.html")


def feed(request):
    print(request.user)
    if str(request.user) == "AnonymousUser":
        return redirect("/login/")
    following = Follower.objects.filter(
        follower_user=User.objects.filter(username=request.user.username).first()
    )
    posts = []
    for f in following:
        posts.extend(
            Post.objects.filter(author=f.leader_user).order_by("-date_posted")[:10]
        )

    context = {"posts": posts}
    return render(request, "blog/feed.html", context)


def post(request, id):
    if request.method == "GET":
        post = Post.objects.filter(id=id).first()
        user = User.objects.filter(username=post.author).first()

        context = {"post": post, "liked": False}

        if request.user.is_authenticated:
            viewer = User.objects.filter(username=request.user.username).first()
            if Like.objects.filter(user=viewer, post=post).exists():
                context["liked"] = True

        return render(request, "blog/post.html", context)

    else:
        user = request.user
        user = User.objects.filter(username=user.username).first()
        post = Post.objects.filter(id=id).first()

        if Like.objects.filter(user=user, post=post).exists():
            Like.objects.filter(user=user, post=post).first().delete()
            post.likes -= 1
            post.save()

        else:
            Like(user=user, post=post).save()
            post.likes += 1
            post.save()

        return HttpResponse(post.likes)


@login_required
def create_post(request):
    if request.method == "POST":
        author = Post(author=request.user)

        form = PostCreationForm(request.POST, request.FILES, instance=author)

        if form.is_valid():
            form.save(commit=False)
            form.author = request.user
            form.save()
            post = (
                Post.objects.filter(
                    author=User.objects.filter(username=request.user.username)[0].id
                )
                .last()
                .id
            )
            messages.success(request, f"Post has been created!")
            return redirect(f"/post/{post}/")

    else:
        form = PostCreationForm()

    return render(request, "blog/create_post.html", {"form": form})


@login_required
def delete_post(request):
    if request.method == "POST":
        id = request.POST.get("id")
        post = Post.objects.filter(id=id).first()
        user = User.objects.filter(username=post.author.username).first()
        if user.username == str(request.user):
            Post.objects.get(id=id).delete()
            messages.success(request, f"Post has been deleted!")
            return redirect("/")
    messages.error(request, f"Something went wrong!")
    return redirect("/")


def my_posts(request, user):
    posts = Post.objects.filter(
        author=User.objects.filter(username=user).first().id
    ).order_by("-date_posted")
    context = {"posts": posts}
    return render(request, "blog/my_posts.html", context)

