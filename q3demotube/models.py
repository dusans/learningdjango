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
    demo = models.FileField(upload_to='q3/demos')
    time_addet = models.DateTimeField(default=datetime.datetime.now)

    def __unicode__(self):
        return self.name

class Video(models.Model):
    demo = models.ForeignKey(Demo)
    name = models.CharField(max_length=200, blank=True)
    videoFile = models.FileField(upload_to='q3/videos')
    thumbnail = models.ImageField(upload_to='q3/thumbnails')
    bigImage = models.ImageField(upload_to='q3/images', null=True)
    description = models.TextField(blank=True)
    time = models.TimeField()
    start = models.TimeField(null=True)
    end = models.TimeField(null=True)
    duration = models.TimeField(null=True)
    capture_time = models.FloatField(null=True)
    compression_time = models.FloatField(null=True)
    has_images = models.BooleanField()
    has_video = models.BooleanField()
    time_addet = models.DateTimeField(default=datetime.datetime.now)
    view_count = models.PositiveIntegerField(default=0)
    rate = models.PositiveIntegerField(default=5)


    def __unicode__(self):
        return "%s - %s" % (self.name, self.time)

    def can_be_captured(self):
        return (self.end.minute * 60 + self.end.second) - (self.start.minute * 60 + self.start.second) <=  30

    def set_tags(self, tags):
        for t in self.tag_set.all():
            t.delete()
        for tag in tags.split(","):
            self.tag_set.create(tag=tag.strip())

    def tags(self):
        return ", ".join([t.tag for t in self.tag_set.all()])

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

    def __unicode__(self):
        return "%s -> %s" % (self.user.username, self.video.name)

class VideoRating(models.Model):
    user = models.ForeignKey(User)
    video = models.ForeignKey(Video)
    rate = models.IntegerField()

