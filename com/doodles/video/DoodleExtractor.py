from Doodle import Doodle
from DoodleLang import DoodleLang
import sys
import requests

reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8') 

output_image_directory='../output/images/'

def removeSpecialCharacters(string):
        return ''.join(e for e in string if e.isalnum())
    
def populateDoodleHeaders(dooldleObject, doodleJson):
    dooldleObject.set_doodle_title(doodleJson['title'])
    dooldleObject.set_doodle_name(doodleJson['name'])
    dooldleObject.set_doodle_query(doodleJson['query'])
    dooldleObject.set_doodle_width(doodleJson['hires_width'])
    dooldleObject.set_doodle_height(doodleJson['hires_height'])
    absoluteJpegPath=output_image_directory+doodleJson['name']+doodleJson['hires_url'][-4:]
    absolutePngPath=output_image_directory+doodleJson['name']+doodleJson['url'][-4:]
    print "https://"+doodleJson['hires_url'][2:]
    requestJpeg = requests.get("https://"+doodleJson['hires_url'][2:])
    if requestJpeg.status_code == 200:
        with open(absoluteJpegPath, 'wb') as f:
            for chunk in requestJpeg:
                f.write(chunk)
    dooldleObject.set_doodle_image_jpeg(absoluteJpegPath)


def populateDoodleLangs(dooleLangObjects, doodleJson):
    translations = doodleJson['translations']                            
    for lang in translations:
            doodleLang = DoodleLang()
            doodleLang.set_doodle_lang(lang)
            doodleLang.set_doodle_query(translations[lang]['query'])
            doodleLang.set_doodle_hoverText(translations[lang]['hover_text'])
            dooleLangObjects.append(doodleLang)

def getDoodleFromGoogle():
    dooldleObject=Doodle()
    dooleLangObjects=[]
    URL='https://www.google.com/doodles/json/2017/12'
    PARAMS = {'hl':'en_GB'}
    request = requests.get(url = URL, params = PARAMS)
    data = request.json()
    doodleJson=data[9]
    populateDoodleHeaders(dooldleObject, doodleJson)
    populateDoodleLangs(dooleLangObjects, doodleJson)
    dooldleObject.set_doodle_dooleLangs(dooleLangObjects)
    return dooldleObject