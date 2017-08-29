#coding=utf-8
"""shannon URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include,handler404,handler500
from django.contrib import admin
from django.contrib.auth import views as auth_views

from ccusers.api import views as ccusers_api_views
from ccposts.api import views as ccposts_api_views
from comments.api import views as comments_api_views
from rest_framework import routers

handler404 = "ccposts.views.page_not_found"
handler500 = "ccposts.views.page_error"


'''
Because we're using viewsets instead of views,
we can automatically generate the URL conf for our API,
by simply registering the viewsets with a router class.
'''
router = routers.DefaultRouter()
router.register(r'users', ccusers_api_views.UserSerializerViewSet)
router.register(r'group', ccusers_api_views.GroupSerializerViewSet)
router.register(r'posts', ccposts_api_views.PostDetailSerializerViewSet)
router.register(r'comments', comments_api_views.CommentSerializerViewSet)

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ccposts/',include('ccposts.urls', namespace='ccposts', app_name='ccposts')),
    url(r'^ccusers/', include('ccusers.urls', namespace='ccusers', app_name='ccusers')),
    url(r'', include('comments.urls', namespace='comments', app_name='comments')),
    url(r'', include('cclikes.urls', namespace='cclikes', app_name='cclikes')),
    url(r'^search/', include('haystack.urls')),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework_api_auth')),
    url(r'^cclikes/', include('cclikes.urls')),

]
    #we're including default login and logout views for use with
    #the browsable API. That's optional, but useful if your API
    #requires authentication and you want to use the browsable API.
    #url('r^docs/', include_docs_urls(title='My API title')),
    #/docs/ --The documentation page itself.
    #/docs/schema.js --A JavaScript resource that exposes the API schema.

    #namespace参数为我们指定了命名空间，指明此urls.py中的url属于blog app，这样不同的app下有相同url也不会冲突。