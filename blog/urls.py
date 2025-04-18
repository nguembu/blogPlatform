from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import UserPostListView, login_view, home
from .views import change_profile  , PrivacyPolicyView
from .views import tag_user, profile
from .views import follow_user, unfollow_user, add_comment_to_post
from .views import (
    PostListView, PostDetailView, PostCreateView,
    PostUpdateView, PostDeleteView
)

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/comment/', add_comment_to_post, name='add-comment'),
    path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/like/', views.like_post, name='like-post'),
    path('about/', views.about, name='blog-about'),
    path('login/', auth_views.LoginView.as_view(
        template_name='blog/login.html',
        redirect_authenticated_user=True
    ), name='login'),
     path('login/', login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('post/<int:post_id>/tag/<int:user_id>/', tag_user, name='tag_user'),
    path('follow/<int:user_id>/', follow_user, name='follow'),
    path('unfollow/<int:user_id>/', unfollow_user, name='unfollow'),
    path('change-profile/', change_profile, name='change-profile'),
    path('privacy-policy/', PrivacyPolicyView.as_view(), name='privacy-policy'),
    path('profile/', profile, name='profile'),
     path('', home, name='home'),  # Définir la vue home
]