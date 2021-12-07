from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required

from yatube.settings import PAGE_COUNT

from .models import Group, Post, User, Follow
from .forms import PostForm, CommentForm


from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required

from yatube.settings import PAGE_COUNT

from .models import Group, Post, User


def index(request):
    template = "posts/index.html"
    posts = Post.objects.all()
    paginator = Paginator(posts, PAGE_COUNT)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "page_obj": page_obj,
    }
    return render(request, template, context)


def group_posts(request, slug):
    template = "posts/group_list.html"
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    paginator = Paginator(posts, PAGE_COUNT)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "group": group,
        "page_obj": page_obj,
    }
    return render(request, template, context)


def profile(request, username):
    template = "posts/profile.html"
    post = get_object_or_404(User, username=username)
    posts = post.posts.all()
    paginator = Paginator(posts, PAGE_COUNT)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    subscribers = post.following.all()
    following = False
    authors = list()
    for user in subscribers:
        author = user.user
        authors.append(author)
    if request.user in authors:
        following = True
    context = {
        "post": post,
        "page_obj": page_obj,
        "number_of_posts": posts.count(),
        'following': following
    }
    return render(request, template, context)


def post_detail(request, post_id):
    template = "posts/post_detail.html"
    post_detail = get_object_or_404(Post, pk=post_id)
    author = post_detail.author
    number_of_posts = author.posts.all().count()
    form = CommentForm(request.POST or None)
    comments = post_detail.comments.all()
    context = {
        "post_detail": post_detail,
        "number_of_posts": number_of_posts,
        "comments": comments,
        "form": form,
    }
    return render(request, template, context)


@login_required
def post_create(request):
    if request.method != "POST":
        form = PostForm()
        return render(request, "posts/create.html", {"form": form})
    form = PostForm(request.POST, files=request.FILES or None)
    if not form.is_valid():
        return render(request, "posts/create.html", {"form": form})
    form.instance.author = request.user
    form.save()
    return redirect("posts:profile", request.user.username)


@login_required
def post_edit(request, post_id):
    post_edit = get_object_or_404(Post, pk=post_id)
    if request.method != "POST":
        form = PostForm(instance=post_edit)
        return render(
            request, "posts/create.html", {"form": form, "is_edit": post_edit}
        )
    form = PostForm(
        request.POST or None, files=request.FILES or None, instance=post_edit
    )
    if not form.is_valid():
        return render(request, "posts/create.html", {"form": form})
    form.save()
    return redirect("posts:post_detail", post_id)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect("posts:post_detail", post_id)


@login_required
def follow_index(request):
    user = request.user
    followings = user.follower.all()
    authors = list()
    for user in followings:
        author = user.author
        authors.append(author)
    post_list = Post.objects.filter(author__in=authors)
    paginator = Paginator(post_list, PAGE_COUNT)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "page_obj": page_obj,
    }
    return render(request, "posts/follow.html", context)


@login_required
def profile_follow(request, username):
    post_author = get_object_or_404(User, username=username)
    subscribers = post_author.following.all()
    authors = list()
    for user in subscribers:
        author = user.user
        authors.append(author)
    if request.user != post_author and request.user not in authors:
        Follow.objects.create(user=request.user, author=post_author)
    return redirect("posts:profile", username=username)


@login_required
def profile_unfollow(request, username):
    post_author = get_object_or_404(User, username=username)
    Follow.objects.filter(user=request.user, author=post_author).delete()
    return redirect("posts:profile", username=username)
