from q3demotube.models import Demo, Video, VideoRating
from django import forms
from django.forms import ModelForm
from django import forms

class DemoForm(ModelForm):
    class Meta:
        model = Demo
        exclude = ('user', 'time_addet',)

    #def __init__(self, user_id=None,*args,**kwargs):
        #super(DemoForm, self).__init__(*args, **kwargs)
        #self.user_id = user_id

class VideoForm(forms.Form):
    time = forms.TimeField(required=True)
    tags = forms.CharField(max_length=300, min_length=2)

    #class Meta:
        #model = Video
        #fields = ('time',)

class VideoRatingForm(ModelForm):
    class Meta:
        model = VideoRating
        fields = ('video', 'rate',)

class VideoTimeForm(ModelForm):
    class Meta:
        model = Video
        fields = ('start', 'end',)