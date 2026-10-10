from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .forms import SignUpForm, ProfileForm, PostForm, CommentForm
from .models import Post, Follow

User = get_user_model()

def signup(request):
    if request.user.is_authenticated:
        return redirect("feed")
    form = SignUpForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Welcome! Your account is ready.")
        return redirect("feed")
    return render(request, "registration/signup.html", {"form": form})

def feed(request):
    posts = Post.objects.select_related("author", "author__profile").prefetch_related("likes", "comments__author")
    form = PostForm()
    comment_form = CommentForm()
    following_ids = []
    liked_ids = []
    if request.user.is_authenticated:
        following_ids = list(Follow.objects.filter(follower=request.user).values_list("followed_id", flat=True))
        liked_ids = list(request.user.liked_posts.values_list("id", flat=True))
    return render(request, "network/feed.html", {
        "posts": posts, "form": form, "comment_form": comment_form,
        "following_ids": following_ids, "liked_ids": liked_ids,
    })

@login_required
@require_POST
def create_post(request):
    form = PostForm(request.POST)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        messages.success(request, "Your post was published.")
    else:
        messages.error(request, "Please write a post (up to 1,000 characters).")
    return redirect(request.POST.get("next") or "feed")

@login_required
@require_POST
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id, author=request.user)
    post.delete()
    messages.success(request, "Post deleted.")
    return redirect(request.POST.get("next") or "feed")

@login_required
@require_POST
def toggle_like(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.likes.filter(pk=request.user.pk).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect(request.POST.get("next") or "feed")

@login_required
@require_POST
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
    else:
        messages.error(request, "Comment cannot be empty.")
    return redirect(request.POST.get("next") or "feed")

def profile(request, username):
    person = get_object_or_404(User.objects.select_related("profile"), username=username)
    posts = person.posts.select_related("author", "author__profile").prefetch_related("likes", "comments__author")
    is_following = request.user.is_authenticated and Follow.objects.filter(follower=request.user, followed=person).exists()
    liked_ids = list(request.user.liked_posts.values_list("id", flat=True)) if request.user.is_authenticated else []
    return render(request, "network/profile.html", {
        "person": person, "posts": posts, "is_following": is_following,
        "liked_ids": liked_ids, "form": PostForm(), "comment_form": CommentForm(),
        "followers_count": person.follower_links.count(),
        "following_count": person.following_links.count(),
    })

@login_required
@require_POST
def toggle_follow(request, username):
    person = get_object_or_404(User, username=username)
    if person == request.user:
        messages.info(request, "You cannot follow yourself.")
        return redirect("profile", username=username)
    link, created = Follow.objects.get_or_create(follower=request.user, followed=person)
    if not created:
        link.delete()
    return redirect("profile", username=username)

@login_required
def edit_profile(request):
    profile_obj, _ = request.user.profile, None
    form = ProfileForm(request.POST or None, instance=profile_obj)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Profile updated.")
        return redirect("profile", username=request.user.username)
    return render(request, "network/edit_profile.html", {"form": form})
