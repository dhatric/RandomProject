#!/usr/bin/python

import httplib
import httplib2
import os
import random
import sys
import time

from apiclient.discovery import build
from apiclient.errors import HttpError
from apiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow
import argparse
from Doodle import Doodle
from DoodleLang import DoodleLang

output_video_directory='../output/video/'
output_images_directory='../output/images/'

httplib2.RETRIES = 1

# Maximum number of times to retry before giving up.
MAX_RETRIES = 10

# Always retry when these exceptions are raised.
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError, httplib.NotConnected,
  httplib.IncompleteRead, httplib.ImproperConnectionState,
  httplib.CannotSendRequest, httplib.CannotSendHeader,
  httplib.ResponseNotReady, httplib.BadStatusLine)

# Always retry when an apiclient.errors.HttpError with one of these status
# codes is raised.
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

CLIENT_SECRETS_FILE = "client_secrets.json"

YOUTUBE_READ_WRITE_SSL_SCOPE = "https://www.googleapis.com/auth/youtube.force-ssl"
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.
MISSING_CLIENT_SECRETS_MESSAGE = "Client Secret Json Missing"

VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")


def get_authenticated_service(args):
  flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=YOUTUBE_READ_WRITE_SSL_SCOPE,
    message=MISSING_CLIENT_SECRETS_MESSAGE)

  storage = Storage("youtube-api-snippets-oauth2.json")
  credentials = storage.get()

  if credentials is None or credentials.invalid:
    credentials = run_flow(flow, storage, args)
  return build(API_SERVICE_NAME, API_VERSION,
      http=credentials.authorize(httplib2.Http()))


def video_upload(youtube, options):
  print "Uploading video to youtube..."  
  tags = None
  if options.keywords:
    tags = options.keywords.split(",")

  body=dict(
    snippet=dict(
      title=options.title,
      description=options.description,
      tags=tags,
      categoryId=options.category,
      still_id=options.still_id
    ),
    status=dict(
      privacyStatus=options.privacyStatus
    )
  )
  # Call the API's videos.insert method to create and upload the video.
  insert_request = youtube.videos().insert(
    part=",".join(body.keys()),
    body=body,
    media_body=MediaFileUpload(options.file, chunksize=-1, resumable=True)
  )
  return resumable_upload(insert_request,"VIDEO_UPLOAD")


def thumbnails_upload(youtube,media_file, **kwargs):
  print "Uploading thumbnail to youtube..."    
  request = youtube.thumbnails().set(media_body=MediaFileUpload(media_file, chunksize=-1,
                               resumable=True),**kwargs
  )
  resumable_upload(request,"THUMBNAIL_UPDATE")
        
# This method implements an exponential backoff strategy to resume a
# failed upload.
def resumable_upload(insert_request,API_TYPE):
  response = None
  error = None
  retry = 0
  videoID=""
  while response is None:
    try:
      status, response = insert_request.next_chunk()
      if API_TYPE == 'VIDEO_UPLOAD':
          if 'id' in response:
            videoID=response['id']
            print "Video id '%s' was successfully uploaded." % response['id']
          else:
            exit("The upload failed with an unexpected response: %s" % response)
      elif  API_TYPE == 'THUMBNAIL_UPDATE':
          print "thumbnail updated"
    except HttpError, e:
      if e.resp.status in RETRIABLE_STATUS_CODES:
        error = "A retriable HTTP error %d occurred:\n%s" % (e.resp.status,e.content)
      else:
        raise
    except RETRIABLE_EXCEPTIONS, e:
      error = "A retriable error occurred: %s" % e

    if error is not None:
      print error
      retry += 1
      if retry > MAX_RETRIES:
        exit("No longer attempting to retry.")

      max_sleep = 2 ** retry
      sleep_seconds = random.random() * max_sleep
      print "Sleeping %f seconds and then retrying..." % sleep_seconds
      time.sleep(sleep_seconds)
    return videoID;


def uploadToYoutube(videoDetails,dooldleLang,doodleObject):
  if not os.path.exists(videoDetails.file):
    exit("Please specify a valid file using the --file= parameter.")
  videoId=""
  youtube = get_authenticated_service(videoDetails)
  try:
    videoId=video_upload(youtube, videoDetails)
    thumbnails_upload(youtube,doodleObject.get_doodle_image_jpeg(),videoId=videoId)
  except HttpError, e:
    print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
    if e.resp.status == 400:
        exit("Limit reached stopping the execution")
  return videoId 