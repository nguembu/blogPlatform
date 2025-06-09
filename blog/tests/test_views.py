from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from blog.models import Post, Comment, Profile

User = get_user_model()

class BlogViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', email='test@example.com', password='testpass123'
        )
        # Création du profil si non créé par un signal
        self.profile, _ = Profile.objects.get_or_create(user=self.user)

        self.post = Post.objects.create(
            author=self.user, title='Test Post', content='Test content'
        )

    def test_post_list_view(self):
        response = self.client.get(reverse('blog-home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/home.html')
        self.assertContains(response, 'Test Post')

    def test_post_detail_view(self):
        response = self.client.get(reverse('post-detail', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')

    def test_post_create_view_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('post-create'))
        self.assertRedirects(response, "/accounts/login/?next=/post/new/")

    # def test_post_create_view_logged_in(self):
    #     self.client.login(username='testuser', password='testpass123')
    #     response = self.client.post(reverse('post-create'), {
    #         'title': 'New Post',
    #         'content': 'New content',
    #     }, follow=True)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue(Post.objects.filter(title='New Post', author=self.user).exists())

    # def test_add_comment_authenticated(self):
    #     self.client.login(username='testuser', password='testpass123')
    #     response = self.client.post(reverse('post-add-comment', kwargs={'pk': self.post.pk}), {
    #         'text': 'A new comment'
    #     }, follow=True)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue(Comment.objects.filter(post=self.post, text='A new comment', author=self.user).exists())

    def test_add_comment_not_authenticated(self):
        response = self.client.post(reverse('post-add-comment', kwargs={'pk': self.post.pk}), {
            'text': 'Should not work'
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_profile_view_requires_login(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_profile_view_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('profile'), follow=True)
        self.assertEqual(response.status_code, 200)

    # def test_full_post_creation_and_comment_flow(self):
    #     self.client.login(username='testuser', password='testpass123')
    #     response = self.client.post(reverse('post-create'), {
    #         'title': 'Integration Post',
    #         'content': 'Integration content',
    #     }, follow=True)
    #     self.assertEqual(response.status_code, 200)
    #     post = Post.objects.filter(title='Integration Post', author=self.user).order_by('-id').first()
    #     self.assertIsNotNone(post)

    #     response = self.client.post(reverse('post-add-comment', kwargs={'pk': post.pk}), {
    #         'text': 'Integration comment'
    #     }, follow=True)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue(Comment.objects.filter(post=post, text='Integration comment', author=self.user).exists())

    def test_navigation_access(self):
        urls = [
            reverse('blog-home'),
            reverse('post-detail', kwargs={'pk': self.post.pk}),
            reverse('profile'),
            reverse('post-create'),
        ]
        # Non connecté
        self.assertEqual(self.client.get(urls[0]).status_code, 200)
        self.assertEqual(self.client.get(urls[1]).status_code, 200)
        self.assertRedirects(self.client.get(urls[2]), '/accounts/login/?next=/profile/')
        self.assertRedirects(self.client.get(urls[3]), '/accounts/login/?next=/post/new/')

        # Connecté
        self.client.login(username='testuser', password='testpass123')
        for url in urls:
            response = self.client.get(url)
            self.assertIn(response.status_code, [200, 302])
