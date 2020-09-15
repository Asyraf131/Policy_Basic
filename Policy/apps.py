from django.apps import AppConfig


class PolicyConfig(AppConfig):
    name = 'Policy'

    def ready(self):
        import Policy.signals
