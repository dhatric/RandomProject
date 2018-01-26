import DoodleExtractor
import VideoDoodle


def autoPlayDoodle():
    doodleObject = DoodleExtractor.getDoodleFromGoogle()
    if len(doodleObject.get_doodle_contents()) > 0 :
        VideoDoodle.createDoodleVideo(doodleObject)
    file_write = open("LastSuccess.txt", "w") 
    file_write.write(doodleObject.get_doodle_name())
    file_write.close()
    
if __name__ == '__main__':
    autoPlayDoodle()

