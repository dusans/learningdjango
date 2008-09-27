from django.conf.urls.defaults import *
from q3demotube.models import Demo, Video
#from django.views.generic.create_update import delete_object
# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()




video_dict = {
    'model': Video,
    'post_delete_redirect': '/q3demotube/demo_list/'
}

urlpatterns = patterns('',
    (r'^videos/$', 'q3demotube.views.videos'),
    (r'^videos/(?P<page_number>\d+)/$', 'q3demotube.views.videos'),
    (r'^my_videos/$', 'q3demotube.views.my_videos'),
    (r'^my_videos/(?P<page_number>\d+)/$', 'q3demotube.views.my_videos'),
    (r'^video/(?P<video_id>\d+)/$', 'q3demotube.views.video'),
    (r'^video_edit/(?P<video_id>\d+)/$', 'q3demotube.views.video_edit'),
    (r'^delete_video/(?P<object_id>\d+)/$', 'q3demotube.views.delete_video'),
    (r'^rate_video/$', 'q3demotube.views.rate_video'),
    (r'^add_demo/$', 'q3demotube.views.add_demo'),
    (r'^demo_list/$', 'q3demotube.views.demo_list'),
    (r'^demo/(?P<demo_id>\d+)/$', 'q3demotube.views.demo_view'),
    (r'^edit_demo/(?P<demo_id>\d+)/$', 'q3demotube.views.demo'),
    (r'^delete_demo/(?P<object_id>\d+)/$', 'q3demotube.views.delete_demo'),
    (r'^get_images/(?P<demo_id>\d+)/$', 'q3demotube.views.get_images'),
    (r'^get_videos/(?P<demo_id>\d+)/$', 'q3demotube.views.get_videos'),
    (r'^edit_time/(?P<video_id>\d+)/$', 'q3demotube.views.edit_time'),
    (r'^add_favorite/$', 'q3demotube.views.add_favorite'),
    (r'^.*$', 'q3demotube.views.videos'),
)
