from django.apps import AppConfig
from .models import Resource


class SocialConfig(AppConfig):
    name = "social"

    def ready(self):
        from django_oso.oso import Oso

        Oso.register_constant(None, "None")
        Oso.register_class(Resource, name="social::Resource")
        return super().ready()
