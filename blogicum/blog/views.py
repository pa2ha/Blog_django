from django.shortcuts import render, get_object_or_404
from blog.models import Post, Category, Comment, User
from django.views.generic import (
    CreateView, DeleteView, ListView, UpdateView, DetailView)
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PostForm, CommentForm
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required


class index(ListView):
    model = Post
    template_name = 'blog/index.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_published=True,
                                   pub_date__lte=timezone.now(),
                                   category__is_published=True)
        queryset = queryset.order_by('-pub_date')
        return queryset


class profile(ListView):
    model = Post
    template_name = 'blog/profile.html'
    paginate_by = 10

    def get_queryset(self):
        username = self.kwargs['username']
        user = User.objects.get(username=username)
        return super().get_queryset().filter(author=user).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs['username']
        user = User.objects.get(username=username)
        context['profile'] = user
        return context


class edit_profile(UpdateView, LoginRequiredMixin):
    model = User
    template_name = 'blog/edit_profile.html'
    fields = '__all__'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('blog:profile',
                       kwargs={'username': self.object.username})


class create_post(CreateView, LoginRequiredMixin):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.author = self.request.user
            return super().form_valid(form)
        else:
            return redirect('login')

    def get_success_url(self):
        username = self.request.user.username
        success_url = reverse_lazy('blog:profile',
                                   kwargs={'username': username})
        return success_url


class edit_post(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'blog/create.html'
    fields = '__all__'
    pk_url_kwarg = 'pk'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            return HttpResponseRedirect(
                reverse('blog:post_detail', kwargs={'pk': post.pk})
            )
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        username = self.request.user.username
        return reverse('blog:profile', kwargs={'username': username})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id, author=request.user)

    if request.method == 'POST':
        post.delete()
        return redirect('blog:profile', username=request.user.username)

    return render(request, 'blog/create.html', {'post': post})


class post_view(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comments.select_related('author')
        return context


class add_comment(CreateView, LoginRequiredMixin):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/add_comment.html'

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        if self.request.user.is_authenticated:
            form.instance.post = post
            form.instance.author = self.request.user
            return super().form_valid(form)
        else:
            return HttpResponseRedirect(reverse_lazy('login'))

    def get_success_url(self):
        return reverse_lazy('blog:post_detail',
                            kwargs={'pk': self.kwargs['pk']})


class edit_comment(UpdateView, LoginRequiredMixin):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/edit_comment.html'
    context_object_name = 'comment'

    def dispatch(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.author != request.user:
            return HttpResponseRedirect(
                reverse_lazy('blog:post_detail',
                             kwargs={'pk': comment.post.pk}))
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail',
                            kwargs={'pk': self.object.post.pk})


class delete_comment(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'blog/confirm_delete_comment.html'
    context_object_name = 'comment'

    def dispatch(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.author != request.user:
            return redirect('blog:post_detail', pk=comment.post.pk)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        comment = self.get_object()
        return reverse('blog:post_detail', kwargs={'pk': comment.post.pk})


def post_detail(request, id):
    template = 'blog/detail.html'
    post = get_object_or_404(Post.is_published.select_related('category'),
                             pk=id, category__is_published=True)
    context = {'post': post}
    return render(request, template, context)


class category_posts(ListView):
    model = Post
    template_name = 'blog/category.html'
    paginate_by = 10

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        category = get_object_or_404(Category, slug=category_slug)
        queryset = super().get_queryset()
        queryset = queryset.filter(is_published=True, category=category)
        queryset = queryset.exclude(category__is_published=False)
        queryset = queryset.filter(pub_date__lte=timezone.now())
        queryset = queryset.order_by('-pub_date')
        return queryset

    def dispatch(self, request, *args, **kwargs):
        category_slug = self.kwargs['category_slug']
        category = get_object_or_404(Category, slug=category_slug)

        if not category.is_published:
            return HttpResponse("Category is not published", status=404)

        return super().dispatch(request, *args, **kwargs)
