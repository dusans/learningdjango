import shutil
import os
from q3demotube.models import *
from datetime import time, timedelta
from django.conf import settings

#c = Category(name='First Category')
#d = Demo.objects.all()


def getSec(t):
    return timedelta(hours=t.hour, minutes=t.minute, seconds=t.second).seconds

def addSec(t, n):
    sec = getSec(t) + n
    return time(sec / 3600, sec / 60, sec % 60)

q3mmeDir = "c:/Igre/q3/mme"
q3Dir = "c:/Igre/q3"
virtualDubDir = "c:/Program Files/VirtualDub"
#demo_id = 1

def setMME(demo_id, demo, videos, quality, wav, fps, capType="images"):
    #==== ==== ==== ====
    # COPY DEMO
    #==== ==== ==== ====
    ext = demo.demo.path.split(".")[-1]
    shutil.copy2(demo.demo.path, "%s/demos/%s-%s.%s" % (q3mmeDir, demo_id, capType, ext))
    #==== ==== ==== ====
    # CREATE PROJECT
    #==== ==== ==== ====
    project = open("%s/project.cfg" % (q3mmeDir)).read()
    os.chdir("%s/project" % (q3mmeDir))

    try:
        os.mkdir("%s-%s" % (demo_id, capType))
    except:
        print "Dir already existes"

    for video in videos:
        if capType == "images":
            start = getSec(addSec(video.time, -20)) * 1000
            end = getSec(addSec(video.time, 25)) * 1000
        else:
            start = getSec(video.start) * 1000
            end = getSec(video.end) * 1000

        projectXML = project % (start, end, fps, quality, wav)
        o = open("%s/project/%s-%s/%s.cfg" % (q3mmeDir, demo_id, capType, video.id), "w")
        o.write(projectXML)
        o.close()

    #==== ==== ==== ====
    # DEMO LIST
    #==== ==== ==== ====
    o = open("%s/%s-demolist.txt" % (q3mmeDir, demo_id), "w")
    for video in videos:
        o.write('"/%s-%s" "%s"\n' % (demo_id, capType, video.id))
    o.close()

#==== ==== ==== ====
# GET IMAGES WITH MME
#==== ==== ==== ====
def getMMEImages(demo_id, capType="images"):
    #==== ==== ==== ====
    # START
    #==== ==== ==== ====
    demo = Demo.objects.get(pk=demo_id)
    videos = demo.video_set.filter(has_images=False)

    #==== ==== ==== ====
    # SET MME
    #==== ==== ==== ====
    setMME(demo_id, demo, videos, quality=25, wav=0, fps=4, capType=capType)

    #==== ==== ==== ====
    # RUN CAPTURE
    #==== ==== ==== ====
    os.chdir("%s" % (q3Dir))
    run = '''quake3mme.exe +set fs_game "mme" +set mme_renderWidth "640" +set mme_renderHeight "480" +set r_multisample "0" +set r_multisampleNvidia "0" +set r_anisotropy "0" +set fs_extraGames "osp" +set r_picmip "0" +set r_picmip "0" +exec "low.cfg" +demolist "%s-demolist.txt"''' % (demo_id)
    print run

    os.system('%s &' % run)

    #==== ==== ==== ====
    # COPY + DELETE
    #==== ==== ==== ====
    capture = os.listdir('%s/mme/capture/%s-%s' % (q3Dir, demo_id, capType))

    for video in videos:
        for image in capture:
            if image.startswith('%s.' % video.id):
                shutil.copy2("%s/capture/%s-%s/%s" % (q3mmeDir, demo_id, capType, image), "%sq3/images/%s" % (settings.MEDIA_ROOT, image))

        for image in capture:
            if image.startswith('%s.' % video.id):
                os.remove("%s/capture/%s-%s/%s" % (q3mmeDir, demo_id, capType, image))


    for video in videos:
        video.has_images = True
        video.save()

def getMMEVideos(demo_id, capType="videos"):
    #==== ==== ==== ====
    # START
    #==== ==== ==== ====
    demo = Demo.objects.get(pk=demo_id)
    videos = demo.video_set.filter(has_video=False)

    #==== ==== ==== ====
    # SET MME
    #==== ==== ==== ====
    setMME(demo_id, demo, videos, quality=100, wav=1, fps=30, capType=capType)

    #==== ==== ==== ====
    # RUN CAPTURE
    #==== ==== ==== ====
    os.chdir("%s" % (q3Dir))
    run = '''quake3mme.exe +set fs_game "mme" +set mme_renderWidth "640" +set mme_renderHeight "480" +set r_multisample "0" +set r_multisampleNvidia "0" +set r_anisotropy "0" +set fs_extraGames "osp" +set r_picmip "0" +set r_picmip "0" +exec "low.cfg" +demolist "%s-demolist.txt"''' % (demo_id)
    print run
    os.system('%s &' % run)

    capture = os.listdir('%s/mme/capture/%s-%s' % (q3Dir, demo_id, capType))
    #==== ==== ==== ====
    # CREATE VIDEO - VIRTUAL DUB
    #==== ==== ==== ====
    os.chdir("%s" % (virtualDubDir))
    script = open("defaultVDFlv.txt").read()

    for video in videos:
        #==== ==== ==== ====
        # CREATE DUB SCRIPT
        #==== ==== ==== ====
        firstImage = [i for i in capture if i.startswith("%s." %video.id) and i.endswith(".jpg")][0]
        wavFile = [i for i in capture if i == "%s.wav" % video.id][0]
        outFile = "%sq3/videos/%s.flv" % (settings.MEDIA_ROOT, video.id)
        scriptOut = script % (  "%s/capture/%s-%s/%s" % (q3mmeDir, demo.id, capType, firstImage) ,
                                "%s/capture/%s-%s/%s" % (q3mmeDir, demo.id, capType, wavFile),
                                outFile)

        open("VirtualDubMod.jobs", "w").write(scriptOut)
        #==== ==== ==== ====
        # RUN DUB SCRIPT
        #==== ==== ==== ====
        run = "vdub.exe /s VirtualDubMod.jobs"
        print run
        #os.system('%s &' % run)

        video.has_video = True
        #video.save()

    #==== ==== ==== ====
    # REMOVE
    #==== ==== ==== ====
    for f in capture:
        if f.endswith(".jpg") or f.endswith(".wav"):
            pass #  os.remove("%s/capture/%s-%s/%s" % (q3mmeDir, demo_id, capType, f))
