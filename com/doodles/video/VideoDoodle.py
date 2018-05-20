# -*- coding: utf-8 -*- 


from Doodle import Doodle
from DoodleLang import DoodleLang
import sys
from moviepy.editor import *
import argparse
import UploadDoodle
import urllib2
from bs4 import BeautifulSoup
import re
import DoodleLikesComments

output_video_directory='../output/videos/'
audio_background='../audios/Sleepy_Jake.mp3'
background_image='../background.gif'
output_thumbnails_directory='../output/thumbnails/'
#doodle main duration without  content
mainDoodleDuration=20




def populateVideoParameters(dooldleLang,doodleObject):
    videoDetails = argparse.Namespace()
    videoDetails.file=dooldleLang.get_doodle_videoLocation()
    videoDetails.title=dooldleLang.get_doodle_query()+ " | "+dooldleLang.get_doodle_hoverText()
    videoDetails.description="Google Doodle :\n"+ dooldleLang.get_doodle_hoverText()+"\n" +dooldleLang.get_doodle_query() +"\n" +doodleObject.get_doodle_title()+"\n" +doodleObject.get_doodle_name()+"\n" +dooldleLang.get_doodle_query()+"\n"+ dooldleLang.get_doodle_hoverText()+"\n\n" +".\n".join(doodleObject.get_doodle_contents())+"\n www.dictionguru.com"
    videoDetails.category="22"
    keywords=[doodleObject.get_doodle_title(),doodleObject.get_doodle_name(),dooldleLang.get_doodle_query(),dooldleLang.get_doodle_hoverText(),doodleObject.get_doodle_query()]
    videoDetails.keywords=",".join(keywords)
    videoDetails.privacyStatus="public"
    videoDetails.logging_level="WARNING"
    videoDetails.noauth_local_webserver=True
    videoDetails.still_id=1
    return videoDetails

def resize_func(t):
    global mainDoodleDuration
    zoom=0
    if mainDoodleDuration == 20:
        if t < 10:
            zoom = 0.4 + 0.02*(mainDoodleDuration-t) # Zoom-out.
        elif t >=10 and t<=20 :
            zoom = 0.4 + 0.02*t  # Zoom-IN
    if mainDoodleDuration == 10:  
        if t < 5:
            zoom = 0.4 + 0.04*(mainDoodleDuration-t) # Zoom-out.
        elif t >= 5 and t < 10 :
            zoom = 0.4 + 0.04*t  # Zoom-IN
    return  zoom 


def createDoodleVideo(doodleObject):
    global mainDoodleDuration
    reload(sys)  # Reload does the trick!
    sys.setdefaultencoding('UTF8')
    width=doodleObject.get_doodle_width()
    height=width*9/16
    #height=doodleObject.get_doodle_height()+100
    screensize = (width,height)
    wordWidth=width-40
    wordHeight=height/6
    #input = raw_input("Shall I proceed ")
    print "creating video for "+doodleObject.get_doodle_title()

    #contentCollection=[]
    statements=doodleObject.get_doodle_contents()
    # If doodle content is present reduce main image to 10
    if len(statements) > 0:
        mainDoodleDuration = 10
    contentCollection=createDoodleVideoContent(doodleObject,mainDoodleDuration,statements)
  
    for dooldleLang in doodleObject.get_doodle_dooleLangs():
        if dooldleLang.get_doodle_hoverText() is not None and len(dooldleLang.get_doodle_hoverText()) > 1  and (dooldleLang.get_doodle_lang() == 'en'  or  dooldleLang.get_doodle_query() != doodleObject.get_doodle_eng_query()) :  
            textCollection=[]    
            print dooldleLang.get_doodle_lang()+ " " +dooldleLang.get_doodle_hoverText()
            background_image_clip = VideoFileClip(background_image)
            for i in range(int(mainDoodleDuration/background_image_clip.duration)):
                textCollection.append(VideoFileClip(background_image).set_pos(('center',10)).set_start(i*background_image_clip.duration).set_duration(background_image_clip.duration).resize(1))
            textCollection.append(VideoFileClip(background_image).set_pos(('center',10)).set_start(mainDoodleDuration-1).resize(1))    
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
            totalvideoDuration=mainDoodleDuration
            if len(contentCollection) >0 :
                textCollection.extend(contentCollection)
                totalvideoDuration= contentCollection[-1].end
            video = CompositeVideoClip(textCollection,size=screensize,bg_color=(255,255,255))
            absoluteVideoFile=output_video_directory+doodleObject.get_doodle_name()[:20]+"_"+dooldleLang.get_doodle_lang()+".mp4"
            dooldleLang.set_doodle_videoLocation(absoluteVideoFile)
            audio_backgroundClip=AudioFileClip(audio_background)
            video=video.set_audio(audio_backgroundClip.set_duration(totalvideoDuration))
            video.save_frame(output_thumbnails_directory+doodleObject.get_doodle_name()[:20]+"_"+dooldleLang.get_doodle_lang()+".jpeg", 2, False)
            video.write_videofile(absoluteVideoFile,fps=24)
            videoDetails=populateVideoParameters(dooldleLang,doodleObject)
            UploadDoodle.uploadToYoutube(videoDetails,dooldleLang,doodleObject)
            print doodleObject.get_doodle_videoID()
            DoodleLikesComments.generateLikesComments(dooldleLang, doodleObject)
            file_write = open("LastSuccess.txt", "w")
            file_write.write(doodleObject.get_doodle_name())
            file_write.close()


def createDoodleVideoContent(doodleObject,mainDoodleDuration,statements):
    textCollection=[] 
    #statements=getContentForDoodle(doodleObject)
    if len(statements) > 0:
        width=doodleObject.get_doodle_width()
        each_text_duration=6
        contentDuration=len(statements)*each_text_duration
        background_image_clip = VideoFileClip(background_image)
        for i in range(int(contentDuration/background_image_clip.duration)):
            start_time=mainDoodleDuration+(i*background_image_clip.duration)
            textCollection.append(VideoFileClip(background_image).set_pos(('center',10)).set_start(start_time).set_duration(background_image_clip.duration).resize(1))
        textCollection.append(VideoFileClip(background_image).set_pos(('center',10)).set_start(mainDoodleDuration+contentDuration-2).set_end(mainDoodleDuration+contentDuration).resize(1))
        txt_title_word = TextClip("<span size='35000' font='Calibri-Bold' foreground='black' >"+re.sub('[<>&;-]+',' ',doodleObject.get_doodle_title())+"</span>",method='pango',size=(width-80,400))
        txt_title_word = txt_title_word.set_pos(('center',40)).set_start(mainDoodleDuration).set_end(mainDoodleDuration+contentDuration) 
        textCollection.append(txt_title_word)
        start=mainDoodleDuration
        end=mainDoodleDuration+each_text_duration
        for statement in statements:
                print statement+"\n\n\n\n"
                txt_usage_word = TextClip("<span size='30000' font='Calibri-Bold' foreground='black' >"+re.sub('[<>&;-]+',' ',statement)+".</span>",method='pango',size=(width-80,400))
                txt_usage_word = txt_usage_word.set_pos(('center','center')).set_start(start).set_end(end)
                start=start+each_text_duration
                end=end+each_text_duration          
                textCollection.append(txt_usage_word)
    return textCollection  
    #video = CompositeVideoClip(textCollection,size=screensize,bg_color=(255,255,255))
    #video.write_videofile("hello.mp4",fps=24)             