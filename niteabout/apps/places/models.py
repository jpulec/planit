from django.db import models
from django.contrib.gis.db import models as geomodels
from django.contrib.auth.models import User

from djangoratings.fields import RatingField


from decimal import Decimal

import math

import logging

logger = logging.getLogger(__name__)

class Tag(models.Model):
    key = models.CharField(max_length="128")
    value = models.CharField(max_length="256")

    def __unicode__(self):
        return self.key + ":" + self.value

    class Meta:
        unique_together = ('key', 'value',)

class OSMPlace(models.Model):
    osm_id = models.BigIntegerField(blank=True, null=True)
    tags = models.ManyToManyField('Tag', null=True, blank=True)
    timestamp = models.DateTimeField(null=True)
    version = models.IntegerField(null=True)

    class Meta:
        abstract= True

    def __unicode__(self):
        return unicode(self.osm_id)

class Cuisine(models.Model):
    name = models.CharField(max_length=128)

    def __unicode__(self):
        return self.name.capitalize()

class PlaceCategory(models.Model):
    name = models.CharField(max_length=128)

    def __unicode__(self):
        return self.name.capitalize()

class FeatureName(models.Model):
    name = models.CharField(max_length=128)
    categories = models.ManyToManyField('PlaceCategory')

    def __unicode__(self):
        return self.name.capitalize()

class FeatureLabel(models.Model):
    feature_name = models.ForeignKey('FeatureName')
    value = models.IntegerField()
    label = models.CharField(max_length=256)

    def __unicode__(self):
        return unicode(self.feature_name) + ":" + unicode(self.value) + ":" + self.label

class Feature(models.Model):
    feature_name = models.ForeignKey('FeatureName')
    place = models.ForeignKey('Place')
    rating = RatingField(range=range(-5,6), can_change_vote=True, weight=10)

    class Meta:
        unique_together = ('feature_name', 'place',)

    def get_label(self):
        try:
            label = FeatureLabel.objects.get(feature_name=self.feature_name, value=round(self.rating.get_rating()))
            return label.label
        except FeatureLabel.DoesNotExist as e:
            return ""

    def get_score(self):
        return self.rating.get_rating()

    def get_votes(self):
        return self.rating.votes

    def __unicode__(self):
        return unicode(self.place) + ":" + unicode(self.feature_name) + ":" + unicode(self.rating)

class Place(OSMPlace):
    name = models.CharField(max_length=256)
    geom = geomodels.PointField()
    categories = models.ManyToManyField('PlaceCategory')
    cuisines = models.ManyToManyField('Cuisine', blank=True, null=True)
    objects = geomodels.GeoManager()

    def __unicode__(self):
        return unicode(self.name)

    def __sub__(self, other):
        if isinstance(other, Place):
            # TODO: do this faster and less naively
            total = 0
            for feature in self.feature_set.all():
                for ofeature in other.feature_set.all():
                    if ofeature.feature_name == feature.feature_name:
                        total += pow(feature.get_score() - ofeature.get_score(), 2)
                        break
            return math.sqrt(total)
        elif isinstance(other, NiteTemplate):
            # TODO: do this faster and less naively
            total = 0
            for feature in self.feature_set.all():
                for nitefeature in other.nitefeature_set.all():
                    if nitefeature.feature_name == feature.feature_name:
                        total += pow(feature.get_score() - float(nitefeature.score), 2)
                        break
            return math.sqrt(total)
        else:
            raise TypeError

    def category_names(self):
        return ', '.join([c.name for c in self.categories.all()])
    category_names.short_description = "Categories"

class HourSpan(models.Model):
    open = models.TimeField()
    close = models.TimeField()

    def __unicode__(self):
        return unicode(self.open) + "-" + unicode(self.close)

class Hours(models.Model):
    place = models.ForeignKey('Place')
    sunday = models.ForeignKey('HourSpan', related_name="sunday_hours", blank=True, null=True)
    monday = models.ForeignKey('HourSpan', related_name="monday_hours", blank=True, null=True)
    tuesday = models.ForeignKey('HourSpan', related_name="tuesday_hours", blank=True, null=True)
    wednessday = models.ForeignKey('HourSpan', related_name="wednesday_hours", blank=True, null=True)
    thursday = models.ForeignKey('HourSpan', related_name="thursday_hours", blank=True, null=True)
    friday = models.ForeignKey('HourSpan', related_name="friday_hours", blank=True, null=True)
    saturday = models.ForeignKey('HourSpan', related_name="saturday_hours", blank=True, null=True)

    def __unicode__(self):
        return unicode(self.place) + " hours"

DAYS_OF_WEEK = (
        ('Su', 'Sunday'),
        ('M', 'Monday'),
        ('Tu', 'Tuesday'),
        ('W', 'Wednesday'),
        ('Th', 'Thursday'),
        ('F', 'Friday'),
        ('Sa', 'Saturday'),
        )

class Deal(models.Model):
    place = models.ForeignKey('Place')
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    day = models.IntegerField(max_length=1, choices=DAYS_OF_WEEK, blank=True, null=True)
    deal = models.TextField()

    def __unicode__(self):
        return unicode(self.place) + " has " + self.deal + " on " + self.get_day_display() + " starting at " + unicode(self.start_time) + " until " + unicode(self.end_time)

from niteabout.apps.plan.models import NiteTemplate
