from django.conf import settings
from django.test import TestCase

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
