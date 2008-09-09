import datetime
import random
import re
from prviDjango.lottery.models import Draw, Numbers
from mesta import towns

datum = datetime.date.today()
for townName, num in zip(towns.split(), range(len(towns.split()))):
    d = Draw(round_number=num, is_drawen=0, value=random.randrange(1, 1000000), town=townName, is_old=0, user_id=1, date=datum)
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
