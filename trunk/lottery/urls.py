from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    (r'^drawList/$', 'lottery.views.drawList'),
    (r'^history/(?P<page_number>\d+)/$', 'lottery.views.history'),
    (r'^lucky/$', 'lottery.views.lucky'),
    (r'^get_lucky/$', 'lottery.views.get_lucky'),
    (r'^my_lucky/$', 'lottery.views.my_lucky'),
    (r'^delete_lucky/(?P<drawId>\d+)$', 'lottery.views.delete_lucky'),

    (r'^test_login/$', 'simpleLogin.views.test_login'),
    (r'^formSet/$', 'simpleLogin.views.test_form_set'),
    (r'^formSetSubmit/$', 'simpleLogin.views.form_set_submit'),
)
