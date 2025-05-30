from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import *
from .views import privacy_policy, help_view

urlpatterns = [
    # Home & About
    path('', PostListView.as_view(), name='blog-home'),
    path('about/', views.about, name='blog-about'),
    path('privacy-policy/', privacy_policy, name='privacy-policy'),

    # Post CRUD
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),

    # Post Interactions
    path('post/<int:pk>/comment/', add_comment_to_post, name='post-add-comment'),
    path('post/<int:pk>/like/', views.like_post, name='post-like'),
    path('post/<int:post_id>/tag/', tag_user, name='post-tag-user'),

    # User Posts
    path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'),

    # Follow System
    path('follow/<int:user_id>/', follow_user, name='follow'),
    path('unfollow/<int:user_id>/', unfollow_user, name='unfollow'),

    # Profile
    path('help/', help_view, name='help'),
    path('profile/', profile, name='profile'),
    path('change-profile/', change_profile, name='change-profile'),
    path('parametre/', parametre, name='parametre'),
    path('delete-account/', delete_account, name='delete-accounts'),
    path('contact/', views.contact, name='blog-Contact'),
    path('contact/success/', contact_success, name='contact-success'),
    path('contact/failure/', contact_failure, name='contact-failure'),
    path('contact/thanks/', contact_thanks, name='contact-thanks'),
    path('contact/thanks/<str:email>/', contact_thanks, name='contact-thanks-email'),
    path('contact/thanks/<str:email>/<str:message>/', contact_thanks, name='contact-thanks-email-message'),
    path('contact/thanks/<str:email>/<str:message>/<str:subject>/', contact_thanks, name='contact-thanks-email-message-subject'),
    path('contact/thanks/<str:email>/<str:message>/<str:subject>/<str:status>/', contact_thanks, name='contact-thanks-email-message-subject-status'),
    path('add-comment/', views.add_comment, name='add-comment'),

    # Auth
    path('login/', views.login_view, name='login'),  # vue personnalisée
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
]
