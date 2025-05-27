from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Comment, Profile, Person

# ==============================
# Formulaire pour les commentaires
# ==============================

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].label = "Add a comment"
        self.fields['text'].widget.attrs.update({
            'placeholder': 'Write your comment here...',
            'class': 'form-control',
            'rows': 3,
        })

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
# Formulaire d'enregistrement personnalisé
# ==============================

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Person
        fields = ['username', 'email', 'sex', 'profile_picture', 'password1', 'password2']

# ==============================
# Formulaire pour taguer un utilisateur
# ==============================

class TagForm(forms.Form):
    user = forms.ModelChoiceField(queryset=Person.objects.all(), label="Taguer un utilisateur")

class LoginForm(forms.Form):
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput(attrs={'class': 'form-control'}))