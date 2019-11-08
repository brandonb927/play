from django.conf import settings
from django.http import HttpResponseRedirect
from django.test import Client, TestCase
from django.urls import reverse


from django_extensions.management.commands.show_urls import Command as ShowUrlsCommand


class URLPatternTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url_patterns = ShowUrlsCommand().extract_views_from_urlpatterns(
            __import__(settings.ROOT_URLCONF, {}, {}, [""]).urlpatterns
        )

    def test_url_no_slashes(self):
        for (func, regex, url_name) in self.url_patterns:
            self.assertTrue(
                regex == "" or regex.endswith("/") or regex.endswith("/$"), regex
            )

    def test_static_pages_200(self):
        for (func, regex, url_name) in self.url_patterns:
            # bvanvugt: Is this the best/only way to detect dynamic urls?
            if "<" in regex or ">" in regex:
                continue
            response = self.client.get(regex)
            self.assertTrue(response.status_code, 200)


class AdminLoginTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_page(self):
        response = self.client.get("/admin/django/login/")

        self.assertEqual(response.status_code, 302)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, reverse("login"))

    def test_login_page_next_param(self):
        response = self.client.get("/admin/django/login/?next=%2Ftest%2Furl")

        self.assertEqual(response.status_code, 302)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, reverse("login") + "?next=%2Ftest%2Furl")


class AdminLogoutnTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_page(self):
        response = self.client.get("/admin/django/logout/")

        self.assertEqual(response.status_code, 302)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, reverse("admin:index"))
