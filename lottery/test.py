import datetime
import random
import re
from prviDjango.lottery.models import Draw, Numbers

'''datum = datetime.date.today()
d = Draw(round_number=2, is_drawen=0, value=40000.00, town="Kranj", is_old=0, user_id=1, date=datum)
d.save()

d = Draw.objects.get(pk=4)

for i in range(7):
    d.numbers_set.create(number=random.randint(1,39), extra=0)

d.numbers_set.create(number=22, extra=1)
d.save()

", ".join(map(str, d.numbers_set.all()))'''

d = Draw.objects.get(pk=4)
s1 = set([i.number for i in d.numbers_set.all()])

#From input string from form create a set of numbers
s2 = set(map(int, re.sub("[^\d\,]", "", foo).split(",")))
