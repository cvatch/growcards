#!/usr/bin/env python
# coding: utf-8

# In[3]:


#! python3
import praw
import pandas as pd
import datetime as dt
import re

reddit = praw.Reddit(client_id='mOgxLW4KmZgoQg',                      client_secret='YGqzJnyG_sVwvOvWAw41dyrT6V0',                      user_agent='spreader',                      username='cvatch',                      password='')
subreddit = reddit.subreddit('onewordeach')
top_subreddit = subreddit.top(limit=1000)
topics_dict = { "title":[], "body":[],}
for submission in top_subreddit:
    reddit_text = re.compile("reddit", re.IGNORECASE)
    redditors_text = re.compile("redditors", re.IGNORECASE)
    title = reddit_text.sub("The World", submission.title)
    selftext =reddit_text.sub("The World", submission.selftext)
    title = redditors_text.sub("people", title)
    selftext = redditors_text.sub("people", selftext)
    topics_dict["title"].append(title)
    topics_dict["body"].append(selftext)
    
topics_data = pd.DataFrame(topics_dict)

topics_data.to_csv('one word each 0926.csv', index=False) 


# In[ ]:





# In[ ]:




