from q3demotube.models import Demo, Video, VideoRating
from django import forms
from django.forms import ModelForm
from django import forms

class DemoForm(ModelForm):
    class Meta:
        model = Demo
        exclude = ('user', 'time_addet', 'view_count', 'rate', 'duration')

class DemoEdit(ModelForm):
    class Meta:
        model = Demo
        exclude = ('user', 'time_addet', 'demo', 'view_count', 'rate', 'duration')


class VideoForm(ModelForm):
    class Meta:
        model = Video
        fields = ('time', 'name',)
    tags = forms.CharField(max_length=300, min_length=2)

class VideoEdit(ModelForm):
    class Meta:
        model = Video
        fields = ('time', 'name', 'description')
    tags = forms.CharField(max_length=300, min_length=2)

class VideoRatingForm(ModelForm):
    class Meta:
        model = VideoRating
        fields = ('video', 'rate',)

class VideoTimeForm(ModelForm):
    class Meta:
        model = Video
        fields = ('start', 'end',)