from q3demotube.forms import DemoForm, VideoForm, VideoTimeForm, VideoRatingForm
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.forms.formsets import formset_factory
from django.contrib.auth.decorators import login_required
from q3demotube.models import Demo, Video, Category
from datetime import time, timedelta
from django.conf import settings
from q3demotube.q3demo import addSec, getSec, getMMEImages, getMMEVideos
# Create your views here.

@login_required
def add_demo(request):
    VideoFormSet = formset_factory(VideoForm, extra=3)
    if request.POST:
        demoForm = DemoForm(request.POST, request.FILES)
        videoForm = VideoFormSet(request.POST)

        if demoForm.is_valid():
            d = demoForm.save(commit=False)
            d.user_id = request.user.id
            d.save()

            for form in videoForm.forms:
                if form.is_valid():
                    print form
                    timeIn2 = form.cleaned_data['time']
                    print timeIn2
                    video = d.video_set.create(time=timeIn2, start=addSec(timeIn2, -10), end=addSec(timeIn2, 8))
                    # Tags
                    for tag in form.cleaned_data['tags'].split(" "):
                        video.tag_set.create(tag=tag)
                    '''v = video.save(commit=False)
                    v.demo_id = d.id
                    v.start = addSec(v.time, -10)
                    v.end = addSec(v.time, 8)
                    v.save()'''
        else:
            return render_to_response('q3demotube/add_demo.html', { 'demoForm':demoForm, 'videoForm':videoForm,
                                                                    'MEDIA_URL': settings.MEDIA_URL})

    demoForm = DemoForm({'category': Category.objects.latest('id').id})
    videoForm = VideoFormSet()
    return render_to_response('q3demotube/add_demo.html', { 'demoForm':demoForm, 'videoForm':videoForm,
                                                            'MEDIA_URL': settings.MEDIA_URL})

#@login_required
def demo_list(request):
    demos = Demo.objects.all()
    return render_to_response('q3demotube/demo_list.html', {'demos': demos, 'MEDIA_URL': settings.MEDIA_URL})

def videos(request):
    videos = Video.objects.filter(has_video=True)
    return render_to_response('q3demotube/videos.html', {'videos': videos, 'MEDIA_URL': settings.MEDIA_URL})

def times(request, demo_id):
    timeList = Video.objects.filter(demo=demo_id)
    demo = Demo.objects.get(pk=demo_id)
    return render_to_response('q3demotube/times.html', {'timeList': timeList, 'demo': demo})

@login_required
def get_images(request, demo_id):
    demo = Demo.objects.get(pk=demo_id)
    if demo.video_set.filter(has_images=False).count():
        getMMEImages(demo_id)
    return times(request, demo_id)

@login_required
def get_videos(request, demo_id):
    demo = Demo.objects.get(pk=demo_id)
    if demo.video_set.filter(has_video=False).count():
        getMMEVideos(demo_id)
    return times(request, demo_id)

def video(request, video_id):
    video = Video.objects.get(pk=video_id)
    video.view_set.create(ip=request.META['REMOTE_ADDR'], user_id=request.user.id)
    return render_to_response('q3demotube/video.html', {'video': video, 'MEDIA_URL': settings.MEDIA_URL,
                                'ratings': range(1,6), 'rated': video.rated()})

@login_required
def rate_video(request):
    if request.POST:
        video_id, rate = request.POST['object_id'], request.POST['rate']
        video = Video.objects.get(pk=video_id)
        if rate in map(str, range(1,11)) and not video.videorating_set.filter(user=request.user.id).count():
            video.videorating_set.create(rate=rate, user_id=request.user.id)
            return HttpResponse("Video has been rated")
        return HttpResponse("Already voted!")
    return HttpResponse("Post Needet!")

@login_required
def add_favorite(request):
    from q3demotube.models import Favorite
    if request.method == "POST":
        f = Favorite(user_id=request.user.id, video_id=request.POST['video_id'])
        f.save()
        return HttpResponse("Favorite addet!")
    return HttpResponse("No!")

def edit_time(request, video_id=0):
    video = Video.objects.get(pk=video_id)
    start = addSec(video.time, -15)

    if request.POST:
        timeForm = VideoTimeForm(request.POST, instance=video)
        if timeForm.is_valid():
            timeForm.save()
        return times(request, video.demo_id)
    else:
        timeForm = VideoTimeForm({'start': video.start, 'end': video.end})

    images = [(str(addSec(start, i / 4)), "0" * (10 - len(str(i))) + str(i)) for i in range(140)]

    return render_to_response('q3demotube/edit_time.html', {'images': images, 'MEDIA_URL': settings.MEDIA_URL,
                                                            'demo_id': video.demo.id, 'timeForm': timeForm,
                                                            'videoTime': str(video.time), 'video': video})