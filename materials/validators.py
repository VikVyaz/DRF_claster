from urllib.parse import urlparse

from rest_framework.serializers import ValidationError


class UrlValidator:

    def __init__(self, url):
        self.url = url

    def __call__(self, value):
        url = value.get(self.url)

        parsed = urlparse(url)
        hostname = parsed.hostname or ''

        if 'youtube.com' not in hostname:
            raise ValidationError('Ссылка должна вести на YouTube.com')
