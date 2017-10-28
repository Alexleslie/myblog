
from django.shortcuts import render, get_object_or_404,render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView
from datetime import datetime
from django.contrib import messages
from .models import Post, Category, Message
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, user_logged_in
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from .form import RegisterForm, SearchForm
from django.contrib.auth.forms import UserCreationForm


def check(body,type):
    if type == 'body':
        danger_list = ['/', '<', '>', '#', '*', '(', ')', '"', "'"]
        for i in range(len(danger_list)):
            if danger_list[i] in body:
                return True
    return False


def page_not_found(request):
    return render(request, 'blog/errors/404.html')


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
        if check(body, 'body'):
            messages.error(request, '你想干嘛？？？？')
            return render(request, 'blog/search.html',)

        else:
            result_list = Post.objects.filter(body__contains=body)
            result_list2 = Post.objects.filter(title__contains=body)
            result_list = (result_list | result_list2).distinct()

            return render(request, 'blog/category.html', context={'post_list':result_list,
                                                                  'result': body +'的搜索结果'})
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

        return render(request, 'blog/register.html',context={'form':form})

    else:
        return render(request, 'blog/register.html')


'''def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if check(username, 'username'):
            messages.error(request, '用户名不规范')
            return render(request, 'blog/login.html')
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
'''







