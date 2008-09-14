from q3demotube.forms import DemoForm, VideoForm
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.forms.formsets import formset_factory
from django.contrib.auth.decorators import login_required
from q3demotube.models import Demo, Video
from datetime import time, timedelta
# Create your views here.

def addSeconds(t, n):
    td = timedelta(seconds=(t.minute * 60) + (t.second)) + timedelta(seconds=n)
    return time(td.seconds / 3600, td.seconds / 60, td.seconds % 60)

@login_required
def add_demo(request):
    VideoFormSet = formset_factory(VideoForm, extra=3)
    if request.POST:
        print type(request.user.id), request.user.id
        demoForm = DemoForm(request.POST, request.FILES)
        videoForm = VideoFormSet(request.POST)
        #print "demoForm.is_valid()", demoForm.is_valid()
        if demoForm.is_valid():
            d = demoForm.save(commit=False)
            d.user_id = request.user.id
            d.save()

            for video in videoForm.forms:
                if video.is_valid() and video['time'].data:
                    #print "video.is_valid()", video.is_valid()
                    v = video.save(commit=False)
                    v.demo_id = d.id
                    v.start = addSeconds(v.time, -10)
                    v.end = addSeconds(v.time, 8)
                    v.save()
        else:
            #print "foo"
            return render_to_response('q3demotube/add_demo.html', {'demoForm':demoForm, 'videoForm':videoForm})

    demoForm = DemoForm()
    videoForm = VideoFormSet()
    return render_to_response('q3demotube/add_demo.html', {'demoForm':demoForm, 'videoForm':videoForm})

#@login_required
def demo_list(request):
    demos = Demo.objects.all()
    return render_to_response('q3demotube/demo_list.html', {'demos': demos})


def times(request, demo_id):
    timeList = Video.objects.filter(demo=demo_id)
    demo = Demo.objects.get(pk=demo_id)
    return render_to_response('q3demotube/times.html', {'timeList': timeList, 'demo': demo})

def get_images(request, demo_id):
    videos = Video.objects.filter(demo=demo_id)
    for video in videos:
        if not video.has_images:
            pass
