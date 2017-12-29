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


def resize_func(t):
    if t < 4:
        return 1 + 0.08*t  # Zoom-in.
    elif 4 <= t <= 6:
        return 1 + 0.08*4  # Stay.
    else: # 6 < t
        return 1 + 0.08*(10-t)  # Zoom-out.
    

def createDoodleVideo(doodleObject):
    reload(sys)  # Reload does the trick!
    sys.setdefaultencoding('UTF8')
    print "creating video for "+doodleObject.get_doodle_title()
    for dooldleLang in doodleObject.get_doodle_dooleLangs():
        if dooldleLang.get_doodle_hoverText() is not None and dooldleLang.get_doodle_lang() == 'en':  
            textCollection=[]    
            print dooldleLang.get_doodle_hoverText()
            txt_word_header = TextClip("Google Doodle ",color='white',font='arial',method='label',size=(wordWidth,50))
            txt_word_header = txt_word_header.set_pos(('center',62)).set_duration(10)
            textCollection.append(txt_word_header)
            background_clip = ImageClip(doodleObject.get_doodle_image_jpeg())
            background_clip = background_clip.resize(resize_func).set_pos(('center',114)).set_duration(10)
            textCollection.append(background_clip)
            txt_word = TextClip(dooldleLang.get_doodle_hoverText(),color='white',font='Arial-Unicode-MS',method='caption',size=(wordWidth,wordHeight),print_cmd=True)
            txt_word = txt_word.set_pos(('center',570)).set_duration(10)
            textCollection.append(txt_word)
            video = CompositeVideoClip(textCollection,size=screensize)
            absoluteVideoFile=output_video_directory+doodleObject.get_doodle_name()[:20]+"_"+dooldleLang.get_doodle_lang()+".mp4"
            video.write_videofile(absoluteVideoFile,fps=24,codec="mpeg4") 

    
    
    
    
