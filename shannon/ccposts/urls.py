#coding:utf-8
from django.conf.urls import url
from ccposts import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^article/(?P<slug>[\w-]+)/$', views.ArticleDetailView, name='detail'),
    url(r'^aboutme/$', views.AboutMe, name='aboutme'),
    url(r'^category/(?P<pk>[0-9]+)/$', views.CategoryView.as_view(), name='category'),
    url(r'^archive/$', views.Archive.as_view(), name='archive'),
    url(r'^archive/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.archives, name='archivebydate'),
    url(r'^tag/(?P<pk>[0-9]+)/$', views.TagView.as_view(), name='tag'),
    url(r'^RSS/$', views.RSSFeed(), name='RSS'),
    url(r'^ajax_search/$', views.search_titles, name='ajax_search'),
]
    #使用(?P<>\d+)的形式捕获值给<>中得参数，比如(?P<article_id>\d+)，
    #当访问/blog/article/3时，将会将3捕获给article_id,这个值会传到
    #views.ArticleDetailView,这样我们就可以判断展示哪个Article了
