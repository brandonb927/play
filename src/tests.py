from django.conf import settings
from django.http import HttpResponseRedirect
from django.test import Client, TestCase
from django.urls import reverse


from django_extensions.management.commands.show_urls import Command as ShowUrlsCommand


class URLPatternTestCase(TestCase):
    def test_url_no_slashes(self):
        urlconf = __import__(settings.ROOT_URLCONF, {}, {}, [""])
        view_patterns = ShowUrlsCommand().extract_views_from_urlpatterns(
            urlconf.urlpatterns
        )
        for (func, regex, url_name) in view_patterns:
            self.assertTrue(
                regex == "" or regex.endswith("/") or regex.endswith("/$"), regex
            )


class AdminLoginTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_page(self):
        response = self.client.get("/admin/login/")

        self.assertEqual(response.status_code, 302)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, reverse("login"))

    def test_login_page_next_param(self):
        response = self.client.get("/admin/login/?next=%2Ftest%2Furl")

        self.assertEqual(response.status_code, 302)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, reverse("login") + "?next=%2Ftest%2Furl")


class AdminLogoutnTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_page(self):
        response = self.client.get("/admin/logout/")

        self.assertEqual(response.status_code, 302)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, reverse("admin:index"))
