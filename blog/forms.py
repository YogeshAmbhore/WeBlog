from django import forms
from django.forms import ModelForm, fields
from .models import Post, AuthorProfile, Comment
from django.db import transaction
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password',
        }
    ))

class BloggerCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    def clean_username(self):
        if User.objects.filter(username__iexact=self.cleaned_data['username']).exists():
            raise forms.ValidationError("the given username is already registered")
        return self.cleaned_data['username']

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError("the given email is already registered")
        return self.cleaned_data['email']

    class Meta:
        model = User
        fields = ['first_name', 'username', 'email', 'password1', 'password2']
        labels = {
            'first_name' : 'Name',
        }

    def __init__(self, *args, **kwargs):
        super(BloggerCreationForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'form-control'})
    
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.username = user.username.lower()
        user.save()
        author = AuthorProfile.objects.create(user=user)
        return user

class BlogCreationForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'status']

    def __init__(self, *args, **kwargs):
        super(BlogCreationForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'form-control'})

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'content')