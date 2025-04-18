from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image
from django.utils import timezone
from django.urls import reverse
import re
from django.contrib.auth.models import AbstractUser ,Group, Permission

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images', blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='blog_posts', blank=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
    
    def total_likes(self):
        return self.likes.count()



class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=True)

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.post.pk})

    def format_text_with_mentions(self):
        pattern = r'@([A-Za-z0-9_]+)'  # Regex pour détecter @NOM
        def replace_func(match):
            username = match.group(1)
            try:
                user = User.objects.get(username=username)
                return f'<a href="{reverse("user-posts", args=[username])}">@{username}</a>'
            except User.DoesNotExist:
                return match.group(0)  # Retourne le texte original s'il n'y a pas de correspondance

        return re.sub(pattern, replace_func, self.text)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
            


class Tag(models.Model):
    user = models.ForeignKey(User, related_name='tags', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', related_name='tags', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} tagged in {self.post.title}"
    
    
class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    followed = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('follower', 'followed')

class CustomUser(AbstractUser):
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True, default='default.jpg')

    # Ajoutez les related_name pour éviter les conflits
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # Changer le nom ici
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',  # Changer le nom ici
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )