#!/usr/bin/env python
# coding: utf-8

# In[3]:


#! python3
import praw
import pandas as pd
import datetime as dt

reddit = praw.Reddit(client_id='mOgxLW4KmZgoQg',                      client_secret='YGqzJnyG_sVwvOvWAw41dyrT6V0',                      user_agent='spreader',                      username='cvatch',                      password='')
subreddit = reddit.subreddit('onewordeach')
top_subreddit = subreddit.top(limit=1000)
topics_dict = { "title":[], "body":[],}
for submission in top_subreddit:
    topics_dict["title"].append(submission.title)
    topics_dict["body"].append(submission.selftext)
    
topics_data = pd.DataFrame(topics_dict)

topics_data.to_csv('one word each 0926.csv', index=False) 


# In[ ]:





# In[ ]:




