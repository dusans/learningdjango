import re
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Draw(models.Model):
    round_number = models.IntegerField()
    date = models.DateField()
    is_drawen = models.BooleanField()
    value = models.FloatField()
    town = models.CharField(max_length=200)
    is_old = models.BooleanField()
    user = models.ForeignKey(User)

    def __unicode__(self):
        return ", ".join(map(str,[self.round_number, self.date, self.value, self.town.encode('unicode')]))

    def numbers_list(self):
        return ", ".join(map(str, sorted([i.number for i in self.numbers_set.filter(extra=0)])))

    def extra_number(self):
        if self.numbers_set.count():
            return self.numbers_set.filter(extra=1)[0]
        else:
            return 0

    def has_all(self, s2):
        s1 = set([i.number for i in self.numbers_set.all()])
        #s2 = set(map(int, re.sub("[^\d\,]", "", numbers_string).split(",")))
        return not len(s2 - s1)

    def has_one(self, s2):
        s1 = set([i.number for i in self.numbers_set.all()])
        return (s2 - s1) != s2

class Numbers(models.Model):
    draw = models.ForeignKey(Draw)
    number = models.IntegerField()
    extra = models.BooleanField()

    def __unicode__(self):
        return str(self.number)

#class LuckyNumber(models.Model):
#    number = models.IntegerField()

