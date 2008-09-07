from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^prviDjango/', include('prviDjango.foo.urls')),

    # Uncomment the next line to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line for to enable the admin:
    (r'^admin/(.*)', admin.site.root),
    (r'^login/(.*)', 'prviDjango.register'),
    (r'^polls/', include('prviDjango.polls.urls')),
    (r'^lottery/', include('prviDjango.lottery.urls')),
)
