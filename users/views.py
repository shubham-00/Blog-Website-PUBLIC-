from django.shortcuts import render, redirect
from django.http import HttpResponse

# from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile
from blog.models import Follower


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            if User.objects.filter(email=form.cleaned_data.get("email")).exists():
                messages.success(request, f"Email already exists! Try logining.")
                return redirect("users-login")
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(
                request, f"Your account has been created! Try logining in!"
            )
            return redirect("users-login")

    else:
        form = UserRegisterForm()

    return render(request, "users/register.html", {"form": form})


def profile(request, user):
    username = user
    user = User.objects.filter(username=user).first()
    if request.method == "POST":

        if request.POST.get("follow_to", "") == "":
            # User profile update
            u_form = UserUpdateForm(request.POST, instance=user)
            p_form = ProfileUpdateForm(
                request.POST,
                request.FILES,
                instance=Profile.objects.filter(user=user).first(),
            )

            if u_form.is_valid() and p_form.is_valid():

                u_form.save()
                p_form.save()
                messages.success(request, "Profile updated")
                return redirect(f"/profile/{ request.POST.get('username') }/")

        else:
            # Follower arrived
            print("Line 57 ... WOO", "\n\n\n\n\n\n\n\n\n\n")

            leader = User.objects.filter(username=user).first()
            follower = User.objects.filter(username=request.user.username).first()

            if Follower.objects.filter(
                leader_user=leader, follower_user=follower
            ).exists():
                print("Follower exists, deleting...", "\n\n\n\n\n\n\n\n\n\n")
                Follower.objects.filter(
                    leader_user=leader, follower_user=follower
                ).first().delete()

            else:
                print("Adding a new follower...", "\n\n\n\n\n\n\n\n\n\n")
                Follower(leader_user=leader, follower_user=follower).save()

            followers = Follower.objects.filter(leader_user=user).count()
            return HttpResponse(followers)

    else:
        u_form = UserUpdateForm(instance=user)
        p_form = ProfileUpdateForm(instance=Profile.objects.filter(user=user).first())

        if request.user.is_authenticated:
            viewer = User.objects.filter(username=request.user.username).first()
            if Follower.objects.filter(leader_user=user, follower_user=viewer).exists():
                following = True
            else:
                following = False

    context = {
        "u_form": u_form,
        "p_form": p_form,
        "author": user,
        "followers": Follower.objects.filter(leader_user=user).count(),
    }
    try:
        context["following"] = following
    except:
        context["following"] = False

    if not user:
        return HttpResponse("Invalid...")
    return render(request, "users/profile.html", context)
