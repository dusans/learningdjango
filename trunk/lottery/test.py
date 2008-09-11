import datetime
import random
import re
from lottery.models import Draw, Numbers
from django.contrib.auth.models import User
from mesta import towns

today = datetime.date.today()
xgo4 = User.objects.get(pk=6)

for k in range(10):
    d = Draw(round_number=44, is_drawen=0, value=0, town="", is_old=0, user_id=xgo4.id, date=today)
    d.save()
    for i in range(7):
        d.numbers_set.create(number=random.randint(1,38), extra=0)

    d.numbers_set.create(number=39, extra=1)
    d.save()

'''d = Draw.objects.get(pk=4)
d.save()

", ".join(map(str, d.numbers_set.all()))

d = Draw.objects.get(pk=4)
s1 = set([i.number for i in d.numbers_set.all()])

#From input string from form create a set of numbers
s2 = set(map(int, re.sub("[^\d\,]", "", foo).split(",")))'''
