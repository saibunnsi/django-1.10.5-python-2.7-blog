#coding:utf-8

from ccposts.models import Article
from rest_framework.serializers import ModelSerializer

class PostDetailSerializer(ModelSerializer):
    # hyperlinking is good RESTful design

    class Meta:
        model = Article
        fields = '__all__'
        #set the fields attribute to the special value '__all__' to indicate that all fields in the model should be used.
        #OR : exclude = ('field')set the exclude attribute to a list of fields to be excluded from the serializer.
        #field = ('url', 'username', 'email', 'groups')

