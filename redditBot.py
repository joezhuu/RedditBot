#!/usr/bin/python
import praw
import time
from datetime import datetime
from fbchat import Client
from fbchat.models import *
import json
import msvcrt

print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

# get facebook username, passwor
with open('settings.json') as f:
    settings = json.load(f)

# get known images
hist = []
with open("hist.txt", "r") as f:
  for line in f:
    hist.append(line.strip())

reddit = praw.Reddit('bot1')
client = Client(settings["botFbUser"], settings["botFbPassword"])
imageList = hist[-20:] # keep the last 20 lines in the history

def checkSubReddit(name, reddit, client, imageList):
    subreddit = reddit.subreddit(name)
    msg = ""
    for submission in subreddit.new(limit=3):
        created = datetime.fromtimestamp(submission.created_utc).strftime('%Y-%m-%d %H:%M:%S')
        title = submission.title
        shortLink = "https://redd.it/"+submission.id
        image = submission.url

        if image.endswith("png") or image.endswith("jpg"):
            if not image in imageList:
                print("[***NEW***] "+created+" "+title+" "+image)

                imageList.append(image)
                user = client.searchForUsers(settings["myFbId"])[0]
                client.sendRemoteImage(image, message=Message(text=title+"\n"+shortLink), thread_id=user.uid, thread_type=ThreadType.USER)
            else:
                print("[OLD] "+created+" "+title+" "+image)

    time.sleep(20)
    return imageList


try:	
    while 1:
        for name in settings["subreddit"]:
            imageList = checkSubReddit(name, reddit, client, imageList)
    
        time.sleep(60)
except KeyboardInterrupt: # Ctrl+C in command line
    client.logout()
    print("Logout successful")

    with open("hist.txt", "w") as f:
        for line in imageList:
            f.write(line+"\n")
    print("History updated")
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    
