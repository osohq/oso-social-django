from django.apps import AppConfig

from datetime import datetime, timedelta

from django_oso.oso import Oso


class Date:
    @classmethod
    def ten_min_ago(cls):
        return datetime.now() - timedelta(minutes=10)


class SocialConfig(AppConfig):
    name = "social"

    def ready(self):
        print("ready")
        Oso.register_class(Date)
