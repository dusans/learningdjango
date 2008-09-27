import datetime
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    parent_cat = models.ForeignKey('self', null=True)
    user = models.ForeignKey(User, null=True)
    is_private = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

class Demo(models.Model):
    category = models.ForeignKey(Category)
    user = models.ForeignKey(User)
    name = models.CharField(max_length=200, blank=True)
    demo = models.FileField(upload_to='q3demos')
    time_addet = models.DateTimeField(default=datetime.datetime.now)

class Video(models.Model):
    demo = models.ForeignKey(Demo)
    name = models.CharField(max_length=200, blank=True)
    videoFile = models.FileField(upload_to='q3/videos')
    thumbnail = models.ImageField(upload_to='q3/images')
    description = models.TextField(blank=True)
    time = models.TimeField()
    start = models.TimeField(null=True)
    end = models.TimeField(null=True)
    has_images = models.BooleanField()
    has_video = models.BooleanField()
    time_addet = models.DateTimeField(default=datetime.datetime.now)

    def __unicode__(self):
        return "%s - %s - %s" % (self.demo.demo.url, self.name, self.time)

    def can_be_captured(self):
        return (self.end.minute * 60 + self.end.second) - (self.start.minute * 60 + self.start.second) <=  30

    def rated(self):
        try:
            rates = [vr.rate for vr in self.videorating_set.all()]
            return round(sum(rates) / float(len(rates)))
        except:
            return 0

    def set_tags(self, tags):
        for t in self.tag_set.all():
            t.delete()
        for tag in tags.split(","):
            self.tag_set.create(tag=tag.strip())

    def tags(self):
        return ", ".join([t.tag for t in self.tag_set.all()])

class Images(models.Model):
    video = models.ForeignKey(Video)
    image = models.ImageField(upload_to='q3/images')

class Tag(models.Model):
    video = models.ForeignKey(Video)
    tag = models.SlugField()

class View(models.Model):
    video = models.ForeignKey(Video)
    user = models.ForeignKey(User, null=True)
    ip = models.IPAddressField()
    time_addet = models.DateTimeField(default=datetime.datetime.now)

class Favorite(models.Model):
    user = models.ForeignKey(User)
    video = models.ForeignKey(Video)

class VideoRating(models.Model):
    user = models.ForeignKey(User)
    video = models.ForeignKey(Video)
    rate = models.IntegerField()

