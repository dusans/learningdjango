import datetime
import re
import random
from django import forms
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.core import serializers
from lottery.forms import *
from lottery.models import Draw


def drawList(req):
    if req.POST:
        form = FilterDraw(req.POST)
        #datetime.date(*map(int,(foo.split("-"))))
        #return HttpResponse(len(form['numbers'].data))
        # DATA
        draws = Draw.objects.filter(date__gte=form['from_date'].data,
                                    date__lte=form['till_date'].data,
                                    is_drawen=[0, 1][form['is_drawen'].data == "on"],
                                    user_id=0)

        #FILTER
        if len(form['numbers'].data):
            s2 = set(map(int, re.sub("[^\d\,]", "", form['numbers'].data).split(",")))
            if form['logical_and'].data == "on":
                draws = [d for d in draws if d.has_all(s2)]
            else:
                draws = [d for d in draws if d.has_one(s2)]

        return render_to_response('lottery/drawList.html', {'form': form, 'draws': draws})
    else:
        form = FilterDraw({ 'from_date':datetime.date(2007, 1, 1), 'till_date':datetime.date.today(),
                            'is_drawen':0, 'logical_and':1})
        return render_to_response('lottery/drawList.html', {'form': form, 'draws': Draw.objects.all()})

def history(req, page_number):
    draws = Draw.objects.all()
    p = Paginator(draws, 20)
    if int(page_number) in p.page_range:
        return render_to_response('lottery/history.html', { 'draws': p.page(page_number).object_list,
                                                            'pages': p.num_pages,
                                                            'page_number': int(page_number)})
    else:
        return HttpResponse("Noup not gona happen %s" % page_number)

@login_required
def lucky(req):
    if req.POST:
        form = LuckyForm(req.POST)
        draws = Draw.objects.filter(user=req.user)
        if form.is_valid():
            s2 = set(map(int, re.sub("[^\d\,]", "", form['check'].data).split(",")))
            draws = [d for d in draws if d.has_all(s2)]
    else:
        form = LuckyForm()
        draws = Draw.objects.filter(user=req.user)

    return render_to_response('lottery/lucky.html', {'form': form, 'draws': draws})

@login_required
def get_lucky(req):
    #CREATE LUCKY
    luckyNumbers = set()
    while len(luckyNumbers) < 8:
        luckyNumbers.add(random.randint(1,39))

    #SAVE LUCKY
    today = datetime.date.today()
    d = Draw(round_number=44, is_drawen=0, value=0, town="", is_old=0, user_id=req.user.id, date=today)
    d.save()
    for i in luckyNumbers:
        d.numbers_set.create(number=i, extra=0)

    d.save()

    #RETURN JSON
    data = serializers.serialize("json", d.numbers_set.all())
    return HttpResponse(data, mimetype="application/javascript") #("[%s]" % ",".join(map(str,luckyNumbers)))

@login_required
def my_lucky(req):
    #GET LUCKY
    luckyNumbers = LuckyForm(req.POST)['lucky'].data
    luckyNumbers = re.sub("[^\d\,]", "", str(luckyNumbers)).split(",")
    luckyNumbers = map(int, luckyNumbers)

    #SAVE LUCKY
    today = datetime.date.today()
    d = Draw(round_number=44, is_drawen=0, value=0, town="", is_old=0, user_id=req.user.id, date=today)
    d.save()
    for i in luckyNumbers:
        d.numbers_set.create(number=i, extra=0)
    d.save()

    #RETURN JSON
    data = serializers.serialize("json", d.numbers_set.all())
    return HttpResponse(data, mimetype="application/javascript")

def delete_lucky(req, drawId):
    Draw.objects.get(pk=drawId).delete()
    return HttpResponse("#%s deleted" % drawId)

@login_required
def test_login(request):
    return HttpResponse('U should see this only if u are logged in ' + str(request.user))