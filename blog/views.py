
from django.shortcuts import render, get_object_or_404

from django.views.generic import ListView, DetailView
from django.utils.text import  slugify

from .models import Post, Category


class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    #def get_context_data(self, **kwargs):
      #  context = super(IndexView, self).get_context_data(**kwargs)
      #  cate = Category.objects
      #  context.update({'category': cate})
      #  return context


class CategoryView(ListView):
    model = Post
    template_name = 'blog/category.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)

    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        context.update({'category': cate})
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        self.object.increase_views()
        return response




