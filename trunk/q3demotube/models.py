from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    parent_cat = models.ForeignKey('self', null=True)

    def __unicode__(self):
        return self.name

class Demo(models.Model):
    category = models.ForeignKey(Category)
    user = models.ForeignKey(User)
    name = models.CharField(max_length=200, blank=True)
    demo = models.FileField(upload_to='q3demos')

class Video(models.Model):
    demo = models.ForeignKey(Demo)
    name = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    time = models.TimeField()
    start = models.TimeField(null=True)
    end = models.TimeField(null=True)
    has_images = models.BooleanField()
    has_video = models.BooleanField()

    def __unicode__(self):
        return "%s - %s - %s" % (self.demo.demo.url, self.name, self.time)

class VideoRating(models.Model):
    user = models.ForeignKey(User)
    video = models.ForeignKey(Video)
    rate = models.IntegerField()