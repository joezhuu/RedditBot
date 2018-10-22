1. install python
2. run setup.bat to install praw library(reddit) and google.cloud library (image recognition)
3. set environmentPath GOOGLE_APPLICATION_CREDENTIALS with the downloaded google vision credential file
4. copy praw.ini to python_path\Lib\site-packages\praw (e.g. C:\Users\joez\AppData\Local\Programs\Python\Python37\Lib\site-packages\praw\)
5. modify client_id and client_secret in praw.ini(this can be found at https://www.reddit.com/prefs/apps/)
6. modify settings.json for pushover token and subreddit list
7. run python .\ReditBot.py