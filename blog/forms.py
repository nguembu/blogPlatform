from django import forms
from .models import Comment
from django.contrib.auth.models import User
from .models import Profile, CustomUser
from django.contrib.auth.forms import UserCreationForm

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['text'].label = "Add a comment"
        self.fields['text'].widget.attrs.update({'placeholder': 'Write your comment here...'})
        self.fields['text'].widget.attrs['class'] = 'form-control'
        self.fields['text'].widget.attrs['rows'] = 3

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'bio']



class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        

class TagForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all(), label="Taguer un utilisateur")

class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'profile_picture']  # Ajoutez le champ profile_picture