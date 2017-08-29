#coding:utf-8

from ccusers.models import MyUser
from django.contrib.auth.models import Group
from rest_framework.viewsets import ModelViewSet
from ccusers.api.serializers import UserSerializer, GroupSerializer

class UserSerializerViewSet(ModelViewSet):
    '''
    API endpoint that allows users to be viewed or edited.
    '''
    queryset = MyUser.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class GroupSerializerViewSet(ModelViewSet):
    '''
    API endpoint that allows groups to be viewed or edited.
    '''
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
