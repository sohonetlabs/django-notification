import datetime
from time import time

from django.test import TestCase

from django.contrib.auth.models import User
from django.core.management import call_command
from django.conf import settings

from notification.models import Notice, NoticeType


class TestRemoveOldNoticesCommand(TestCase):

    def call_remove_old_notices_command(self, dryrun=False):
        call_command('remove_old_notices', dryrun=dryrun)

    def setUp(self):
        self.user1 = User.objects.create_user('user1', 'user1@example.com', '123456')

    def create_notice(self):
        notice = Notice(
            recipient=self.user1,
            sender=self.user1,
            message='test message for notice',
            notice_type = NoticeType.objects.latest('pk'),
            on_site=True)
        notice.save()
        return notice

    def test_notifications_not_old_enough(self):
        settings.NOTICES_MAX_AGE = 999 # big number to make notifications
                                            # look young
        notice = self.create_notice()
        self.call_remove_old_notices_command()
        self.assertEqual(1, Notice.objects.count())
        
    def test_notification_old_enough(self):
        settings.NOTICES_MAX_AGE = 0 # every notice will be old enough
        notice = self.create_notice()
        self.call_remove_old_notices_command()
        self.assertEqual(0, Notice.objects.count())
    
    def test_dry_run(self):
        settings.NOTICES_MAX_AGE = 0 # every notice will be old enough
        notice = self.create_notice()
        self.call_remove_old_notices_command(dryrun=True)
        self.assertEqual(1, Notice.objects.count())

