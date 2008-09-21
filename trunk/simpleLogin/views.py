# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django import forms
from django.forms.formsets import formset_factory
from django.contrib.auth.decorators import login_required

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

class TestForm(forms.Form):
    id_name = forms.IntegerField()
    name = forms.CharField()

def login_form(req):
    return render_to_response('simpleLogin/form.html', {'form': LoginForm()})

def login_user(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponse('U are loged in!!!')
        else:
            return HttpResponse('disabled account')
    else:
        return HttpResponse('invalid login')

@login_required
def test_login(request):
    return HttpResponse('U should see this only if u are logged in ' + str(request.user))

def test_form_set(request):
    TestFormSet = formset_factory(TestForm, extra=10)
    formSet = TestFormSet()
    return render_to_response('lottery/formSet.html', {'formSet': formSet})

def form_set_submit(request):
    TestFormSet = formset_factory(TestForm)
    formSet = TestFormSet(request.POST)
    return render_to_response('lottery/formSet.html', {'formSet': formSet})
