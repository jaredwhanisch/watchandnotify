import smtplib, ssl
import os
import praw 
import time

port = 465  # For SSL

#environment variables for email and reddit api access
sender_email = os.environ.get('SENDER_EMAIL')
sender_password = os.environ.get('SENDER_PASSWORD')
destination_email = os.environ.get('DESTINATION_EMAIL')
reddit_client_id = os.environ.get('REDDIT_CLIENT_ID')
reddit_client_secret = os.environ.get('REDDIT_CLIENT_SECRET')
reddit_user_agent = os.environ.get('REDDIT_USER_AGENT')

#list of watches you want to be notified for
keywords = ["BREW", "VOSTOK"]
#initializing the email contents, setting the subject
message = """Subject: Found a watch!\n\n"""
#read-only reddit instance
reddit = praw.Reddit(
    client_id=reddit_client_id,
    client_secret=reddit_client_secret,
    user_agent=reddit_user_agent
)

#looking at the new submissions on r/watchexchange
for submission in reddit.subreddit("watchexchange").new():
    #interating through all the different watches I'm interested in being notified for
    for keyword in keywords:
        #if the submission was created within the last hour and the title contains one of the keywords
        if((time.time() - submission.created_utc < 3600) and (submission.title.upper().find(keyword) != -1)):
            #appending all watches that match what I'm looking for to the body of the email
            message += "reddit.com"+submission.permalink+"\n" 

# Create a secure SSL context
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, destination_email, message)
    