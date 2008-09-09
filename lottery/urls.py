from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^drawList/$', 'prviDjango.lottery.views.drawList'),
    (r'^history/(?P<page_number>\d+)/$', 'prviDjango.lottery.views.history'),
)
