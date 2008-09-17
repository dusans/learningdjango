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
    wavFile = "%s.wav" % video.id
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