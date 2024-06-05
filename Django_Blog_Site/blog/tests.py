from django.test import TestCase
from django.contrib.auth.models import User
from django.shortcuts import reverse

from .models import Post


class BlogPostTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='testuser')
        cls.post1 = Post.objects.create(
            title='test1',
            text='this is description of test1',
            status=Post.STATUS_CHOICES[0][0],
            author=cls.user,
        )
        cls.post2 = Post.objects.create(
            title='test2',
            text='this is description of test2',
            status=Post.STATUS_CHOICES[0][1],
            author=cls.user,
        )

    def test_post_model_str_25(self):
        post = self.post1
        self.assertEqual(str(post), post.title)

    def test_Correctness_of_post_detail_29(self):
        self.assertEqual(self.post1.title, 'test1')
        self.assertEqual(self.post1.text, 'this is description of test1')

    def test_post_list_view_url_33(self):
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)

    def test_post_list_view_url_by_name_37(self):
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)

    def test_post_detail_view_url_41(self):
        response = self.client.get(f'/blog/{self.post1.id}/')
        self.assertEqual(response.status_code, 200)

    def test_post_detail_view_url_by_name_45(self):
        response = self.client.get(reverse('post_detail', args=[self.post1.id]))
        self.assertEqual(response.status_code, 200)

    def test_title_exists_49(self):
        response = self.client.get(reverse('post_list'))
        self.assertContains(response, self.post1.title)

    def test_title_exists_on_post_detail_53(self):
        response = self.client.get(reverse('post_detail', args=[self.post1.id]))
        self.assertContains(response, self.post1.title)
        self.assertContains(response, self.post1.text)

    def test_status_404_if_id_not_exists_58(self):
        # for example /blog/10000 ---> ObjectDoesNotExist ---> page not found 404
        response = self.client.get(reverse('post_detail', args=[5198295]))
        self.assertEqual(response.status_code, 404)

    def test_draft_post_not_show_in_posts_list_63(self):
        response = self.client.get(reverse('post_list'))
        self.assertContains(response, self.post1.title)
        self.assertNotContains(response, self.post2.title)

    def test_post_create_view_68(self):
        response = self.client.post(reverse('post_create'), {
            'title': 'test3',
            'text': 'this is description of test3',
            'status': 'pub',
            'author': self.user.id
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, 'test3')
        self.assertEqual(Post.objects.last().text, 'this is description of test3')

    def test_post_update_view_79(self):
        response = self.client.post(reverse('post_update', args=[self.post2.id]), {
            'title': 'test1 Updated',
            'text': 'this is update for test1',
            'status': 'pub',
            'author': self.user.id
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, 'test1 Updated')
        self.assertEqual(Post.objects.last().text, 'this is update for test1')

    def test_post_delete_view_90(self):
        response = self.client.post(reverse('post_delete', args=[self.post1.id]))
        self.assertEqual(response.status_code, 302)
