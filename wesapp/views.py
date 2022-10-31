from dataclasses import field
from pdb import post_mortem
from urllib import response

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
# Create
from django.http import HttpResponse, HttpResponseRedirect
# your views here.
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from .models import Contact
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from .models import Post, Comment
import requests
API_KEY = '2c0f2edec2944d49a72c0fb05ad44397'

# def HomeView(ListView):
#     model = Post
#     template_name = 'feed.html'


class HomeView(ListView):
    model = Post
    template_name = 'feed.html'


# def header_image(self):
#     if self.image and hasattr(self.image, 'url'):
#         return self.image.url


def home(request):
    return render(request, 'home.html')


def premium_access(request):
    return render(request, 'premium_access.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = f'Welcome to WeStocks ,{name}'
        message = 'We got your problem,we will try to communicate with you within 24 hours, Thanks'
        recepient = email
        send_mail(subject, message, settings.EMAIL_HOST_USER,
                  [recepient], fail_silently=False)
        phone = request.POST['phone']
        content = request.POST['content']

        if len(name) < 2 or len(email) < 3 or len(phone) < 10 or len(content) < 4:
            messages.error(request, "Please fill the form correctly")
        else:
            contact = Contact(name=name, email=email,
                              phone=phone, content=content)
            contact.save()
            messages.error(request, 'your message has been successfully sent')

    return render(request, 'contact.html')


def news(request):
    url = f'https://newsapi.org/v2/everything?q=market&apiKey={API_KEY}'
    data = requests.get(url)
    response = data.json()
    articles = response['articles']
    context = {'articles': articles}
    return render(request, 'news.html', context)


def like_post(request):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked = False
    else:
        post.likes.add(request.user)
        is_liked = True
    return HttpResponseRedirect(reverse('feed'))


def home_body(request):
    return render(request, 'home_body.html')


def about(request):
    return render(request, 'about.html')


def feed(request, id, slug):
    post = get_object_or_404(Post, id=id, slug=slug)
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        is_liked = True
    context = {
        'post': post,
        'is_liked': is_liked,
        'total_likes': post.total_likes,
    }

    return render(request, 'feed.html', context)


def footer(request):
    return render(request, 'footer.html')


def home01(request):
    return render(request, 'home01.html')


def subscription(request):
    return render(request, 'subscription.html')


def profile(request):
    return render(request, 'profile.html')


def register(request):

    if request.method == 'POST':

        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        subject = 'Welcome to WeStocks'
        message = 'Thank you for joining us'
        recepient = email
        send_mail(subject, message, settings.EMAIL_HOST_USER,
                  [recepient], fail_silently=False)
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username is already exist')
                return redirect(register)
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email is already exist')
                return redirect(register)
            else:
                user = User.objects.create_user(
                    username=username, password=password, email=email, first_name=first_name, last_name=last_name)
                user.set_password(password)
                user.is_staff = True
                user.save()

                messages.info(request, 'you have registered successfully!!!')
                return redirect(register)
        else:
            messages.info(request, ' password do not match')
            return redirect(register)

    else:
        return render(request, 'register.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('home01')
        else:
            messages.info(request, 'Invalid Username or Password')
            return redirect('login_user')
    else:
        return render(request, 'login.html')


def logout_user(request):
    auth.logout(request)
    return redirect('home01')


class AddPostView(CreateView):
    model = Post
    template_name = 'add_post.html'
    fields = ['title', 'author', 'content2']
    # fields = ('title', 'body')
    success_url = reverse_lazy('feed')


class ArticleDetail(DetailView):
    model = Post
    template_name = 'articles_contain.html'


class UpdatePostView(UpdateView):
    model = Post
    template_name = 'update_post.html'
    fields = ['title', 'content2']
    success_url = reverse_lazy('feed')


class DeletePostView(DeleteView):
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('feed')


class AddCommentView(CreateView):
    model = Comment
    template_name = 'add_comment.html'
    # fields = ['name', 'body']
    success_url = reverse_lazy('feed')

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)

    success_url = reverse_lazy('feed')
    fields = ('name', 'body')


def mypost(request):
    posts = Post.objects.filter(author=request.user.username)
    return render(request, 'mypost.html', {'myposts': posts})


def user_change_pass(request):
    if request.method == 'POST':
        fm = PasswordChangeForm(user=request.user, data=request.POST)
        if fm.is_valid():
            fm.save()
            update_session_auth_hash(request, fm.user)
            return HttpResponseRedirect('/profile/')
    else:
        fm = PasswordChangeForm(user=request.user)
    return render(request, 'changepass.html', {'form': fm})
