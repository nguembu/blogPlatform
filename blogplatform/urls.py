from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from blog import views as blog_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Inclure toutes les routes de l'application blog, y compris 'profile/' et 'register/'
    path('', include('blog.urls')),  

    # Si tu veux garder une route spécifique pour register en dehors de blog.urls, tu peux, sinon elle est déjà dans blog.urls
    # path('register/', blog_views.register, name='register'),  # à supprimer si déjà dans blog.urls

    # Authentification sociale avec django-allauth
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
