# -*- coding: utf-8 -*- 
#!/usr/bin/python

import httplib
import httplib2
import json
import time

from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow
import argparse
from Doodle import Doodle
from DoodleLang import DoodleLang
import DoodleCommonMethods
import random

output_video_directory='../output/video/'
output_images_directory='../output/images/'
output_thumbnails_directory='../output/thumbnails/'
client_secret_directory='../client_secrets/'

httplib2.RETRIES = 1

MAX_RETRIES = 10

RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError, httplib.NotConnected,
  httplib.IncompleteRead, httplib.ImproperConnectionState,
  httplib.CannotSendRequest, httplib.CannotSendHeader,
  httplib.ResponseNotReady, httplib.BadStatusLine)

RETRIABLE_STATUS_CODES = [500, 502, 503, 504]



YOUTUBE_READ_WRITE_SSL_SCOPE = "https://www.googleapis.com/auth/youtube.force-ssl"
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"
MISSING_CLIENT_SECRETS_MESSAGE = "Client Secret Json Missing"
VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")
RATINGS = ('like', 'dislike', 'none')
secure_random = random.SystemRandom()

def get_authenticated_service(args,account):
  print account['emailId']
  CLIENT_SECRETS_FILE = client_secret_directory+account['client_secret']
  flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=YOUTUBE_READ_WRITE_SSL_SCOPE,
    message=MISSING_CLIENT_SECRETS_MESSAGE)
  storage = Storage(client_secret_directory+account['youtube_api'])
  credentials = storage.get()
  if credentials is None or credentials.invalid:
    credentials = run_flow(flow, storage, args)
  return build(API_SERVICE_NAME, API_VERSION,
      http=credentials.authorize(httplib2.Http()))

def like_video(youtube,video_id,dooldleLang,doodleObject):
     youtube.videos().rate(id=video_id,rating=RATINGS[0]).execute()
     
def comment_video(youtube,video_id,dooldleLang,doodleObject,account,**kwargs):
    comments=[]
    comments.append(dooldleLang.get_doodle_hoverText())
    comments.append(dooldleLang.get_doodle_query())
    comments.append(doodleObject.get_doodle_name())
    comments.append('Awesome content thanks for sharing')
    comments.append('good video enjoyed the background music and very informative')
    comments.append('Super video and elaborative')
    comments.append('cool video, keep uploading')
    comments.append('OMG so cool﻿')
    comments.append('I loved the video')
    comments.append('Video was very informative')
    comments.append('Loved the background music.')
    comments.append('Stickers at the background are great. Loved it')
    comments.append('I subscribed to your channel')
    comments.append('Nice Content, Please keep posting')
    
    final_comment=secure_random.choice(comments)
    if account['master'] == 'true':
        final_comment=dooldleLang.get_doodle_hoverText()
    
    properties={'snippet.channelId': 'UCr7kfsdcVIFT5dOw1y7owuw',
     'snippet.videoId': video_id,
     'snippet.topLevelComment.snippet.textOriginal': final_comment};
    resource = DoodleCommonMethods.build_resource(properties)
    kwargs = DoodleCommonMethods.remove_empty_kwargs(**kwargs)
    youtube.commentThreads().insert(body=resource,**kwargs).execute()

def populateCommomParams():
    videoDetails = argparse.Namespace()
    videoDetails.privacyStatus="public"
    videoDetails.logging_level="WARNING"
    videoDetails.noauth_local_webserver=True
    videoDetails.still_id=1
    return videoDetails    


def generateLikesComments(dooldleLang,doodleObject):
    with open('accounts.json') as json_data:
        accounts = json.load(json_data)
        for account in accounts:
            youtube = get_authenticated_service(populateCommomParams(),account)
            like_video(youtube,doodleObject.get_doodle_videoID(),dooldleLang,doodleObject)
            comment_video(youtube,doodleObject.get_doodle_videoID(),dooldleLang,doodleObject,account,part='snippet') 
            time.sleep(10)



    