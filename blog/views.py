from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from datetime import datetime
from django.contrib import messages
from .models import Post, Category, Message
from .form import RegisterForm
from django.contrib.auth.decorators import login_required,permission_required
import markdown
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


def check(body, type):
    if type == 'body':
        danger_list = ['/', '<', '>', '#', '*', '(', ')', '"', "'"]
        for i in range(len(danger_list)):
            if danger_list[i] in body:
                return True
    return False


def page_not_found(request):
    return render(request, 'blog/errors/404.html')


def forbidden(request):
    return render(request, 'blog/errors/403.html')


def server_error(request):
    return render(request, 'blog/errors/500.html')


class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'


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


def detail(request,pk):
    post = get_object_or_404(Post, pk=pk)
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ])
    post.increase_views()
    return render(request, 'blog/detail.html', context={'post': post})


def search(request):
    if request.method == 'POST':
        body = request.POST['body']
        if check(body, 'body'):
            messages.error(request, '你想干嘛？？？？')
            return render(request, 'blog/search.html',)

        else:
            result_list = Post.objects.filter(body__contains=body)
            result_list2 = Post.objects.filter(title__contains=body)
            result_list = (result_list | result_list2).distinct()
            return render(request, 'blog/category.html', context={'post_list': result_list,
                                                                  'result': body + '的搜索结果'})
    else:
        return render(request, 'blog/search.html', )


def outside(request):
    return render(request, 'blog/outside.html')


def message(request):
    message_list = Message.objects.all()
    if request.method == 'POST':
        body = request.POST['body']
        if check(body, 'body'):
                messages.error(request,'你又想干啥？？？')
                return render(request, 'blog/message.html', context={'message_list': message_list})
        else:
            message = Message.objects.create(body=body, created_time=datetime.utcnow())
            message.save()
            return render(request, 'blog/message.html', context={'message_list': message_list})
    else:
        message_list = Message.objects.all()
        return render(request, 'blog/message.html', context={'message_list': message_list})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '注册成功')
        return render(request, 'blog/register.html', context={'form':form})

    else:
        return render(request, 'blog/register.html')


@login_required(login_url='/')
@permission_required('Can_add_post', raise_exception=True)
def edit(request, pk):
    post = Post.objects.get(id=pk)
    if request.method == 'POST':
        body = request.POST['body']
        post.body = body
        post.save()
        return HttpResponseRedirect(reverse('blog:detail', kwargs={'pk': pk}))
    else:
        return render(request, 'blog/edit_post.html', context={'post': post})


@login_required(login_url='/')
@permission_required('post:Can_add_post', raise_exception=True)
def create(request):
    if request.method == 'POST':
        body = request.POST['body']
        title = request.POST['title']
        category = int(request.POST['category'])
        category = Category.objects.get(id=category)
        post = Post.objects.create(title=title, body=body, category=category,created_time=datetime.utcnow(),
                                   author=request.user, modified_time=datetime.utcnow())
        post.save()
        messages.success(request, '发表成功')
        post = Post.objects.get(id=post.id)
        post.body = markdown.markdown(post.body,
                                      extensions=[
                                          'markdown.extensions.extra',
                                          'markdown.extensions.codehilite',
                                          'markdown.extensions.toc',
                                      ])
        return render(request, 'blog/detail.html', context={'post': post})
    else:
        return render(request, 'blog/create_post.html')


@login_required(login_url='/')
@permission_required('post.Can_add_post', raise_exception=True)
def delete(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.method == 'POST':
        category = post.category
        Post.objects.filter(id=post.pk).delete()
        post_list = Post.objects.filter(category=category)
        return render(request, 'blog/category.html', context={'category': category,
                                                              'post_list': post_list})
    else:
        return render(request, 'blog/delete.html', context={'post': post})





