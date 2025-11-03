from django.apps import AppConfig


class MarketConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'market'
    
    def ready(self):
        """Development helper: clear sessions on server start.

        This ensures users are not left logged in between dev server restarts.
        Only run when DEBUG is True and the dev server is starting to avoid
        surprising behavior in production.
        """
        try:
            from django.conf import settings
            import sys
            # only clear sessions when running the dev server
            if settings.DEBUG and any('runserver' in a for a in sys.argv):
                from django.contrib.sessions.models import Session
                Session.objects.all().delete()
        except Exception:
            # don't let startup fail for missing DB or migrations during manage.py commands
            pass
