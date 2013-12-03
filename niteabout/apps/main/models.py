from django.db import models
from django.contrib.auth.models import User

from niteabout.apps.plan.models import NitePlan

class Event(models.Model):
    active = models.BooleanField()
    dt = models.DateTimeField()
    name = models.CharField(max_length=256)
    description = models.TextField()
    cost = models.IntegerField()
    attendees = models.ManyToManyField(User, blank=True)

    def __unicode__(self):
        return self.name

class UserProfile(models.Model):
    auth = models.OneToOneField(User)

    def __unicode__(self):
        return unicode(self.auth)

from niteabout.apps.main import signals
