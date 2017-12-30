# -*- coding: utf-8 -*- 


from Doodle import Doodle
from DoodleLang import DoodleLang
import sys
from moviepy.editor import *
import argparse
import UploadDoodle



output_video_directory='../output/videos/'
audio_background='../audios/Sleepy_Jake.mp3'
background_image='../background.jpg'

duration=20

def populateVideoParameters(dooldleLang,doodleObject):
    videoDetails = argparse.Namespace()
    videoDetails.file=dooldleLang.get_doodle_videoLocation()
    videoDetails.title=dooldleLang.get_doodle_query()+ " Google Doodle"
    videoDetails.description="Google Doodle :\n"+ dooldleLang.get_doodle_hoverText()+"\n" +dooldleLang.get_doodle_query() +"\n" +doodleObject.get_doodle_title()+"\n" +doodleObject.get_doodle_name()
    videoDetails.category="27"
    keywords=[doodleObject.get_doodle_title(),doodleObject.get_doodle_name(),dooldleLang.get_doodle_query(),dooldleLang.get_doodle_hoverText()]
    videoDetails.keywords=",".join(keywords)
    videoDetails.privacyStatus="public"
    videoDetails.logging_level="WARNING"
    videoDetails.noauth_local_webserver=True
    videoDetails.still_id=1
    return videoDetails


def resize_func(t):
    zoom=0
    if t < 10:
        zoom = 0.4 + 0.02*(duration-t) # Zoom-out.
    elif t >=10 and t<20 :
        zoom = 0.4 + 0.02*t  # Zoom-IN
    elif t >=20 and t<30 :
        zoom = 0.4 + 0.02*(duration-t) # Zoom-out.
    elif t >=30 and t<=50 :
        zoom = 0.4 + 0.02*t  # Zoom-IN    
    #print "time is "+ str(t) + "zoom is" +str(zoom)  
    return  zoom 

def createDoodleVideo(doodleObject):
    reload(sys)  # Reload does the trick!
    sys.setdefaultencoding('UTF8')
    width=doodleObject.get_doodle_width()
    height=width*9/16
    screensize = (width,height)
    wordWidth=width-40
    wordHeight=height/6
    input = raw_input("Shall I proceed ")
    print "creating video for "+doodleObject.get_doodle_title()
    for dooldleLang in doodleObject.get_doodle_dooleLangs():
        if dooldleLang.get_doodle_hoverText() is not None and len(dooldleLang.get_doodle_hoverText()) > 1 and  dooldleLang.get_doodle_lang() == 'en':  
            textCollection=[]    
            print dooldleLang.get_doodle_hoverText()
            txt_word_header = TextClip("Google Doodle Celebrates",color='black',font='arial',method='label',size=(wordWidth,50))
            txt_word_header = txt_word_header.set_pos(('center',60)).set_duration(duration)
            textCollection.append(txt_word_header)
            if doodleObject.get_doodle_image_jpeg()[-3:] =='gif':
                doodle_clip = VideoFileClip(doodleObject.get_doodle_image_jpeg())
            else:
                doodle_clip = ImageClip(doodleObject.get_doodle_image_jpeg())
            doodle_clip = doodle_clip.resize(resize_func).set_pos(('center',114)).set_duration(duration)
            textCollection.append(doodle_clip)
            txt_word = TextClip(dooldleLang.get_doodle_hoverText(),color='black',font='Arial-Unicode-MS',method='label',size=(wordWidth,wordHeight),print_cmd=True)
            txt_word = txt_word.set_pos(('center',height-100)).set_duration(duration)
            textCollection.append(txt_word)
            video = CompositeVideoClip(textCollection,size=screensize,bg_color=(255,255,255))
            absoluteVideoFile=output_video_directory+doodleObject.get_doodle_name()[:20]+"_"+dooldleLang.get_doodle_lang()+".mp4"
            dooldleLang.set_doodle_videoLocation(absoluteVideoFile)
            audio_backgroundClip=AudioFileClip(audio_background)
            video=video.set_audio(audio_backgroundClip.set_duration(duration))
            video.write_videofile(absoluteVideoFile,fps=24)
            videoDetails=populateVideoParameters(dooldleLang,doodleObject)
            #UploadDoodle.uploadToYoutube(videoDetails,dooldleLang,doodleObject)

    
    
    
    
