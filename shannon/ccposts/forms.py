
#coding:utf-8
#coding:utf-8
'''
from django import forms
from django.contrib.auth.models import User
from .models import Article, Comment #UserProfile

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_username', 'comment_email', 'comment_content']
        widgets = {
            'comment_username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "请输入昵称",
                'aria-describedby':"sizing-addon1",
                }),
            'comment_email': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "请输入邮箱",
                'aria-describedby': "sizing-addon1",
                }),
            'comment_content': forms.Textarea(attrs={'placeholder':"我来评两句~"}),
            }

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
#UserForm包含一个定义password属性.当User模型实例默认包含password属性时,
#HTML表单元素将不会隐藏密码.如果用户输入密码,那么这个密码就会可见.
#所以我们修改password属性作为CharField实例并使用PasswordInput()组建,这时用户输入就会被隐藏.
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
'''
'''
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('personal_website', 'picture')
'''
#在Meta类中所有定义都会被当做它的附加属性.每个Meta至少包含一个model字段,
#它可以和模型之间关联.例如在我们的UserForm类中就关联了User模型.
#在Django1.7中你可以用fields或者exclude来定义你需要展示的字段.
