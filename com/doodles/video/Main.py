import DoodleExtractor
import VideoDoodle

if __name__ == '__main__':
    doodleObject = DoodleExtractor.getDoodleFromGoogle()
    VideoDoodle.createDoodleVideo(doodleObject)
    #VideoDoodle.createDoodleVideoContent(doodleObject)
    #print doodleObject.get_doodle_title()
    #print doodleObject.get_doodle_name()
    #print doodleObject.get_doodle_query()
    #print doodleObject.get_doodle_image_png()
    #print doodleObject.get_doodle_image_jpeg()
    #for dooldleLang in doodleObject.get_doodle_dooleLangs():
         #print dooldleLang.get_doodle_lang()
         #print dooldleLang.get_doodle_query()
         #print dooldleLang.get_doodle_hoverText()

        