1. install python
2. run setup.bat to install praw library(reddit) and google.cloud library (image recognition)
3. copy praw.ini to python_path\Lib\site-packages\praw (e.g. C:\Users\joez\AppData\Local\Programs\Python\Python37\Lib\site-packages\praw\)
4. modify client_id and client_secret in praw.ini(this can be found at https://www.reddit.com/prefs/apps/)
5. modify settings.json for pushover token and subreddit list
6. run python /ReditBot.py