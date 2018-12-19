from Doodle import Doodle
from DoodleLang import DoodleLang
import sys
import requests
import urllib2
from bs4 import BeautifulSoup

reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8') 

output_image_directory='../output/images/'

def removeSpecialCharacters(string):
        return ''.join(e for e in string if e.isalnum())
    
def populateDoodleHeaders(dooldleObject, doodleJson):
    dooldleObject.set_doodle_title(doodleJson['title'])
    dooldleObject.set_doodle_name(doodleJson['name'])
    dooldleObject.set_doodle_query(doodleJson['query'])
    dooldleObject.set_doodle_width(doodleJson['high_res_width'])
    dooldleObject.set_doodle_height(doodleJson['high_res_height'])
    absoluteJpegPath=output_image_directory+doodleJson['name']+doodleJson['high_res_url'][-4:]
    absolutePngPath=output_image_directory+doodleJson['name']+doodleJson['url'][-4:]
    print "https://"+doodleJson['high_res_url'][2:]
    requestJpeg = requests.get("https://"+doodleJson['high_res_url'][2:])
    if requestJpeg.status_code == 200:
        with open(absoluteJpegPath, 'wb') as f:
            for chunk in requestJpeg:
                f.write(chunk)
    dooldleObject.set_doodle_image_jpeg(absoluteJpegPath)


def populateDoodleLangs(dooldleObject,dooleLangObjects, doodleJson):
    translations = doodleJson['translations']                            
    for lang in translations:
            doodleLang = DoodleLang()
            doodleLang.set_doodle_lang(lang)
            doodleLang.set_doodle_query(translations[lang]['query'])
            doodleLang.set_doodle_hoverText(translations[lang]['hover_text'])
            if lang =='en':
                dooldleObject.set_doodle_eng_query(translations[lang]['query'])
            dooleLangObjects.append(doodleLang)

def getContentForDoodle(doodleObject):
    content_array=[]
    final_content_array=[]
    url='https://www.google.com/doodles/'+doodleObject.get_doodle_name()
    print url
    #response = urllib2.urlopen(url)
    soup = BeautifulSoup(urllib2.urlopen(url), 'html.parser')
    if soup is not None:
         near_soup_tag= soup.find('li',attrs={'id':'blog-card','class':'doodle-card'})
         near_soap_span=BeautifulSoup(""+str(near_soup_tag),'html.parser')
         if near_soap_span is not None:
             span_array=near_soap_span.find_all('p')
             print span_array
             if len(span_array) > 0:
                 string_aray =[]
                 #Appending to plain text and back to list to avoid issues from portal
                 for span in span_array:
                     string_aray.append(span.text)
                 string_plainText= "".join(string_aray)
                 content_array=string_plainText.split(".")
                 for content in content_array:
                     if len(content) > 10 and len(content) < 250:
                         final_content_array.append(content)
                 if len(final_content_array) > 1:        
                     final_content_array.append("Like, Share and Subscribe to Diction Guru")  
    #print final_content_array
    doodleObject.set_doodle_contents(final_content_array)

def getDoodleFromGoogle(doodleJson):
    dooldleObject=Doodle()
    dooleLangObjects=[]
    populateDoodleHeaders(dooldleObject, doodleJson)
    populateDoodleLangs(dooldleObject,dooleLangObjects, doodleJson)
    dooldleObject.set_doodle_dooleLangs(dooleLangObjects)
    getContentForDoodle(dooldleObject)
    return dooldleObject