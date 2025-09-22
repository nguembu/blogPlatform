from django.test import TestCase
from django.contrib.auth import get_user_model
from blog.models import Post, Comment

User = get_user_model()

class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="bob",
            email="bob@test.com",
            password="12345"
        )
        self.post = Post.objects.create(
            title="Titre Test",
            content="Contenu Test",
            author=self.user
        )

    def test_post_str(self):
        self.assertEqual(str(self.post), "Titre Test")


class CommentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="alice",
            email="alice@test.com",
            password="12345"
        )
        self.post = Post.objects.create(
            title="Post",
            content="Content",
            author=self.user
        )
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            text="Cool"   # ✅ champ corrigé
        )

    def test_comment_str(self):
        self.assertEqual(str(self.comment), "Cool")
