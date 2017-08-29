#coding:utf-8
from django.contrib import admin

#(    password_reset, password_reset_done, password_reset_confirm,
#    password_reset_complete
#)
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from . import views

#“邮件密码重置”部分采用了django内置的模块，为了和登录注册统一，让整套Authentication系统呈现得更清楚，
#此部分urls放在本应用（ccusers.urls）下，相应templates放在模板文件夹ourusers（templates/ccusers）下，即auth_views中相应模板路径全部需要修改！！！
#而auth_views中类似reverse('password_reset_done')部分也须修改成reverse('ccusers:password_reset_done')，否则会返回reverse错误！！！

app_name = 'ccusers'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^register/$', views.register, name="register"),
    url(r'^login/$', views.login_view, name="login"),
    url(r'^logout/$', views.logout_view, name="logout"),
    url(r'^register_activate/activation/$',views.activate_view, name='activation'),
    #url(r'^activate/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/(?P<uid64>[0-9A-Za-z_\-]+)/$',
     #   views.activation, name='activation'),
    url(r'^register_guide_message/$', views.activate_guide_view, name='activate_guide'),
   # url(r'^activate/(?P<code>[a-z0-9].*)/$', views.activate_user_view, name="user_activate"),



    url(r'^reset_password/$', auth_views.password_reset, name='password_reset'),
    url(r'^reset_password/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset_password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset_password/complete/$', auth_views.password_reset_complete, name='password_reset_complete'),
    ]




