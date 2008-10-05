import shutil
import os
from q3demotube.models import Demo, Video
from datetime import time, timedelta
from django.conf import settings
from django.core.files import File
from PIL import Image
import time as timer

def getSec(t):
    return timedelta(hours=t.hour, minutes=t.minute, seconds=t.second).seconds

def addSec(t, n):
    sec = max(1, getSec(t) + n)
    return time(sec / 3600, sec / 60, sec % 60)

q3mmeDir = "c:/Igre/q3/mme"
q3Dir = "c:/Igre/q3"
ffmpegDir = "C:/Program Files/megui/tools/ffmpeg"
mp4BoxDir = "C:/Program Files/megui/tools/mp4box"

def setMME(demo_id, videos, quality, wav, fps, capType="images"):
    #==== ==== ==== ====
    # COPY DEMO
    #==== ==== ==== ====
    demo = Demo.objects.get(pk=demo_id)
    ext = demo.demo.name.split(".")[-1]
    shutil.copy2(demo.demo.path, "%s/demos/%s-%s.%s" % (q3mmeDir, demo_id, capType, ext))
    #==== ==== ==== ====
    # CREATE PROJECT
    #==== ==== ==== ====
    os.chdir("%s/project" % (q3mmeDir))
    project = open("%s/project.cfg" % (q3mmeDir)).read()

    try:
        os.mkdir("%s-%s" % (demo_id, capType))
    except:
        print "Dir already existes"

    for video in videos:
        if capType == "images":
            start = max(1, getSec(addSec(video.time, -15))) * 1000
            end = getSec(addSec(video.time, 20)) * 1000
            format = "jpg"
        else:
            start = max(1,getSec(video.start)) * 1000
            end = getSec(video.end) * 1000
            format = "tga"

        projectXML = project % (start, end, fps, format, quality, wav)
        open("%s/project/%s-%s/%s.cfg" % (q3mmeDir, demo_id, capType, video.id), "w").write(projectXML)

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
    setMME(demo_id, videos, quality=40, wav=0, fps=4, capType=capType)

    #==== ==== ==== ====
    # RUN CAPTURE
    #==== ==== ==== ====
    os.chdir("%s" % (q3Dir))
    run = '''quake3mme.exe +set fs_game "mme" +set r_ignorehwgamma "2" +hidden +set mme_renderWidth "440" +set mme_renderHeight "220" +set r_multisample "0" +set r_multisampleNvidia "0" +set r_anisotropy "0" +exec "low.cfg" +set r_picmip "16" +demolist "%s-demolist.txt"''' % (demo_id)
    print run
    os.system('%s &' % run)

    #==== ==== ==== ====
    # COPY + DELETE
    #==== ==== ==== ====
    capture = os.listdir('%s/mme/capture/%s-%s' % (q3Dir, demo_id, capType))

    os.chdir("%sq3/images" % (settings.MEDIA_ROOT))

    try:
        os.mkdir("%s-%s" % (demo_id, capType))
    except:
        print "Dir already existes"

    for video in videos:
        for image in capture:
            if image.startswith('%s.' % video.id):
                shutil.copy2("%s/capture/%s-%s/%s" % (q3mmeDir, demo_id, capType, image), "%sq3/images/%s-images/%s" % (settings.MEDIA_ROOT, demo_id, image))
                video.images_set.create(image=File(open("%sq3/images/%s-images/%s" % (settings.MEDIA_ROOT, demo_id, image))))

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
    setMME(demo_id, videos, quality=100, wav=1, fps=30, capType=capType)

    #==== ==== ==== ====
    # RUN CAPTURE
    #==== ==== ==== ====
    t_start = timer.time()
    os.chdir("%s" % (q3Dir))
    run = '''quake3mme.exe +set fs_game "mme" +set r_ignorehwgamma "2" +hidden +set mme_renderWidth "540" +set mme_renderHeight "260" +set r_multisample "0" +set r_multisampleNvidia "0" +set r_anisotropy "0" +exec "low.cfg" +set r_picmip "16" +demolist "%s-demolist.txt"''' % (demo_id)
    print run
    os.system('%s &' % run)
    t_end = timer.time()

    capture = os.listdir('%s/mme/capture/%s-%s' % (q3Dir, demo_id, capType))

    for video in videos:
        #==== ==== ==== ====
        # GET MEDIA
        #==== ==== ==== ====
        capturedImages = [i for i in capture if i.startswith("%s." %video.id) and i.endswith(".tga")]
        firstImage = "%s/capture/%s-%s/%s.%s.tga" % (q3mmeDir, demo.id, capType, video.id, "%010d")
        wavFile = "%s/capture/%s-%s/%s.wav" % (q3mmeDir, demo.id, capType, video.id)
        outFile = "%sq3/videos/%s.mp4" % (settings.MEDIA_ROOT, video.id)

        #==== ==== ==== ====
        # RUN FFMPEG + MP4BOX
        #==== ==== ==== ====
        c_start = timer.time()
        os.chdir("%s" % (ffmpegDir))
        run = '''ffmpeg.exe -y -r 30 -i "%s" -i "%s" -r 30 -acodec libfaac -ab 128k -vcodec libx264 -s 540x260 -b 300k  -flags +loop -cmp +chroma -flags2 +mixed_refs -me umh -subq 5 -trellis 1 -refs 3 -bf 3 -b_strategy 1 -coder 1 -me_range 16 -g 250 -keyint_min 25 -sc_threshold 40 -i_qfactor 0.71 -bt 284k "%s"''' % (firstImage, wavFile, outFile)
        print run
        os.system('%s &' % run)

        os.chdir("%s" % (mp4BoxDir))
        run = 'MP4Box.exe  -tmp c:/ -inter 300 "%s"' % (outFile)
        print run
        os.system('%s &' % run)
        c_end = timer.time()
        #==== ==== ==== ====
        # THUMBNAIL
        #==== ==== ==== ====
        image = capturedImages[len(capturedImages) / 2]
        Image.open("%s/capture/%s-%s/%s" % (q3mmeDir, demo_id, capType, image)).save("%sq3/thumbnails/%s.tga" % (settings.MEDIA_ROOT, video.id), "JPEG")
        #shutil.copy2("%s/capture/%s-%s/%s" % (q3mmeDir, demo_id, capType, image), "%sq3/thumbnails/%s.tga" % (settings.MEDIA_ROOT, video.id))
        video.thumbnail = "q3/thumbnails/%s.tga" % (video.id)

        #==== ==== ==== ====
        # SAVE
        #==== ==== ==== ====
        video.videoFile = "q3/videos/%s.mp4" % (video.id)
        video.has_video = True
        video.capture_time, video.compression_time = (t_end - t_start), (c_end - c_start)
        video.save()

    #==== ==== ==== ====
    # REMOVE
    #==== ==== ==== ====
    for f in capture:
        if f.endswith(".tga") or f.endswith(".wav"):
            os.remove("%s/capture/%s-%s/%s" % (q3mmeDir, demo_id, capType, f))
