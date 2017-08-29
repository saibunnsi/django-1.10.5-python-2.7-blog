#coding:utf-8

from comments.models import Comment
from rest_framework.serializers import ModelSerializer

class CommentSerializer(ModelSerializer):
    # hyperlinking is good RESTful design

    class Meta:
        model = Comment
        fields = '__all__'
        #set the fields attribute to the special value '__all__' to indicate that all fields in the model should be used.
        #OR : exclude = ('field')set the exclude attribute to a list of fields to be excluded from the serializer.
        #field = ('url', 'username', 'email', 'groups')


