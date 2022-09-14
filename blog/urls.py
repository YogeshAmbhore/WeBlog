from . import views
from django.urls import path


urlpatterns = [
    path('login/', views.AuthorLoginView.as_view(), name='author-login'),
    path('signup/', views.AuthorSignUpView.as_view(), name='author-signup'),
    path('logout/', views.logoutauthor, name= 'author-logout'),
    path('create_blog/', views.BlogCreationView.as_view(), name='create-blog'),
    path('profile/', views.ProfileView.as_view(), name='author-profile'),
    path('', views.PostList.as_view(), name='home'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
]