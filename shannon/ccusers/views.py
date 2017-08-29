#coding:utf-8
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, get_user_model, logout
from django.core.mail import send_mail
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render, redirect
from .forms import UserCreationForm, UserLoginForm
from .models import MyUser

User = get_user_model()

def register(request):
    # redirect_to = request.POST.get('next', request.GET.get('next',''))
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user_ = form.save(commit=False)
            user_.save()
            id_ = user_.id
            to_email=user_.email
            from_email = settings.EMAIL_HOST_USER
            to_list = [to_email, id_, settings.EMAIL_HOST_USER]
            text = "Hi\nHow are you?\nHere is the link to activate your account:\nhttp://127.0.0.1:8000/ccusers/register_activate/activation/?id=%s" %(id_)
            part1 = MIMEText(text, 'plain')
            message = MIMEMultipart('alternative')
            message.attach(part1)
            subject = "Activate your account at AZI !"
            message = """\nFrom: %s\nTo: %s\nSubject: %s\n\n%s""" %(from_email, to_email,subject, message.as_string())
            send_mail(subject, message, from_email, to_list, fail_silently=False)
            messages.success(request, 'Thank you for your registration! Have a good day!')

            #messages在重定向后的页面显示，需在相应template中添加相关信息！！！
            #return HttpResponseRedirect('register_success_view')
            #return render(request, 'ccusers/register_activation_complete.html')
            return redirect('../../ccusers/register_guide_message/')
        return redirect('ccusers:activate_guide')

            #注意还要添加------并给出前往邮箱激活账号的信息，注册信息完成后重定向回首页！
    else:
        form = UserCreationForm()
    return render(request, 'ccusers/register.html', context={'form':form})

def activate_guide_view(request):
    return render(request, 'ccusers/register_activation_guide.html')

def activate_view(request):
    id=int(request.GET.get('id'))
    user = MyUser.objects.get(id=id)
    user.is_active=True
    user.save()
    return render(request, 'ccusers/register_activation_complete.html')


def login_view(request, *args, **kwargs):
    redirect_to = request.POST.get('next', request.GET.get('next',''))
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        user_obj = form.cleaned_data.get('user_obj')
        login(request, user_obj)
        if redirect_to:
            return redirect(redirect_to)
        else:
            return redirect('../../ccposts/')
    return render(request, "ccusers/login.html", context={"form":form, 'next':redirect_to})

def logout_view(request):
    redirect_to = request.GET.get('next', request.GET.get('next',''))
    logout(request)
    if redirect_to:
        return redirect(redirect_to)
    else:
        return redirect('/')