from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import *

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/comment/', add_comment_to_post, name='post-add-comment'),
    path('post/<int:pk>/like/', views.like_post, name='post-like'),
    path('post/<int:post_id>/tag/', tag_user, name='post-tag-user'),

    path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'),

    path('follow/<int:user_id>/', follow_user, name='follow'),
    path('unfollow/<int:user_id>/', unfollow_user, name='unfollow'),

    path('profile/', profile, name='profile'),
    path('change-profile/', change_profile, name='change-profile'),
    path('privacy-policy/', PrivacyPolicyView.as_view(), name='privacy-policy'),

    path('about/', views.about, name='blog-about'),

    # Auth
    path('login/', views.login_view, name='login'),  # vue personnalisée
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
]
