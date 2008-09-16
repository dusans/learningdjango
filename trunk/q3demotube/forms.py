from q3demotube.models import Demo, Video
from django import forms
from django.forms import ModelForm

class DemoForm(ModelForm):
    class Meta:
        model = Demo
        exclude = ('user',)

    #def __init__(self, user_id=None,*args,**kwargs):
        #super(DemoForm, self).__init__(*args, **kwargs)
        #self.user_id = user_id


class VideoForm(ModelForm):
    class Meta:
        model = Video
        fields = ('time',)


class VideoTimeForm(ModelForm):
    class Meta:
        model = Video
        fields = ('start', 'end',)