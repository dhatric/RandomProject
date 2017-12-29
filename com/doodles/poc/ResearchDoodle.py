import requests
import json


if __name__ == '__main__':
    URL='https://www.google.com/doodles/json/2017/12'
    PARAMS = {'hl':'en_GB'}
    r = requests.get(url = URL, params = PARAMS)
    data = r.json()
    doodleObject=data[0]
    
    #print data.decode('unicode-escape')
    #print data[0]['title']
    translations=data[0]['translations']
    #print translations
    print translations['te']['query']
    for key in translations:
        print key
        print translations[key]

        
    