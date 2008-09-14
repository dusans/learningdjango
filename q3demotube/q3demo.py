import shutil
import os
from q3demotube.models import *
from datetime import time, timedelta

#c = Category(name='First Category')
#d = Demo.objects.all()

demo_id = 8

q3mmeDir = "c:/Igre/q3/mme"
q3Dir = "c:/Igre/q3"
#==== ==== ==== ====
# COPY
#==== ==== ==== ====
demo = Demo.objects.get(pk=demo_id)
ext = demo.demo.path.split(".")[-1]
#start = str(i.start).replace(":", ".")

shutil.copy2(demo.demo.path, "%s/demos/%s-demo.%s" % (q3mmeDir, demo_id, ext))
#==== ==== ==== ====
# PROJECT
#==== ==== ==== ====
project = open("project.cfg").read()
os.chdir("%s/project" % (q3mmeDir))
try:
    os.mkdir("%s-demo" % demo_id)
except:
    print "Dir already existes"

for i in demo.video_set.all():
    start = timedelta(minutes=i.start.minute, seconds=i.start.second).seconds * 1000
    end = (timedelta(minutes=i.end.minute, seconds=i.end.second).seconds + 15) * 1000

    projectXML = project % (start , end, 4)
    o = open("%s/project/%s-demo/%s.cfg" % (q3mmeDir, demo_id, i.id), "w")
    o.write(projectXML)
    o.close()

#==== ==== ==== ====
# DEMO LIST
#==== ==== ==== ====
#"/DUEL/44-xgo-3.55_3xRG_9.10_NICE_MIDAIR-vs-d0Be-cpm3a" "cpm3a3xRG"
o = open("%s/%s-demolist.txt" % (q3mmeDir, demo_id), "w")
for v in demo.video_set.all():
    o.write('"/%s-demo" "%s"\n' % (demo_id, v.id))
o.close()

#==== ==== ==== ====
# RUN CAPTURE
#==== ==== ==== ====
os.chdir("%s" % (q3Dir))
#run = '''ffmpeg -i "%s" -f mp4 -vcodec mpeg4 -b %s  -r %s -s %s -acodec libfaac -threads 2 -ar 24000 -ab 192000 -ac 2 "%s"''' % (movie, bitrate, fps, r, movieName)
run = '''quake3mme.exe +set fs_game "mme" +set mme_renderWidth "640" +set mme_renderHeight "480"
        +set r_multisample "0" +set r_multisampleNvidia "0" +set r_anisotropy "0"
        +set fs_extraGames "osp" +set r_picmip "0" +set r_picmip "0" +exec "low.cfg"
        +demolist "%s-demolist.txt"''' % (demo_id)

print run
#os.system('%s &' % run)


