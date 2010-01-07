from q3demotube.models import Demo, Video, Category
from q3demotube.forms import *
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.forms.formsets import formset_factory
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.template import RequestContext
from django.views.generic.simple import direct_to_template
from django.conf import settings
from q3demotube.q3demo import addSec, getSec, getMMEImages, getMMEVideos
from django.views.generic.create_update import delete_object
from common.SortHeaders import SortHeaders

@login_required
def add_demo(request):
    VideoFormSet = formset_factory(VideoForm, extra=3)
    if request.method == "POST":
        demoForm = DemoForm(request.POST, request.FILES) #, initial={'user_id': request.user.id}
        videoForm = VideoFormSet(request.POST)

        if demoForm.is_valid():
            d = demoForm.save(commit=False)
            d.user_id = request.user.id
            d.save()
            #>>> for t in v.tag_set.all():
            #...     t.delete()
            for f in videoForm.forms:
                if f.is_valid():
                    if 'time' in f.cleaned_data and 'tags' in f.cleaned_data:
                        name, timeIn = f.cleaned_data['name'], f.cleaned_data['time']
                        start, end = addSec(timeIn, -10), addSec(timeIn, 8)
                        video = d.video_set.create(name=name, time=timeIn, start=start, end=end, duration=addSec(end, - getSec(start)))
                        # Tags
                        video.set_tags(f.cleaned_data['tags'])
                        #for tag in f.cleaned_data['tags'].split(","):
                            #video.tag_set.create(tag=tag.strip())
        else:
            return direct_to_template(request, 'q3demotube/add_demo.html', { 'demoForm':demoForm, 'videoForm':videoForm})

    demoForm = DemoForm({'category': Category.objects.latest('id').id})
    videoForm = VideoFormSet()
    return direct_to_template(request, 'q3demotube/add_demo.html', { 'demoForm':demoForm, 'videoForm':videoForm})

@login_required
def demo_list(request):
    LIST_HEADERS = [("Name", "name"),  ("Demo", "demo"),  ("Category", "category__name"),
                        ("Date", "time_addet"),  ("User", "user__username"),  ("#Frags", None),
                        ("#Edit", None),  ("#Delete", None)]

    sort_headers = SortHeaders(request, LIST_HEADERS)
    demos = Demo.objects.filter(user=request.user).order_by(sort_headers.get_order_by())
    return direct_to_template(request, 'q3demotube/demo_list.html', {'demos': demos, 'headers': list(sort_headers.headers())})

@login_required
def demo_view(request, demo_id):
    demo = Demo.objects.get(pk=demo_id, user=request.user)
    if request.method == 'POST':
        demoEdit = DemoEdit(request.POST, instance=demo)
        if demoEdit.is_valid():
            demoEdit.save()
            return demo_list(request)

    videos = demo.video_set.all()
    demoEdit = DemoEdit(instance=demo)
    return direct_to_template(request, 'q3demotube/demo.html', {'videos': videos,
                                                        'demo': demo, 'demoEdit': demoEdit})

@login_required
def delete_demo(request, object_id):
    if Demo.objects.get(pk=object_id, user=request.user):
        return delete_object(request, object_id=object_id, model=Demo, post_delete_redirect='/q3demotube/demo_list/')

@login_required
def delete_video(request, object_id):
    video = Video.objects.get(pk=object_id, demo__user=request.user)
    if video:
        return delete_object(request, object_id=object_id, model=Video, post_delete_redirect='/q3demotube/demo/%s/' % video.demo.id)

def videos(request, page_number=1):
    LIST_HEADERS = [("name", "name"), ("duration", "duration"), ("time_addet", "time_addet"),
                    ("view_count", "view_count"), ("rate", "rate"), ("capture_time", "capture_time")]

    sort_headers = SortHeaders(request, LIST_HEADERS)
    videos = Video.objects.filter(has_video=True).order_by(sort_headers.get_order_by())
    p = Paginator(videos, 9)
    return direct_to_template(request, 'q3demotube/videos.html', {'videos': p.page(page_number).object_list,
                                'pages': p.num_pages,
                                'page_number': int(page_number), 'headers': list(sort_headers.headers())})


@login_required
def my_videos(request, page_number=1):
    videos = Video.objects.filter(has_video=True, demo__user=request.user).order_by('-time_addet')
    p = Paginator(videos, 9)
    return direct_to_template(request, 'q3demotube/my_videos.html', {'videos': p.page(page_number).object_list,
                                                            'pages': p.num_pages,
                                                            'page_number': int(page_number)})

def video(request, video_id):
    video = Video.objects.get(pk=video_id)
    video.view_set.create(ip=request.META['REMOTE_ADDR'], user_id=request.user.id)
    video.view_count += 1
    video.save()
    return direct_to_template(request, 'q3demotube/video.html', {'video': video,
                                'ratings': range(1,6), 'rated': video.rate})

@login_required
def video_edit(request, video_id):
    video = Video.objects.get(pk=video_id, demo__user=request.user.id)
    if request.method == 'POST':
        videoEdit = VideoEdit(request.POST, instance=video, initial={'tags': video.tags()})
        if videoEdit.is_valid():
            v = videoEdit.save()
            v.set_tags(videoEdit.cleaned_data['tags'])

        return direct_to_template(request, 'q3demotube/video_edit.html', {'videoEdit': videoEdit, 'video': video})
    else:
        videoEdit = VideoEdit(instance=video, initial={'tags': video.tags()})
        return direct_to_template(request, 'q3demotube/video_edit.html', {'videoEdit': videoEdit, 'video': video})

@login_required
def rate_video(request):
    if request.POST:
        video_id, rate = request.POST['object_id'], int(request.POST['rate'])
        video = Video.objects.get(pk=video_id)
        if rate in range(1,11) and not video.videorating_set.filter(user=request.user.id).count():
            video.videorating_set.create(rate=rate, user_id=request.user.id)
            video.rate = (video.rate + rate) / 2
            video.save()
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

@login_required
def edit_time(request, video_id=0):
    video = Video.objects.get(pk=video_id, demo__user=request.user.id)
    start = addSec(video.time, -15)

    if request.method == "POST":
        timeForm = VideoTimeForm(request.POST, instance=video)
        if timeForm.is_valid():
            print "Is valid"
            t = timeForm.save(commit=False)
            t.duration = addSec(t.end, - getSec(t.start))
            t.save()
        return demo_view(request, video.demo_id)
    else:
        timeForm = VideoTimeForm({'start': video.start, 'end': video.end})

    images = [(str(addSec(start, i / 4)), "0" * (10 - len(str(i))) + str(i)) for i in range(140)]

    return direct_to_template(request, 'q3demotube/edit_time.html', {'images': images,
                                                            'demo_id': video.demo.id, 'timeForm': timeForm,
                                                            'videoTime': str(video.time), 'video': video})

@login_required
def add_time(request, demo_id=-1):
    d = Demo.objects.get(pk=demo_id, user=request.user.id)

    if request.method == "POST":
        videoForm = VideoForm(request.POST)
        if videoForm.is_valid():
            name, timeIn = videoForm.cleaned_data['name'], videoForm.cleaned_data['time']
            start, end = addSec(timeIn, -10), addSec(timeIn, 8)
            video = d.video_set.create(name=name, time=timeIn, start=start, end=end, duration=addSec(end, - getSec(start)))
            # Tags
            video.set_tags(videoForm.cleaned_data['tags'])
        return demo_view(request, demo_id)
    else:
        videoForm = VideoForm()
        return direct_to_template(request, 'q3demotube/add_time.html', {'demo_id': demo_id, 'videoForm': videoForm})

@login_required
def get_images(request, demo_id):
    demo = Demo.objects.get(pk=demo_id)
    if demo.video_set.filter(has_images=False).count():
        getMMEImages(demo_id)
    return demo_view(request, demo_id)

@login_required
def get_videos(request, demo_id):
    demo = Demo.objects.get(pk=demo_id)
    if demo.video_set.filter(has_video=False).count():
        getMMEVideos(demo_id)
    return demo_view(request, demo_id)

