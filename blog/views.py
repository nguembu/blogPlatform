from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .models import Post, Comment
from .forms import CommentForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import UserUpdateForm, ProfileUpdateForm

from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from .models import Post, Tag, Comment 
from django.contrib.auth.models import User
from .forms import CommentForm  # Assurez-vous d'importer votre formulaire de commentaire
from .models import Follow, User
from .models import Profile
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login




class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Récupérer les commentaires approuvés
        comments = self.object.comments.filter(approved_comment=True)
        
        # Formater chaque commentaire pour les mentions
        formatted_comments = [comment.format_text_with_mentions() for comment in comments]
        
        context['comments'] = formatted_comments
        context['comment_form'] = CommentForm()
        context['all_users'] = User.objects.exclude(id=self.request.user.id)  # Exclure l'utilisateur actuel
        
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post-detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('post-detail', pk=post.pk)

def about(request):
    return render(request, 'blog/about.html', {'title': 'À propos'})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Inscription réussie !")
            return redirect('blog-home')
    else:
        form = RegisterForm()
    return render(request, 'blog/register.html', {'form': form})
 

@login_required
def profile(request):
    try:
        # Essayer d'accéder au profil de l'utilisateur
        profile = request.user.profile
    except Profile.DoesNotExist:
        # Si le profil n'existe pas, rediriger vers une vue de création de profil
        messages.warning(request, "Votre profil n'existe pas. Veuillez le créer.")
        return redirect('register')  # Remplacez par la vue appropriée pour créer un profil

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Votre profil a été mis à jour !')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'blog/profile.html', context)



@login_required
def tag_user(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        user_to_tag_id = request.POST.get('user')  # Récupérer l'ID de l'utilisateur à taguer
        user_to_tag = get_object_or_404(User, id=user_to_tag_id)

        if request.user != user_to_tag:  # Vérifier que l'utilisateur ne se tague pas lui-même
            Tag.objects.create(user=user_to_tag, post=post)
            return redirect('post_detail', post_id=post.id)  # Redirige vers la page du post

    return redirect('post_detail', post_id=post_id)


def follow_user(request, user_id):
    if request.user.is_authenticated:
        followed_user = get_object_or_404(User, id=user_id)
        Follow.objects.get_or_create(follower=request.user, followed=followed_user)
    return redirect('home')

def unfollow_user(request, user_id):
    if request.user.is_authenticated:
        followed_user = get_object_or_404(User, id=user_id)
        Follow.objects.filter(follower=request.user, followed=followed_user).delete()
    return redirect('home')

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post-detail', pk=post.pk)
    else:
        comment_form = CommentForm()
    
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    })
    
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.author or request.user.is_superuser:
        comment.delete()
    return redirect('post-detail', pk=comment.post.id)

from .forms import CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)  # Inclure request.FILES
        if form.is_valid():
            form.save()
            return redirect('login')  # Rediriger vers la page de connexion
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Connexion réussie !')
            return redirect('home')  # Redirigez vers la page d'accueil ou une autre page
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')

    return render(request, 'blog/login.html')  # Remplacez par le chemin correct de votre template

@login_required
def change_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()  # Sauvegarder les modifications de l'utilisateur
            p_form.save()  # Sauvegarder les modifications du profil
            messages.success(request, 'Votre profil a été mis à jour avec succès !')
            return redirect('profile')  # Rediriger vers la page de profil

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'blog/change_profile.html', context)


class PrivacyPolicyView(TemplateView):
    template_name = 'blog/privacy_policy.html'  # Assurez-vous d'avoir ce template
    
    


def home(request):
    recent_posts = Post.objects.order_by('-created_at')[:5]  # Récupérer les 5 articles les plus récents
    context = {
        'recent_posts': recent_posts,
        # Ajoutez d'autres contextes si nécessaire
    }
    return render(request, 'blog/home.html', context)