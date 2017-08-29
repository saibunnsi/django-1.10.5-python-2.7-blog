#coding:utf-8
from __future__ import unicode_literals
from django.conf import settings
from django.contrib import admin

from unidecode import unidecode
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from django.db import models
#from ccposts.models import Article
#from django.utils.six import python_2_unicode_compatible

class CommentManager(models.Manager):
    def all(self):
        qs = super(CommentManager, self).filter(parent=None)
        return qs

    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        qs = super(CommentManager, self).filter(content_type=content_type,object_id=obj_id).filter(parent=None)
        return qs


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()#Give your model a field that can store primary key values from the models you’ll be relating to
    content_object = GenericForeignKey('content_type', 'object_id')
    parent = models.ForeignKey('self', null=True, blank=True)
    content = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    objects = CommentManager()

    class Meta:
        ordering = ['-created_time']

    def __unicode__(self):
        return self.content[0:20]

    def children(self):#replies
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        else:
            return True

class CommentAdmin(admin.ModelAdmin):
    list_display = ('object_id','user','created_time')
admin.site.register(Comment, CommentAdmin)