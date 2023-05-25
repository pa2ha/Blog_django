from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post, Comment
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CongratulationForm, PostForm
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin



class index(ListView):
    model = Post
    template_name = 'blog/index.html'
    paginate_by = 10


    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_published=True, pub_date__lte=timezone.now(), category__is_published=True)
        return queryset




class create_post(CreateView, LoginRequiredMixin):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'



class edit_post(UpdateView,LoginRequiredMixin):
    model = Post
    template_name = 'blog/create.html'
    fields = '__all__'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # Обработка случая, когда пользователь не авторизован
            # Например, можно перенаправить на страницу входа
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)



class delete_post(DeleteView, LoginRequiredMixin):
    model = Post
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')

        
class edit_profile(UpdateView):
    model = User
    template_name = 'blog/profile.html'
    fields = '__all__'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # Если пользователь не авторизован, перенаправляем на страницу входа
            return redirect('login')
        
        return super().dispatch(request, *args, **kwargs)


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()

    if request.method == 'POST':
        form = CongratulationForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = CongratulationForm()

    return render(request, 'blog/detail.html', {'post': post, 'comments': comments, 'form': form})



def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        form = CongratulationForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = CongratulationForm()

    return render(request, 'blog/add_comment.html', {'post': post, 'form': form})


def edit_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        form = CongratulationForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', pk=post_id)
    else:
        form = CongratulationForm(instance=comment)
    
    return render(request, 'blog/edit_comment.html', {'form': form, 'comment': comment})


def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

    if request.method == 'POST' and request.user == comment.author:
        comment.delete()
        return redirect('blog:post_detail', pk=post_id)

    return render(request, 'blog/confirm_delete_comment.html', {'comment': comment})








class category_posts(ListView):
    model = Post
    template_name = 'blog/category.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_published=True)
        queryset = queryset.exclude(category__is_published=False)
        return queryset
    

class profile_view(LoginRequiredMixin,ListView):
    model = Post
    template_name = 'blog/profile.html'
    paginate_by = 10

    def get_queryset(self):
        username = self.kwargs['username']
        user = User.objects.get(username=username)
        return super().get_queryset().filter(author=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs['username']
        user = User.objects.get(username=username)
        context['profile'] = user
        
        return context