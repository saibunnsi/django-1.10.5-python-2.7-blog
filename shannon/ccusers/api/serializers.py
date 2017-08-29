#coding:utf-8
from django.contrib.auth.models import Group
from ccusers.models import MyUser
from rest_framework.serializers import ModelSerializer

class UserSerializer(ModelSerializer):
    # hyperlinking is good RESTful design

    class Meta:
        model = MyUser
        fields = '__all__'
        #set the fields attribute to the special value '__all__' to indicate that all fields in the model should be used.
        #OR : exclude = ('field')set the exclude attribute to a list of fields to be excluded from the serializer.
        #field = ('url', 'username', 'email', 'groups')


class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields ='__all__'
        #fields = ('url', 'name')

