from django import forms
from .models import CommentModel, Post


class CongratulationForm(forms.ModelForm):
    class Meta:
        model = CommentModel
        fields = ('text',)


class PostForm(forms.ModelForm):
    # Удаляем все описания полей.

    # Все настройки задаём в подклассе Meta.
    class Meta:
        # Указываем модель, на основе которой должна строиться форма.
        model = Post
        fields = ('title', 'text', 'pub_date', 'category', 'location', 'image')
        # Указываем, что надо отобразить все поля.
        widgets = {
            'pub_date': forms.DateInput(attrs={'type': 'date'})}
