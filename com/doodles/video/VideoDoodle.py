# -*- coding: utf-8 -*- 


from Doodle import Doodle
from DoodleLang import DoodleLang
import sys
from moviepy.editor import *

width=1400
height=width*9/16
screensize = (width,height)
wordWidth=width-40
wordHeight=height/5

output_video_directory='../output/videos/'
audio_background='../audios/backgroundAudio.mp3'
background_image='../background.jpg'

duration=20

def resize_func(t):
    zoom=0
    if t < 10:
        zoom = 0.8 + 0.02*(duration-t) # Zoom-out.
    elif t >=10 and t<20 :
        zoom = 0.8 + 0.02*t  # Zoom-IN
    elif t >=20 and t<30 :
        zoom = 0.8 + 0.02*(duration-t) # Zoom-out.
    elif t >=30 and t<=50 :
        zoom = 0.8 + 0.02*t  # Zoom-IN    
    #print "time is "+ str(t) + "zoom is" +str(zoom)  
    return  zoom 

def createDoodleVideo(doodleObject):
    reload(sys)  # Reload does the trick!
    sys.setdefaultencoding('UTF8')
    print "creating video for "+doodleObject.get_doodle_title()
    for dooldleLang in doodleObject.get_doodle_dooleLangs():
        if dooldleLang.get_doodle_hoverText() is not None and dooldleLang.get_doodle_lang() == 'en':  
            textCollection=[]    
            print dooldleLang.get_doodle_hoverText()
            background_image_clip = ImageClip(background_image)
            background_image_clip = background_image_clip.set_duration(duration)
            textCollection.insert(0,background_image_clip)
            txt_word_header = TextClip("Google Doodle ",color='white',font='arial',method='label',size=(wordWidth,50))
            txt_word_header = txt_word_header.set_pos(('center',60)).set_duration(duration)
            textCollection.append(txt_word_header)
            doodle_clip = ImageClip(doodleObject.get_doodle_image_jpeg())
            doodle_clip = doodle_clip.resize(resize_func).set_pos(('center',114)).set_duration(duration)
            textCollection.append(doodle_clip)
            txt_word = TextClip(dooldleLang.get_doodle_hoverText(),color='white',font='Arial-Unicode-MS',method='label',size=(wordWidth,wordHeight),print_cmd=True)
            txt_word = txt_word.set_pos(('center',570)).set_duration(duration)
            textCollection.append(txt_word)
            video = CompositeVideoClip(textCollection,size=screensize)
            absoluteVideoFile=output_video_directory+doodleObject.get_doodle_name()[:20]+"_"+dooldleLang.get_doodle_lang()+".mp4"
            audio_backgroundClip=AudioFileClip(audio_background)
            video=video.set_audio(audio_backgroundClip.set_duration(duration))
            video.write_videofile(absoluteVideoFile,fps=24,codec="mpeg4") 

    
    
    
    
