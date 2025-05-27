from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from blog.models import Post, Comment, Profile

User = get_user_model()

class BlogViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass123')
        
        # Si un signal crée le profil automatiquement, on n'en crée pas manuellement
        try:
            self.profile = self.user.profile
        except Profile.DoesNotExist:
            self.profile = Profile.objects.create(user=self.user)

        self.post = Post.objects.create(author=self.user, title='Test Post', content='Test content')

    def test_post_list_view(self):
        response = self.client.get(reverse('blog-home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/home.html')

    def test_post_detail_view(self):
        response = self.client.get(reverse('post-detail', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')

    def test_post_create_view_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('post-create'))
        self.assertRedirects(response, f"/accounts/login/?next=/post/new/")

    def test_post_create_view_logged_in(self):
        login_success = self.client.login(username='testuser', password='testpass123')
        self.assertTrue(login_success)

        response = self.client.post(reverse('post-create'), {
            'title': 'New Post',
            'content': 'New content',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(title='New Post').exists())


    def test_add_comment_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('post-add-comment', kwargs={'pk': self.post.pk}), {
            'text': 'A new comment'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Comment.objects.filter(post=self.post, text='A new comment').exists())

    def test_profile_view_requires_login(self):
        response = self.client.get(reverse('profile'))
        self.assertRedirects(response, '/accounts/login/?next=/profile/')

    def test_profile_view_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/profile.html')
