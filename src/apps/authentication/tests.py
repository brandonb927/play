from django.http import HttpResponseRedirect
from django.test import Client, TestCase
from django.urls import reverse


class LoginViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_page(self):
        response = self.client.get("/login/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name, ["pages/login.html"])


class LogoutViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_logout_page(self):
        response = self.client.get("/logout/")
        self.assertEqual(response.status_code, 302)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, reverse("home"))

    def test_logout_page_next_param(self):
        response = self.client.get("/logout/?next=/test/url")
        self.assertEqual(response.status_code, 302)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, "/test/url")
