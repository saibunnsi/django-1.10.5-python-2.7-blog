#coding:utf-8
from collections import defaultdict
from math import ceil
from os.path import join

import markdown
from markdown.extensions.toc import TocExtension
from django.utils.text import slugify

from django.contrib.auth.decorators import login_required
from django.contrib.syndication.views import Feed #RSS feed
#from django.utils.feedgenerator import Rss201rev2Feed
#from .constants import SYNC_STATUS#
from django.contrib.contenttypes.models import ContentType

from django.http import HttpResponse, Http404
from django.shortcuts import render, render_to_response, redirect, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.views.generic.edit import FormView
from django.template import loader, Context

from ccposts.models import Article, Category, Tag,TagManager,ArticleImage
from comments.models import Comment
from comments.forms import CommentForm

from haystack.query import SearchQuerySet

def page_not_found(request):
    return render_to_response('ccposts/404.html')
def page_error(request):
    return render_to_response('ccposts/500.html')


def search_titles(request):
    posts = SearchQuerySet().autocomplete(content_auto=request.POST.get('search_text', ''))
    return render_to_response('search/ajax_search.html', {'posts': posts})


@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")

def index(request):
    article_list = Article.objects.all().order_by('-last_modified_time')[0:1]
    return render(request, 'ccposts/index.html', context={'article_list':article_list})

'''
class ArticleDetailView(generic.DetailView):
    model = Article
    template_name = 'ccposts/detail.html'
    context_object_name = 'article'

    def get(self, request, *args, **kwargs):
        response = super(ArticleDetailView, self).get(request, *args, **kwargs)
        self.object.increase_views()
        return response
        
    # 指定以上几个属性，已经能够返回一个DetailView视图了，为了让文章以markdown形式展现，我们重写get_object()方法。
    def get_object(self, queryset=None):
        article = super(ArticleDetailView,self).get_object(queryset=None)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
            TocExtension(slugify=slugify)
            ])
        article.body = md.convert(article.body)
        article.toc = md.toc
        return article    
'''

def ArticleDetailView(request, slug=None):
    instance = get_object_or_404(Article, slug=slug)
    initial_data = { "content_type": instance.get_content_type,"object_id": instance.id }
    form = CommentForm(request.POST or None, initial=initial_data)
    if form.is_valid() and request.user.is_authenticated():
        c_type = form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=c_type)
        obj_id = form.cleaned_data.get('object_id')
        content_data = form.cleaned_data.get("content")
        parent_obj = None
        try:
            parent_id = int(request.POST.get("parent_id"))
        except:
            parent_id = None
        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()
        new_comment, created = Comment.objects.get_or_create(
                        user = request.user,
                        content_type = content_type,
                        object_id = obj_id,
                        content = content_data,
                        parent = parent_obj,
        )
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())
    comments = instance.comments

    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite(linenums=True)',
        'markdown.extensions.toc',
        TocExtension(slugify=slugify,permalink=True)
    ])
    instance.body = md.convert(instance.body)

    context = {
        "title": instance.title,
        "instance": instance,
        "toc": md.toc,
        "comments": comments,
        "comment_form":form,
        }
    return render(request, "ccposts/detail.html", context=context)

#class ExtendedRSSFeed(Rss201rev2Feed):
class RSSFeed(Feed):
    title = "AZI"
    link = "ccposts/RSS/"
    description ="AZI RSS Feed"
    def items(self):
        return Article.objects.order_by('-last_modified_time')
    def item_title(self, item):
        return item.title
    def item_last_modified_time(self, item):
        return item.last_modified_time
    def item_description(self, item):
        return item.body
    '''
    加此项后显示 No match reverse error
    def item_link(self, item):
        return reverse('article-item', args=[item.pk])
    '''

def AboutMe(request):
    return render(request, 'ccposts/aboutme.html')

class CategoryView(generic.ListView):
    model = Article
    template_name = "ccposts/category.html"
    context_object_name = "article_list"
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)
'''
def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    article_list = Article.objects.filter(category=cate).order_by('-created_time')
    return render(request, 'ccposts/base.html', context={'article_list':article_list})
'''

'''
    def get_queryset(self):
        category_article_list = Article.objects.filter(category=self.kwargs['cate_id'],status='p')
        # 注意在url里我们捕获了分类的id作为关键字参数（cate_id）传递给了CategoryView，传递的参数在kwargs属性中获取。
        for article in category_article_list:
            article.body = markdown2.markdown(article.body, extras=['fenced-code-blocks'],)
        return category_article_list
    
    # 给视图增加额外的数据
    def get_context_data(self, **kwargs):
        kwargs['category_list'] = Category.objects.all().order_by('categoryname')
        # 增加一个category_list,用于在页面显示所有分类，按照名字排序
        return super(CategoryView, self).get_context_data(**kwargs)
'''

class TagView(generic.ListView):
    model = Article
    template_name = "ccposts/tag.html"
    context_object_name = "article_list"

    def get_queryset(self):
        # my_blog_tags = Article.objects.filter(tags=self.kwargs['tag_id'], status='p')
        # for article in my_blog_tags:
        #   article.body = markdown2.markdown(article.body, extras=['fenced-code-blocks'])
        # return my_blog_tags
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        # def get_context_data(self, **kwargs):
        return super(TagView, self).get_queryset().filter(tags=tag)

'''  
class ArchiveView(generic.ListView):
    model = Article
    template_name = "ccposts/article_by_date.html"
    context_object_name = "article_list"

    def get_queryset(self):
        # 接收从url传递的year和month参数，转为int类型
        year = int(self.kwargs['year'])
        month = int(self.kwargs['month'])
        day = int(self.kwargs['day'])
        # 按照year和month过滤文章
        article_list = Article.objects.filter(created_time__year=year, created_time__month=month, created_time__day=day)
        for article in article_list:
            article.body = markdown2.markdown(article.body, extras=['fenced-code-blocks'], )
        return article_list

    def get_context_data(self, **kwargs):
        kwargs['tag_list'] = Tag.objects.all().order_by('tagname')
        return super(ArchiveView, self).get_context_data(**kwargs)
'''

class Archive(generic.ListView):
    model = Article
    template_name = "ccposts/archive.html"
    context_object_name = "article_list"

    #def get_context_data(request, year, **kwargs):
     #   article_list = Article.objects.filter(created_time__year=year).order_by('-last_modified_time')
        #created_time__month=month#不删掉月份无法返回相应档案信息，暂时还不清楚为什么！
       # context={'article_list': article_list}
      #  return render(request, 'ccposts/archive.html', context)


def archives(request, year, month):
    article_list = Article.objects.filter(created_time__year=year).order_by('-last_modified_time')
    #created_time__month=month#不删掉月份无法返回相应档案信息，暂时还不清楚为什么！
    context={'article_list': article_list}
    return render(request, 'ccposts/archivebydate.html', context)
