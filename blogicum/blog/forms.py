from django import forms
from .models import Comment, Post, User


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


class PostForm(forms.ModelForm):
    # Удаляем все описания полей.

    # Все настройки задаём в подклассе Meta.
    class Meta:
        # Указываем модель, на основе которой должна строиться форма.
        model = Post
        exclude = ('is_published', 'author')
        # Указываем, что надо отобразить все поля.
        widgets = {
            'pub_date': forms.DateInput(attrs={'type': 'date'})}


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'last_name', 'first_name')
