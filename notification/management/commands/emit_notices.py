
import logging

from django.core.management.base import NoArgsCommand
from django.utils import translation
from django.conf import settings

from notification.engine import send_all

class Command(NoArgsCommand):
    help = "Emit queued notices."
    
    def handle_noargs(self, **options):
        translation.activate(settings.LANGUAGE_CODE)

        logging.basicConfig(level=logging.DEBUG, format="%(message)s")
        logging.info("-" * 72)
        send_all()

        translation.deactivate()
    