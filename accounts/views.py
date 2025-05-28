from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import JsonResponse
from .forms import EmailLoginForm

def login_view(request):
    if request.method == 'POST':
        form = EmailLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'success': True, 'message': "Connexion réussie !", 'redirect_url': '/'} )
                messages.success(request, "Connexion réussie !")
                return redirect('blog-home')
            else:
                error_msg = "Email ou mot de passe incorrect."
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'message': error_msg})
                messages.error(request, error_msg)
        else:
            error_msg = "Veuillez corriger les erreurs dans le formulaire."
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': error_msg, 'errors': form.errors})
            messages.error(request, error_msg)
    else:
        form = EmailLoginForm()
    return render(request, 'accounts/login.html', {'form': form})

# Optionnel : une vue pour vérifier l'état de connexion (utile côté JS)
from django.contrib.auth.decorators import login_required

@login_required
def check_login_status(request):
    return JsonResponse({'is_authenticated': True, 'user': request.user.email})
