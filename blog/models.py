from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.utils import timezone
from django.urls import reverse
from PIL import Image
import re

# ==============================
# Custom User Manager
# ==============================

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, username=None, sex=None, **extra_fields):
        if not email:
            raise ValueError("L'adresse email doit être renseignée")
        email = self.normalize_email(email)
        if not username:
            raise ValueError("Le username doit être renseigné")
        user = self.model(email=email, username=username, sex=sex, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, username=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email=email, password=password, username=username, **extra_fields)

# ==============================
# Custom User Model: Person
# ==============================

class Person(AbstractBaseUser, PermissionsMixin):
    SEX_TYPES = (
        ('M', 'Male'),
        ('F', 'Feminine'),
    )

    username = models.CharField(max_length=150, unique=False)  # unique ajouté pour éviter doublons
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=1, choices=SEX_TYPES, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True, default='default.jpg')

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    groups = models.ManyToManyField(
        Group,
        related_name='person_set',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to.'
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='person_permissions_set',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.'
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = "Person"
        verbose_name_plural = "Persons"
        constraints = [
            models.UniqueConstraint(fields=['username', 'email'], name='unique_person_username_email')
        ]

    def save(self, *args, **kwargs):
        # Si le mot de passe n'est pas encore hashé, on le hash
        if self.pk is None:  # création
            self.set_password(self.password)
        else:
            # Sur mise à jour on vérifie si password a changé
            old = Person.objects.filter(pk=self.pk).first()
            if old and old.password != self.password:
                self.set_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

# ==============================
# Blog Post Model
# ==============================

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(Person, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images', blank=True, null=True)
    likes = models.ManyToManyField(Person, related_name='blog_posts', blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def total_likes(self):
        return self.likes.count()

# ==============================
# Comment Model
# ==============================

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(Person, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=True)

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.post.pk})

    def format_text_with_mentions(self):
        pattern = r'@([A-Za-z0-9_]+)'

        def replace_func(match):
            username = match.group(1)
            try:
                user = Person.objects.get(username=username)
                return f'<a href="{reverse("user-posts", args=[username])}">@{username}</a>'
            except Person.DoesNotExist:
                return match.group(0)

        return re.sub(pattern, replace_func, self.text)

# ==============================
# Profile Model
# ==============================

class Profile(models.Model):
    user = models.OneToOneField(Person, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            img = Image.open(self.image.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)
        except Exception:
            pass

# ==============================
# Tag Model
# ==============================

class Tag(models.Model):
    user = models.ForeignKey(Person, related_name='tags', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='tags', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} tagged in {self.post.title}"

# ==============================
# Follow System
# ==============================

class Follow(models.Model):
    follower = models.ForeignKey(Person, related_name='following', on_delete=models.CASCADE)
    followed = models.ForeignKey(Person, related_name='followers', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('follower', 'followed')
