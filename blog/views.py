from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_backends
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
)
from django.urls import reverse_lazy, reverse

from .models import Post, Tag, Comment, Person, Follow, Profile
from .forms import CommentForm, UserUpdateForm, ProfileUpdateForm, RegisterForm, LoginForm

# --- List & Detail Views ---

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']

class HomeView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'recent_posts'
    ordering = ['-date_posted']
    paginate_by = 5

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        comments = post.comments.filter(approved_comment=True)
        context['comments'] = [comment.format_text_with_mentions() for comment in comments]
        context['comment_form'] = CommentForm()
        if self.request.user.is_authenticated:
            context['all_users'] = Person.objects.exclude(id=self.request.user.id)
        else:
            context['all_users'] = Person.objects.none()
        return context

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(Person, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

# --- CRUD Views for Post ---

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'image']
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'image']
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog-home')
    template_name = 'blog/post_confirm_delete.html'

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user

# --- Comment, Like, Tag, Follow, Profile ---

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
        messages.success(request, "Commentaire ajouté avec succès.")
        return redirect('post-detail', pk=post.pk)
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # Seuls les utilisateurs autres que l'auteur du post peuvent liker
    if request.user != post.author:
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            messages.info(request, "Vous avez retiré votre like.")
        else:
            post.likes.add(request.user)
            messages.success(request, "Vous avez aimé ce post.")
    else:
        messages.warning(request, "Vous ne pouvez pas liker votre propre post.")
    return redirect('post-detail', pk=pk)

@login_required
def tag_user(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        user_to_tag_id = request.POST.get('user')
        if user_to_tag_id:
            user_to_tag = get_object_or_404(Person, id=user_to_tag_id)
            if request.user != user_to_tag:
                Tag.objects.get_or_create(user=user_to_tag, post=post)
    return redirect('post-detail', pk=post_id)

@login_required
def follow_user(request, user_id):
    followed_user = get_object_or_404(Person, id=user_id)
    if request.user != followed_user:
        Follow.objects.get_or_create(follower=request.user, followed=followed_user)
        messages.success(request, f"Vous suivez désormais {followed_user.username}.")
    else:
        messages.warning(request, "Vous ne pouvez pas vous suivre vous-même.")
    return redirect('blog-home')

@login_required
def unfollow_user(request, user_id):
    followed_user = get_object_or_404(Person, id=user_id)
    Follow.objects.filter(follower=request.user, followed=followed_user).delete()
    messages.info(request, f"Vous ne suivez plus {followed_user.username}.")
    return redirect('blog-home')

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.author or request.user.is_superuser:
        comment.delete()
        messages.success(request, "Commentaire supprimé.")
    else:
        messages.error(request, "Vous n'êtes pas autorisé à supprimer ce commentaire.")
    return redirect('post-detail', pk=comment.post.pk)

# --- Auth & Profile ---

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            backend = get_backends()[0]
            login(request, user, backend=backend.__module__ + "." + backend.__class__.__name__)
            messages.success(request, "Inscription réussie !")
            return redirect('blog-home')
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    else:
        form = RegisterForm()
    return render(request, 'blog/register.html', {'form': form})

def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                messages.success(request, 'Connexion réussie !')
                return redirect('blog-home')
            else:
                messages.error(request, "Email ou mot de passe incorrect.")
    return render(request, 'blog/login.html', {'form': form})

@login_required
def profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        messages.warning(request, "Votre profil n'existe pas. Veuillez le créer.")
        return redirect('register')

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Votre profil a été mis à jour !')
            return redirect('profile')
        else:
            messages.error(request, "Erreur lors de la mise à jour du profil.")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'blog/profile.html', {'u_form': u_form, 'p_form': p_form})

@login_required
def change_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Votre profil a été mis à jour avec succès !')
            return redirect('profile')
        else:
            messages.error(request, "Erreur lors de la mise à jour du profil.")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)

    return render(request, 'blog/change_profile.html', {'u_form': u_form, 'p_form': p_form})

# --- Static Pages ---

def about(request):
    return render(request, 'blog/about.html', {'title': 'À propos'})
def privacy_policy(request):
        return render(request, 'blog/privacy_policy.html')
def terms_of_service(request):
        return render(request, 'blog/terms_of_service.html')

def contact(request):
        return render(request, 'blog/contact.html', {'title': 'Contact'})

def help_view(request):
        return render(request, 'blog/help.html', {'title': 'Aide'})

def faq(request):
        return render(request, 'blog/faq.html', {'title': 'FAQ'})


@login_required
def parametre(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        messages.warning(request, "Votre profil n'existe pas. Veuillez le créer.")
        return redirect('register')

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Paramètres mis à jour avec succès !')
            return redirect('parametre')
        else:
            messages.error(request, "Erreur lors de la mise à jour des paramètres.")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)

    return render(request, 'blog/parametre.html', {'u_form': u_form, 'p_form': p_form})

@login_required
def delete_account(request):
    if request.method == 'POST':
         user = request.user
         user.delete()
         messages.success(request, "Votre compte a été supprimé avec succès.")
         return redirect('blog-home')
    return render(request, 'blog/delete_account_confirm.html')

def contact_thanks(request, email, message, subject=None, status=None):
    context = {
        'email': email,
        'message': message,
        'subject': subject,
        'status': status,
    }
    return render(request, 'blog/contact_thanks.html', context)

def contact_success(request):
    return render(request, 'blog/contact_success.html', {'title': 'Contact - Succès'})

def contact_failure(request):
    return render(request, 'blog/contact_failure.html', {'title': 'Contact - Échec'})

@login_required
def add_comment(request, post_id):
        post = get_object_or_404(Post, id=post_id)
        if request.user == post.author:
            messages.warning(request, "Vous ne pouvez pas commenter votre propre post.")
            return redirect('post-detail', pk=post_id)
        if request.method == "POST":
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                messages.success(request, "Commentaire ajouté avec succès.")
                return redirect('post-detail', pk=post_id)
        else:
            form = CommentForm()
        return render(request, 'blog/add_comment_to_post.html', {'form': form, 'post': post})