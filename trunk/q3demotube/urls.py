from django.conf.urls.defaults import *
from polls.models import Poll
# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()


info_dict = {
    'queryset': Poll.objects.all(),
}
urlpatterns = patterns('',
    (r'^videos/$', 'q3demotube.views.videos'),
    (r'^add_demo/$', 'q3demotube.views.add_demo'),
    (r'^demo_list/$', 'q3demotube.views.demo_list'),
    (r'^times/(?P<demo_id>\d+)/$', 'q3demotube.views.times'),
    (r'^get_images/(?P<demo_id>\d+)/$', 'q3demotube.views.get_images'),
    (r'^get_videos/(?P<demo_id>\d+)/$', 'q3demotube.views.get_videos'),
    (r'^edit_time/(?P<video_id>\d+)/$', 'q3demotube.views.edit_time'),
    (r'^.*$', 'q3demotube.views.add_demo'),
)
