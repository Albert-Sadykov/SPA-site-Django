from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Post
from .forms.authentication_form import SignUpForm, SignInForm
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from .utils.function_monitor_logger import log_operations
from django.contrib.auth.views import LogoutView
# Create your views here.

class MainView(View):
    @log_operations
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all().order_by('-created_at')
        paginator = Paginator(posts, 6)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(
            request,
            'index.html',
            context={
                'page_obj': page_obj
            }
        )
    
class PostDetailView(View):
    @log_operations
    def get(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, url=slug)
        return render(
            request,
            'post_detail.html',
            context={
                'post': post
            }
        )
    
class SignUpView(View):
    @log_operations
    def get(self, request, *args, **kwargs):
        form = SignUpForm()
        return render(request, 'signup.html', context={
            'form': form,
        })

    @log_operations
    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect('/')
            except IntegrityError:
                form.add_error('username', 'Пользователь с таким именем уже существует')
                return render(
                        request, 
                        'signup.html', 
                        context={
                            'form': form,
                        }
                    )
        return render(
                request, 
                'signup.html', 
                context={
                    'form': form,
                }
            )
    
class SignInView(View):
    @log_operations
    def get(self, request, *args, **kwargs):
        form = SignInForm()
        return render(
            request,
            'signin.html',
            context={
                'form': form,
            }
        )
    
    @log_operations
    def post(self, request, *args, **kwargs):
        form = SignInForm(request.POST)

        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                form.add_error(None, 'Неверный логин или пароль')

                return render(
                    request, 
                    'signin.html',
                    context={
                        'form': form,
                    }
                )

        form.add_error(None, 'Ошибка валидации формы')
        return render(
            request,
            'signin.html',
            context={
                'form': form
            }
        )

class SignOutView(View):
    @log_operations
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect('/')
    
    @log_operations
    def post(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect('/')