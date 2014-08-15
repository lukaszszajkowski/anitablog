from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

  # Examples:
    url(r'^$', 'blog.views.home', name='home'),
    #url(r'^blog/$', 'blog.views.blog', name='blog'),
    url(r'^blog/$', 'blog.views.list_posts', name='list_posts'),
    #url(r'^blog/(?P<slug>.*)$', 'articles.views.list_posts', name='list_posts'),
    url(r'^blog/(?P<slug>[-\w]+)$', 'blog.views.view_post',name='post'),
    url(r'^add/post$', 'blog.views.add_post', name='add_post'),
    # url(r'^blog/', include('blog.urls')),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^admin/', include(admin.site.urls)),

)
