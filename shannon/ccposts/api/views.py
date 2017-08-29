#coding:utf-8

from ccposts.models import Article
from rest_framework.viewsets import ModelViewSet
from .serializers import PostDetailSerializer


class PostDetailSerializerViewSet(ModelViewSet):
    '''
    API endpoint that allows users to be viewed or edited.
    '''
    queryset = Article.objects.all().order_by('-last_modified_time')
    serializer_class = PostDetailSerializer
