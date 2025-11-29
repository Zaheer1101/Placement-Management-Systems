from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Alias for runserver (convenience command): python manage.py renserver'

    def add_arguments(self, parser):
        # Accept arbitrary arguments and forward them to runserver
        parser.add_argument('args', nargs='*')

    def handle(self, *args, **options):
        args = options.get('args') or []
        # If no args provided, default to runserver 0.0.0.0:8000
        if not args:
            args = ['runserver', '0.0.0.0:8000']
        # If the provided args already start with runserver, just call
        if args[0] == 'runserver':
            call_command(*args)
        else:
            # Prepend runserver so calling `python manage.py renserver 8001` works
            call_command('runserver', *args)
