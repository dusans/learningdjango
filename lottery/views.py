import datetime
import re
from django import forms
from django.shortcuts import render_to_response
from django.http import HttpResponse
from prviDjango.lottery.models import Draw

class FilterDraw(forms.Form):
    from_date = forms.DateField()
    till_date = forms.DateField()
    is_drawen = forms.BooleanField(required=False)
    logical_and = forms.BooleanField(required=False)
    numbers = forms.CharField(max_length=200)

#a.items()[2][1].keys()
def drawList(req):
    if req.POST:
        form = FilterDraw(req.POST)
        #datetime.date(*map(int,(foo.split("-"))))
        #return HttpResponse(len(form['numbers'].data))
        draws = Draw.objects.filter(date__gte=form['from_date'].data,
                                    date__lte=form['till_date'].data,
                                    is_drawen=[0, 1][form['is_drawen'].data == "on"])

        if len(form['numbers'].data):
            s2 = set(map(int, re.sub("[^\d\,]", "", form['numbers'].data).split(",")))
            if form['logical_and'].data == "on":
                draws = [d for d in draws if d.has_all(s2)]
            else:
                draws = [d for d in draws if d.has_one(s2)]

        return render_to_response('lottery/drawList.html', {'form': form, 'draws': draws})
    else:
        form = FilterDraw({'from_date':datetime.date(2007, 1, 1), 'till_date':datetime.date.today(), 'is_drawen':0, 'logical_and':1})
        draws = Draw.objects.all()
        return render_to_response('lottery/drawList.html', {'form': form, 'draws': draws})