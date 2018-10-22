#!/usr/bin/python
import praw
import time
import datetime
import json
import msvcrt
import io
import os
import re
import urllib
import requests

from PIL import Image
from google.cloud import vision
from google.cloud.vision import types

print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

# get facebook username, passwor
with open('settings.json') as f:
    settings = json.load(f)

# get known images
postHist = []
with open("hist.txt", "r") as f:
  for line in f:
    postHist.append(line.strip())

reddit = praw.Reddit('bot1')
vision_client = vision.ImageAnnotatorClient()

postHist = postHist[-20:] # keep the last 20 lines in the history

def getCodes(imageUrl):
    codes = []
    file = io.BytesIO(urllib.request.urlopen(imageUrl).read())
    content = file.read()

    image = types.Image(content=content)

    response = vision_client.text_detection(image=image)
    texts = response.text_annotations

    for text in texts:
        desc = format(text.description)
        pattern = r"\w*-\w*-\w*-\w*"
        if re.match(pattern, desc):
            codes.append(desc)

    return codes

def checkSubReddit(name, reddit, client, postHist):
    subreddit = reddit.subreddit(name)
    msg = ""
    for submission in subreddit.new(limit=3):
        created = datetime.datetime.fromtimestamp(submission.created_utc).strftime('%Y-%m-%d %H:%M:%S')

        if datetime.datetime.fromtimestamp(submission.created_utc) > datetime.datetime.now() - datetime.timedelta(days = 1, hours=0, minutes=0, seconds=0):
        # if 1>0:

            if not submission.id in postHist:

                title = submission.title
                shortLink = "https://redd.it/"+submission.id
                imageUrl = submission.url

                print("["+created+"] "+title+" "+imageUrl)
                postHist.append(submission.id)

                if imageUrl.endswith("jpg"):
                    
                    if len(getCodes(imageUrl)) > 0:
                        messageText = title+"\n"+shortLink
                        for code in getCodes(imageUrl):
                            messageText = messageText +"\n"+code

                        print(messageText)
                        
                        requests.post("https://api.pushover.net/1/messages.json", data = {
                        "token": settings["token"],
                        "user": settings["user"],
                        "message": messageText
                        },
                        files = {
                        "attachment": ("image.jpg", io.BytesIO(urllib.request.urlopen(imageUrl).read()), "image/jpeg")
                        }
                        )

    time.sleep(20)
    return postHist


try:	
    while 1:
        for name in settings["subreddit"]:
            postHist = checkSubReddit(name, reddit, "", postHist)
    
        time.sleep(60)
except KeyboardInterrupt: # Ctrl+C in command line

    with open("hist.txt", "w") as f:
        for line in postHist:
            f.write(line+"\n")
    print("History updated")
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    
