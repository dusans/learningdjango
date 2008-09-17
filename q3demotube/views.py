from q3demotube.forms import DemoForm, VideoForm, VideoTimeForm
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.forms.formsets import formset_factory
from django.contrib.auth.decorators import login_required
from q3demotube.models import Demo, Video
from datetime import time, timedelta
from django.conf import settings
from q3demotube.q3demo import addSec, getSec, getMMEImages, getMMEVideos
# Create your views here.

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
                    v.start = addSec(v.time, -10)
                    v.end = addSec(v.time, 8)
                    v.save()
        else:
            #print "foo"
            return render_to_response('q3demotube/add_demo.html', { 'demoForm':demoForm, 'videoForm':videoForm,
                                                                    'MEDIA_URL': settings.MEDIA_URL})

    demoForm = DemoForm()
    videoForm = VideoFormSet()
    return render_to_response('q3demotube/add_demo.html', { 'demoForm':demoForm, 'videoForm':videoForm,
                                                            'MEDIA_URL': settings.MEDIA_URL})

#@login_required
def demo_list(request):
    demos = Demo.objects.all()
    return render_to_response('q3demotube/demo_list.html', {'demos': demos})

def videos(request):
    videos = Video.objects.filter(has_video=True)
    return render_to_response('q3demotube/videos.html', {'videos': videos, 'MEDIA_URL': settings.MEDIA_URL})

def times(request, demo_id):
    timeList = Video.objects.filter(demo=demo_id)
    demo = Demo.objects.get(pk=demo_id)
    return render_to_response('q3demotube/times.html', {'timeList': timeList, 'demo': demo})

def get_images(request, demo_id):
    demo = Demo.objects.get(pk=demo_id)
    if demo.video_set.filter(has_images=False).count():
        getMMEImages(demo_id)
    return times(request, demo_id)

def get_videos(request, demo_id):
    demo = Demo.objects.get(pk=demo_id)
    if demo.video_set.filter(has_video=False).count():
        getMMEVideos(demo_id)
    return times(request, demo_id)

def edit_time(request, video_id=0):
    video = Video.objects.get(pk=video_id)
    start = addSec(video.time, -20)

    if request.POST:
        timeForm = VideoTimeForm(request.POST, instance=video)
        if timeForm.is_valid():
            timeForm.save()
    else:
        timeForm = VideoTimeForm({'start': video.start, 'end': video.end})

    images = [(str(addSec(start, i / 4)), "0" * (10 - len(str(i))) + str(i)) for i in range(180)]

    return render_to_response('q3demotube/edit_time.html', {'images': images, 'MEDIA_URL': settings.MEDIA_URL,
                                                            'demo_id': video.demo.id, 'timeForm': timeForm,
                                                            'videoTime': str(video.time), 'video': video})