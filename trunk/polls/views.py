# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from polls.models import Poll, Choice
from django.template import Context, loader
from django.shortcuts import render_to_response, get_object_or_404, Http404
from django.core.urlresolvers import reverse
from django import forms
from django.forms import ModelForm


class PollForm(ModelForm):
    class Meta:
        model = Poll

class ChoiceForm(ModelForm):
    class Meta:
        model = Choice

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField()
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)

def contactForm(req):
    #poll = Poll.objects.get(pk=11)
    choice = Choice.objects.get(pk=2)
    form = ChoiceForm(instance=choice) #PollForm(instance=poll)
    return render_to_response('polls/contact.html', {'form': form})

def pollForm(req):
    poll = Poll.objects.get(pk=2)
    form = PollForm(instance=poll)
    return render_to_response('polls/pollForm.html', {'form': form})

def newPoll(req):
    poll = Poll()
    f = PollForm(req.POST, instance=poll)
    if f.is_valid():
        foo = f.save()
        return HttpResponse('%s je stranjen' % foo)
    return HttpResponse('Not valid')

def vote(req, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)

    try:
        selected_choice = p.choice_set.get(pk=req.POST['choice'])
    except KeyError, Choice.DoesNotExist:
        #Redisplay the poll voting form
        return render_to_response('polls/poll_detail.html', {'object': p, 'error_message': "Yout didnt select a choise"})
    else:
        selected_choice.votes += 1
        selected_choice.save()
        #Always return an HttpResponseRedirect after success
        return HttpResponseRedirect(reverse('poll_results', args=(p.id,)))

