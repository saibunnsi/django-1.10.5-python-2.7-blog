#coding:utf-8
from django import forms
from .models import Comment

class CommentForm(forms.Form):
   # class Meta:
    #    model = Comment
     #   fields = ['user', 'content']
    content_type = forms.CharField(widget=forms.HiddenInput, max_length=300)
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    parent_id = forms.IntegerField(widget=forms.HiddenInput, required=False)
    content = forms.CharField(widget=forms.Textarea)





