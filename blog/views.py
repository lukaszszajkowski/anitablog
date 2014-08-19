from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.shortcuts import render
from .models import Post, Comment
from .forms import PostForm, CommentForm


def home(request):
    return render(request, 'index.html', {'test': "test"})


def list_posts(request):
    form = CommentForm(request.POST or None)
    posts = Post.objects.all()
    comments = Comment.objects.all()
    return render(request, 'posts.html', {'posts': posts, 'form': form, 'comments': comments})


@user_passes_test(lambda u: u.is_superuser)
def add_post(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect(post)
    return render(request, 'add_post.html', {'form': form})


def view_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        request.session["name"] = comment.name
        request.session["email"] = comment.email

        return redirect(request.path)
    form.initial['name'] = request.session.get('name')
    form.initial['email'] = request.session.get('email')

    return render(request, 'posts.html', {'post': post, 'form': form, })


def detail_post(request, slug):
    post = Post.objects.get(slug=slug)
    context = {
        'post': post,
    }
    return render(request, 'detail_post.html', context)


def add_comment(request, slug):
    post = get_object_or_404(Post, slug=slug)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        request.session["name"] = comment.name
        request.session["email"] = comment.email
        return redirect(reverse('list_posts'))

    form.initial['name'] = request.session.get('name')
    form.initial['email'] = request.session.get('email')

    return render(request, 'add_comment.html', {
                                          'post': post,
                                          'form': form,
                                      })