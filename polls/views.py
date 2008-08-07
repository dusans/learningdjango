# Create your views here.
from django.http import HttpResponse
from prviDjango.polls.models import Poll, Choice
from django.template import Context, loader
from django.shortcuts import render_to_response, get_object_or_404
from django.shortcuts import Http404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse



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

