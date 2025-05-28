from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Comment, Profile, Person

# ==============================
# Formulaire d'enregistrement personnalisé
# ==============================

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Person
        fields = ['username', 'email', 'sex', 'profile_picture', 'password1', 'password2']

# ==============================
# Formulaire de connexion
# ==============================

class LoginForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

# ==============================
# Mise à jour du profil utilisateur
# ==============================

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = Person
        fields = ['username', 'email', 'sex', 'profile_picture']

# ==============================
# Mise à jour du profil bio/image
# ==============================

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'bio']

# ==============================
# Formulaire pour les commentaires
# ==============================

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write your comment here...'
            }),
        }
        labels = {
            'text': "Add a comment",
        }

# ==============================
# Formulaire pour taguer un utilisateur
# ==============================

class TagForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=Person.objects.all(),
        label="Taguer un utilisateur"
    )
