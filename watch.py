import smtplib, ssl
import os
import praw 
import time

port = 465  # For SSL

#list of watches you want to be notified for
keywords = ["BREW", "VOSTOK"]
#initializing the email contents, setting the subject
message = """Subject: Found a watch!\n\n"""
#Flag to determine if a watch was found, 
update = False
#read-only reddit instance
reddit = praw.Reddit(
    client_id=os.environ.get('REDDIT_CLIENT_ID'),
    client_secret=os.environ.get('REDDIT_CLIENT_SECRET'),
    user_agent=os.environ.get('REDDIT_USER_AGENT')
)

#looking at the new submissions on r/watchexchange
for submission in reddit.subreddit("watchexchange").new():
    #interating through all the different watches I'm interested in being notified for
    for keyword in keywords:
        #if the submission was created within the last hour and the title contains one of the keywords
        if((time.time() - submission.created_utc < 3600) and (submission.title.upper().find(keyword) != -1)):
            #appending all watches that match what I'm looking for to the body of the email
            message += "reddit.com"+submission.permalink+"\n"
            update = True

# Create a secure SSL context
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login(os.environ.get('SENDER_EMAIL'), os.environ.get('SENDER_PASSWORD'))
    if update:
        server.sendmail(os.environ.get('SENDER_EMAIL'), os.environ.get('DESTINATION_EMAIL'), message.encode('utf-8'))
    