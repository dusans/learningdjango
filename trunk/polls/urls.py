from django.conf.urls.defaults import *
from polls.models import Poll
# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()


info_dict = {
    'queryset': Poll.objects.all(),
}
urlpatterns = patterns('',
    (r'^$', 'django.views.generic.list_detail.object_list', info_dict),
    (r'^(?P<object_id>\d+)/$', 'django.views.generic.list_detail.object_detail', info_dict),
    url(r'^(?P<object_id>\d+)/results/$', 'django.views.generic.list_detail.object_detail', dict(info_dict, template_name='polls/results.html'), 'poll_results'),
    (r'^(?P<poll_id>\d+)/vote/$', 'polls.views.vote'),
    (r'^contactForm$', 'polls.views.contactForm'),
    (r'^pollForm$', 'polls.views.pollForm'),
    (r'^newPoll/$', 'polls.views.newPoll'),
    (r'^images/$', 'polls.views.uploadImages'),
    (r'^uploadImages/$', 'polls.views.uploadImages'),
    (r'^imageList/$', 'polls.views.imageList'),
)
