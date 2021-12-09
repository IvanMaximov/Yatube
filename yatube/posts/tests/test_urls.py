from http import HTTPStatus
from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from ..models import Group, Post

User = get_user_model()


class PostURLTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='test_user')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовая группа',
        )

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='HasNoName')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_exists_at_desired_location(self):
        """Страница доступна любому пользователю"""
        status = HTTPStatus.OK
        pages_url = {
            '/': status,
            '/group/test-slug/': status,
            '/profile/test_user/': status,
            '/posts/1/': status
        }
        for adress, http_status in pages_url.items():
            with self.subTest(adress=adress):
                response = self.guest_client.get(adress)
                self.assertEqual(response.status_code, http_status)

    def test_post_edit_url_exists_at_desired_location(self):
        """Страница posts/<post_id>/edit/ доступна автору поста."""
        response = self.authorized_client.get('/posts/1/edit/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_create_url_exists_at_desired_location(self):
        """Страница create/ доступна авторизованному пользователю."""
        response = self.authorized_client.get('/create/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            '/': 'posts/index.html',
            '/group/test-slug/': 'posts/group_list.html',
            '/profile/test_user/': 'posts/profile.html',
            '/posts/1/': 'posts/post_detail.html',
            '/create/': 'posts/create.html',
            '/posts/1/edit/': 'posts/create.html',
            "/follow/": 'posts/follow.html'
        }
        for adress, template in templates_url_names.items():
            with self.subTest(adress=adress):
                response = self.authorized_client.get(adress)
                self.assertTemplateUsed(response, template)

    def test_post_comment_url_unexists_at_desired_location(self):
        """Страница posts/<post_id>/comment/ недоступна
        неавторизованному пользователю."""
        response = self.guest_client.get('/posts/1/comment/')
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_follow_url_exists_at_desired_location(self):
        """Страница follow/ доступна авторизованному пользователю."""
        response = self.authorized_client.get('/follow/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
