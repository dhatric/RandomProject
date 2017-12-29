# -*- coding: utf-8 -*- 

import wikipedia
import sys

reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

if __name__ == '__main__':
    #print wikipedia.search("Kuppali Venkatappa Puttappa")
    wikipedia.set_lang("te")
    wikiPage=wikipedia.page('కువెంపు')
    print wikiPage.title
    #print wikiPage.summary
    #print wikiPage.section("Family")
    #print wikiPage.
    #print wikiPage.images
 