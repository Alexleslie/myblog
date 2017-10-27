
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView

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
    paginate_by = 10

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


def search(request):
    if request.method == 'POST':
        body = request.POST['body']
        danger_list= ['/','<','>','#','*','(',')','union','and','order']
        for i in range(len(danger_list)):
            if danger_list[i] in body:
                return render(request, 'blog/search.html', context={'result': '你想干嘛？？？注意一点'})
        else:
            result_list = Post.objects.filter(body__contains=body)
            result_list2 = Post.objects.filter(title__contains=body)
            result_list = (result_list | result_list2).distinct()

            return render(request, 'blog/category.html', context={'post_list':result_list,
                                                                  'result': body +'的搜索结果'})

    else:
        return render(request, 'blog/search.html', )


