#coding:utf-8
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from ccposts.models import Article

#有新评论发邮件
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt

from django.contrib.contenttypes.models import ContentType
from .models import Comment
from .forms import CommentForm

# Create your views here.


