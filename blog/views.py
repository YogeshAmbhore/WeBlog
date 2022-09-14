from django.views import generic
from .models import Post
from django.urls import reverse
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserLoginForm, BloggerCreationForm, BlogCreationForm, CommentForm
from .models import AuthorProfile

class AuthorLoginView(LoginView):
    authentication_form = UserLoginForm
    extra_context = {'page': 'login'}
    template_name = 'login_signup.html'
    # success_url = reverse_lazy('home')

    def get_success_url(self):
        return reverse('home')

def logoutauthor(request):
    logout(request)
    return redirect('home')

class AuthorSignUpView(CreateView):
    form_class = BloggerCreationForm
    model = AuthorProfile
    template_name = 'login_signup.html'
    extra_context = {'page': 'signup'}
    success_url = reverse_lazy('home')

class ProfileView(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'profile.html'

class BlogCreationView(CreateView):
    form_class = BlogCreationForm
    model = Post
    template_name = 'add_blog.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author = self.request.user.authorprofile
        return super().form_valid(form)


class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'

class PostDetail(generic.DetailView):
    model = Post
    # form_class = CommentForm
    template_name = 'post_detail.html'
    

