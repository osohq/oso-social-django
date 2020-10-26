from django.apps import AppConfig


class SocialConfig(AppConfig):
    name = "social"

    def ready(self):
        from django_oso.oso import Oso

        Oso.register_constant(None, "None")
        return super().ready()
