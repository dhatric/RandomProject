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
    
    absoluteJpegPath=output_image_directory+doodleJson['name']+".jpeg"
    absolutePngPath=output_image_directory+doodleJson['name']+".png"
    
    requestJpeg = requests.get("https://"+doodleJson['hires_url'][2:])
    if requestJpeg.status_code == 200:
        with open(absoluteJpegPath, 'wb') as f:
            for chunk in requestJpeg:
                f.write(chunk)
    dooldleObject.set_doodle_image_jpeg(absoluteJpegPath)
    
    requestPng = requests.get("https://"+doodleJson['url'][2:])
    if requestPng.status_code == 200:
        with open(absolutePngPath, 'wb') as f:
            for chunk in requestPng:
                f.write(chunk)

    dooldleObject.set_doodle_image_png(absolutePngPath)


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
    doodleJson=data[0]
    populateDoodleHeaders(dooldleObject, doodleJson)
    populateDoodleLangs(dooleLangObjects, doodleJson)
    dooldleObject.set_doodle_dooleLangs(dooleLangObjects)
    return dooldleObject