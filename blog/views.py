from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.template import RequestContext

from .models import Post, Comment
from .forms import PostForm, CommentForm

def home(request):
    return render(request, 'index.html', {'test': "test"})

def list_posts(request):
    form = PostForm(request.POST or None)
    posts = Post.objects.all()
    comments = Comment.objects.all()
    return render_to_response('posts.html', {'posts':posts,
                                             'form': form,
                                             'comments': comments}, context_instance=RequestContext(request))


@user_passes_test(lambda u: u.is_superuser)
def add_post(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect(post)
    return render_to_response('add_post.html',
                              { 'form': form },
                              context_instance=RequestContext(request))

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

    return render_to_response('posts.html',
                              {
                                  'post': post,
                                  'form': form,
                              },
                              context_instance=RequestContext(request))

