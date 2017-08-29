#coding:utf-8
import os
import datetime
import secretballot

from django.db import models
from django.db.models import IntegerField 
from django.utils import timezone

#for slug, get_absolute_url
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse

from collections import defaultdict

#delete md_file before delete/change model
from django.conf import settings
from django.db.models.signals import pre_delete
from django.db.models import F

from django.dispatch import receiver
from django.core.files.base import ContentFile

#from django.contrib.auth.models import User
#from django.contrib.auth import authenticate

from unidecode import unidecode
from taggit.managers import TaggableManager

from django.contrib.contenttypes.models import ContentType
from comments.models import Comment


#from django.utils.safestring import mark_safe
#from markdown_deux import markdown


upload_dir = 'content/Article/%s/%s'


#标签操作模型
class TagManager(models.Manager):
    @property
    def get_tag_list(self): #返回文章标签列表，每个标签以及对应的文章数目
        tags = Tag.objects.all()#获取所有标签
        taglist = []
        for i in range(len(tags)):
            taglist.append([])
        for i in range(len(tags)):
            temp = Tag.objects.get(tagname=tags[i])#获取当前标签
            posts = temp.article_set.all()#获取当前标签下的所有文章
            taglist[i].append(tags[i].tagname)
            taglist[i].append(len(posts))
        return taglist

#标签模型    
class Tag(models.Model):
    class Meta:
        ordering = ['tagname']
    
    objects = models.Manager()
    tagname = models.CharField(verbose_name='标签名', max_length=30)
    tag_list = TagManager()#自定义的管理器
    articlecount = models.IntegerField(verbose_name='标签下文章数', default=0)#???

    def __unicode__(self):
        return self.tagname

#博文操作模型
class ArticleManager(models.Manager):
    """
    继承自默认的 Manager ，为其添加一个自定义的 archive 方法
    """
    def archive(self):
        date_list = Article.objects.datetimes('created_time', 'month','day', order='DESC')
        # 获取到降序排列的精确到月份且已去重的文章发表时间列表
        # 并把列表转为一个字典，字典的键为年份，值为该年份下对应的月份列表
        date_dict = defaultdict(list)
        for d in date_list:
            date_dict[d.year].append(d.month)
        # 模板不支持defaultdict，因此我们把它转换成一个二级列表，由于字典转换后无序，因此重新降序排序
        return sorted(date_dict.items(), reverse=True)

#md文件上传
def get_upload_md_name(self, filename):
    if self.created_time:
        year = self.created_time.year # always store in created_year folder
    else:
        year = datetime.now().year
        upload_to = upload_dir % (year, self.title + '.md')
        return upload_to
#html文件上传
def get_html_name(self, filename):
    if self.created_time:
        year = self.created_time.year
    else:
        year = datetime.now().year
        upload_to = upload_dir % (year, filename)
        return upload_to

#博文模型
class Article(models.Model):
    class Meta:
        ordering = ['-last_modified_time']

    STATUS_CHOICES = (
        ('d', 'Draft'),
        ('p', 'Published'),
    )
    objects = ArticleManager()
    title = models.CharField(verbose_name='标题', max_length=150)
    body = models.TextField(verbose_name='正文', blank=True)
    abstract = models.CharField(verbose_name='摘要', max_length=200,blank=True, help_text="If possible, use the first 200 words.")
    created_time = models.DateTimeField(verbose_name='创建时间',default=timezone.now) #auto_now_add=True)
    last_modified_time = models.DateTimeField(verbose_name='上次修改时间', auto_now=True)
    tags = models.ManyToManyField(Tag, verbose_name='标签', blank=True)
    category = models.ForeignKey('Category', verbose_name='目录')#, blank=True,default=True)
    status = models.CharField(verbose_name='文章状态', max_length=1, choices=STATUS_CHOICES)
    slug = models.SlugField(unique=True)#(default=None, max_length=200, blank=True)#???
    commentcount = models.PositiveIntegerField(verbose_name='评论', blank=True, default=0)
    views = models.PositiveIntegerField(verbose_name='浏览量', blank=True, default=0)
    likes = models.PositiveIntegerField(verbose_name='点赞数', blank=True, default=0)
    topped = models.NullBooleanField(verbose_name='置顶', default=True)
    html_file = models.FileField(verbose_name='上传html文件', upload_to=get_html_name, blank=True)#generated html file
    md_file = models.FileField(verbose_name='上传md文件', upload_to=get_upload_md_name, blank=True)#uploaded md file    

    def get_absolute_url(self):
        return reverse('ccposts:detail', kwargs={'slug': self.slug})
        #点击提交评论表单后，返回当前页面！

    def gettags(self):#返回一个文章对应的所有标签
        tag = self.tags.all()
        return tag


    def increase_views(self):
        #instance = self
        #instance.views = F('views') + 1
        #instance.views += 1
        #instance.save(update_fields=['views'])
        #return instance.views

        self.views += 1
        #Pay attention to F expression!!!It does not work here, Why???
        self.save(update_fields=['views'])
        #use save(update_fields=[])to avoid 并行save产生的数据冲突！
        return self.views

    def __unicode__(self):
        # 主要用于交互解释器显示表示该类的字符串
        return self.title

    @property #dispaly comments!
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

    @property #Create Comments!
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type
'''
    #model直接生成markdown.body，本博中采用另一种markdown.extensions在views中生成。
    def get_markdown(self):
        content = self.body
        markdown_text = markdown(content)
        return mark_safe(markdown_text)
'''


secretballot.enable_voting_on(Article)
#attach the voting helpers to a particular model it is enough to call
#secretballot.enable_voting_on passing the model class.




def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Article.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def get_upload_img_name(self, filename):
    upload_to = upload_dir % ('images', filename)  # filename involves extension
    return upload_to
#博文图片模型
class ArticleImage(models.Model):
    article = models.ForeignKey(Article, related_name='images')
    image = models.ImageField(upload_to=get_upload_img_name)
    upload_time = models.DateTimeField(verbose_name="上传时间", auto_now_add=True)


#博文目录模型
class Category(models.Model):
    categoryname = models.CharField(verbose_name='目录名称', max_length=30)
    articlecount = models.IntegerField(verbose_name='文章篇数',default=0)
    created_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    last_modified_time = models.DateTimeField(verbose_name='修改时间', auto_now=True)

    def __unicode__(self):
        return self.categoryname