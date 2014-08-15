from django.db import models

# Create your models here.

import datetime
from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    # perex = models.TextField()
    content = models.TextField()

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('post', (self.slug, ), {})


class PostImage(models.Model):
    post = models.ForeignKey(Post)
    image = models.ImageField(upload_to="posts/image/")
    title = models.CharField(max_length=120, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __unicode__(self):
        return str(self.image)


class Comment(models.Model):
    name = models.CharField(max_length=42)
    email = models.EmailField(max_length=100)

    text = models.TextField()
    post = models.ForeignKey(Post, related_name='comments')
    created_on = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.text
