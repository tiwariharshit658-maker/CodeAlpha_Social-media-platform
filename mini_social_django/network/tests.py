from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from .models import Follow, Post

User = get_user_model()


class FollowModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="securepass123")

    def test_self_follow_is_rejected(self):
        with self.assertRaises(ValidationError):
            Follow.objects.create(follower=self.user, followed=self.user)


class UserPostTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="bob", password="securepass123")

    def test_user_can_create_post(self):
        post = Post.objects.create(author=self.user, content="Hello from bob!")
        self.assertEqual(self.user.posts.count(), 1)
        self.assertEqual(post.author, self.user)

    def test_user_profile_displays_posts(self):
        Post.objects.create(author=self.user, content="This is my first post")

        response = self.client.get(reverse("profile", args=[self.user.username]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This is my first post")
        self.assertContains(response, "Posts by bob")
