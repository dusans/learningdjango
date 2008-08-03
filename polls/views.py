# Create your views here.
from django.http import HttpResponse
from prviDjango.polls.models import Poll
from django.template import Context, loader
from django.shortcuts import render_to_response, get_object_or_404
from django.shortcuts import Http404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

def index(request):
    latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
    #t = loader.get_template('polls/index.html')
    #c = Context({'latest_poll_list': latest_poll_list})
    return render_to_response('polls/index.html', {'latest_poll_list': latest_poll_list})

def detail(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    return render_to_response('polls/detail.html', {'poll': p})

def vote(req, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)

    try:
        selected_choice = p.choice_set.get(pk=req.POST['choice'])