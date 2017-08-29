#coding:utf-8
import datetime
from haystack import indexes
from ccposts.models import Article


class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    last_modified_time = indexes.DateTimeField(model_attr='last_modified_time')
    content_auto = indexes.EdgeNgramField(model_attr='title')

    def get_model(self):
        return Article

    def index_queryset(self, using=None):
        return self.get_model().objects.all()#filter(last_modified_time__lte=datetime.datetime.now())
        # 确定在建立索引时有些记录被索引，这里简单返回所有记录。