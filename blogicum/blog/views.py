from django.shortcuts import render, get_object_or_404
from blog.models import Post, Category


def index(request):
    template = 'blog/index.html'
    post = Post.published.select_related('category').filter(
        category__is_published=True
    )[:5]
    context = {'post_list': post}
    return render(request, template, context)


def post_detail(request, id):
    template = 'blog/detail.html'
    post = get_object_or_404(Post.published.select_related('category'),
                             pk=id, category__is_published=True)
    context = {'post': post}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category, slug=category_slug,
        is_published=True
    )
    post = Post.published.select_related('category').filter(
        category=category,
    )
    context = {'category': category, 'post_list': post}
    return render(request, template, context)
