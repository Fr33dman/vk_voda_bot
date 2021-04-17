from __future__ import unicode_literals

from django.db import models

class User_level(models.Model):
    user_id = models.IntegerField(primary_key=True, null=False, unique=True, help_text='Saves persons user_id')
    level = models.SmallIntegerField(null=False, help_text='Saves at witch level(step) of the order user is')
    date = models.DateTimeField(auto_now=True, help_text='Saves time of last message from this user')
    '''
    :param int user_id: User id from received message
    :param int level: Level of user order
    :param date: Not stable
    '''

    def __unicode__(self):
        return self.user_id