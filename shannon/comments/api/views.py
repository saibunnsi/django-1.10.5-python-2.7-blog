#coding:utf-8

from comments.models import Comment

from rest_framework.viewsets import ModelViewSet
from comments.api.serializers import CommentSerializer

class CommentSerializerViewSet(ModelViewSet):
    '''
    API endpoint that allows users to be viewed or edited.
    '''
    queryset = Comment.objects.all().order_by('-created_time')
    serializer_class =  CommentSerializer


