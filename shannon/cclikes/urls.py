#coding:utf-8
from django.conf.urls import url
from cclikes import views

urlpatterns = [
    url(
        r"^like/(?P<content_type>[\w-]+)/(?P<id>\d+)/(?P<vote>-?\d+)/$",
        views.like,
        name="like"
    )
]