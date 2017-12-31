# -*- coding: utf-8 -*- 


from Doodle import Doodle
from DoodleLang import DoodleLang
import sys
from moviepy.editor import *
import argparse
import UploadDoodle



output_video_directory='../output/videos/'
audio_background='../audios/Sleepy_Jake.mp3'
background_image='../background.gif'


mainDoodleDuration=20

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
        zoom = 0.4 + 0.02*(mainDoodleDuration-t) # Zoom-out.
    elif t >=10 and t<20 :
        zoom = 0.4 + 0.02*t  # Zoom-IN
    elif t >=20 and t<30 :
        zoom = 0.4 + 0.02*(mainDoodleDuration-t) # Zoom-out.
    elif t >=30 and t<=50 :
        zoom = 0.4 + 0.02*t  # Zoom-IN    
    #print "time is "+ str(t) + "zoom is" +str(zoom)  
    return  zoom 

def createDoodleVideo(doodleObject):
    
    reload(sys)  # Reload does the trick!
    sys.setdefaultencoding('UTF8')
    width=doodleObject.get_doodle_width()
    height=width*9/16
    #height=doodleObject.get_doodle_height()+100
    screensize = (width,height)
    wordWidth=width-40
    wordHeight=height/6
    input = raw_input("Shall I proceed ")
    print "creating video for "+doodleObject.get_doodle_title()
    
    contentCollection=[]
    contentCollection=createDoodleVideoContent(doodleObject,mainDoodleDuration)
    
    for dooldleLang in doodleObject.get_doodle_dooleLangs():
        if dooldleLang.get_doodle_hoverText() is not None and len(dooldleLang.get_doodle_hoverText()) > 1 and  dooldleLang.get_doodle_lang() == 'en':  
            textCollection=[]    
            print dooldleLang.get_doodle_hoverText()
            background_image_clip = VideoFileClip(background_image)
            for i in range(int(mainDoodleDuration/background_image_clip.duration)):
                textCollection.append(VideoFileClip(background_image).set_pos(('center',80)).set_start(i*background_image_clip.duration).resize(1.2))
            textCollection.append(VideoFileClip(background_image).set_pos(('center',80)).set_start(mainDoodleDuration-1).resize(1.2))    
            txt_word_header = TextClip("Google Doodle Celebrates",color='black',font='arial',method='label',size=(wordWidth,50))
            txt_word_header = txt_word_header.set_pos(('center',60)).set_duration(mainDoodleDuration)
            textCollection.append(txt_word_header)
            if doodleObject.get_doodle_image_jpeg()[-3:] =='gif':
                doodle_clip = VideoFileClip(doodleObject.get_doodle_image_jpeg())
            else:
                doodle_clip = ImageClip(doodleObject.get_doodle_image_jpeg())
            doodle_clip = doodle_clip.resize(resize_func).set_pos(('center',114)).set_duration(mainDoodleDuration)
            textCollection.append(doodle_clip)
            txt_word = TextClip(dooldleLang.get_doodle_hoverText(),color='black',font='Arial-Unicode-MS',method='label',size=(wordWidth,wordHeight),print_cmd=True)
            txt_word = txt_word.set_pos(('center',height-110)).set_duration(mainDoodleDuration)
            textCollection.append(txt_word)
            if len(contentCollection) >0 :
                textCollection.extend(contentCollection)
            totalvideoDuration= contentCollection[-1].end
            video = CompositeVideoClip(textCollection,size=screensize,bg_color=(255,255,255))
            absoluteVideoFile=output_video_directory+doodleObject.get_doodle_name()[:20]+"_"+dooldleLang.get_doodle_lang()+".mp4"
            dooldleLang.set_doodle_videoLocation(absoluteVideoFile)
            audio_backgroundClip=AudioFileClip(audio_background)
            video=video.set_audio(audio_backgroundClip.set_duration(totalvideoDuration))
            video.write_videofile(absoluteVideoFile,fps=24)
            videoDetails=populateVideoParameters(dooldleLang,doodleObject)
            #UploadDoodle.uploadToYoutube(videoDetails,dooldleLang,doodleObject)

    
    
def createDoodleVideoContent(doodleObject,mainDoodleDuration):
    statements=['Kuppali Venkatappa Puttappa (29 December 1904 – 11 November 1994),[2] popularly known by his pen name Kuvempu, was an Indian novelist, poet, playwright, critic and thinker']
    statements.append('He is widely regarded as the greatest Kannada poet of the 20th century. He is the first among Kannada writers to be decorated with the prestigious Jnanpith Award.')
    statements.append('Kuvempu studied at Mysore University in the 1920s, taught there for nearly three decades and served as its vice-chancellor from 1956 to 1960.')
    width=doodleObject.get_doodle_width()
    each_text_duration=6
    contentDuration=len(statements)*each_text_duration
    textCollection=[]  
    background_image_clip = VideoFileClip(background_image)
    for i in range(int(contentDuration/background_image_clip.duration)):
        textCollection.append(VideoFileClip(background_image).set_pos(('center',80)).set_start(mainDoodleDuration+(i*background_image_clip.duration)).resize(1.2))
    textCollection.append(VideoFileClip(background_image).set_pos(('center',80)).set_start(mainDoodleDuration+contentDuration-1).set_end(mainDoodleDuration+contentDuration).resize(1.2))
    start=mainDoodleDuration
    end=mainDoodleDuration+each_text_duration
    for statement in statements:
            txt_usage_word = TextClip("<span size='40000' font='Calibri-Bold' foreground='black' >"+statement+"</span>",method='pango',size=(width-80,400))
            txt_usage_word = txt_usage_word.set_pos(('center','center')).set_start(start).set_end(end)
            start=start+each_text_duration
            end=end+each_text_duration          
            textCollection.append(txt_usage_word)
    return textCollection  
    #video = CompositeVideoClip(textCollection,size=screensize,bg_color=(255,255,255))
    #video.write_videofile("hello.mp4",fps=24)             