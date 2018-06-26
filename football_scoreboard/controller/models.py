from django.db import models

# Create your models here.
class UserRights(models.Model):
    class Meta:
        managed = False

        permissions = (
            ('change_clock', 'Can change clock status'),
            ('change_status', 'Can change game status'),
            ('change_config', 'Can change game config'),
            ('play_videos', 'Can play videos'),
        )