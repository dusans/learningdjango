from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    (r'^login_form/$', 'simpleLogin.views.login_form'),
    (r'^login_complete/$', 'simpleLogin.views.login_complete'),
    (r'^login/$', 'simpleLogin.views.login_user'),
    (r'^test_login/$', 'simpleLogin.views.test_login'),
    (r'^.*$', 'simpleLogin.views.login_form'),
)
