#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pickle

with open(r'C:\Users\GrowTye\Documents\nlp-in-python-tutorial-master\growcards practice\motivation.txt', 'r') as file:
     file_contents = [file.read()]


# In[3]:


print(file_contents)
with open(r"C:\Users\GrowTye\Documents\nlp-in-python-tutorial-master\growcards practice\motivation.pickle", "wb") as file:
    pickle.dump(file_contents,file)


# In[4]:


data = {}
with open(r"C:\Users\GrowTye\Documents\nlp-in-python-tutorial-master\growcards practice\motivation.pickle","rb") as file:
    data["motivation"] = pickle.load(file)


# In[5]:


print(data)


# In[6]:


data.keys()


# In[7]:


print(data)


# In[8]:


next(iter(data.keys()))


# In[9]:


next(iter(data.values()))


# In[10]:


def combine_text(list_of_text):
    '''Takes a list of text and combines them into one large chunk of text.'''
    combined_text = ' '.join(list_of_text)
    return combined_text


# In[11]:


data_combined = {key: [combine_text(value)] for (key, value) in data.items()}


# In[12]:


import pandas as pd
pd.set_option('max_colwidth',150)

data_df = pd.DataFrame.from_dict(data_combined).transpose()
data_df.columns = ['transcript']
data_df = data_df.sort_index()
data_df


# In[13]:


data_df.transcript.loc['motivation']


# In[14]:


# Apply a first round of text cleaning techniques
import re
import string

def clean_text_round1(text):
    '''Make text lowercase, remove text in square brackets, remove punctuation and remove words containing numbers.'''
    text = text.lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\w*\d\w*', '', text)
    return text

round1 = lambda x: clean_text_round1(x)


# In[15]:


data_clean = pd.DataFrame(data_df.transcript.apply(round1))
data_clean


# In[16]:


# Apply a second round of cleaning
def clean_text_round2(text):
    '''Get rid of some additional punctuation and non-sensical text that was missed the first time around.'''
    text = re.sub('[‘’“”…]', '', text)
    text = re.sub('\n', '', text)
    return text

round2 = lambda x: clean_text_round2(x)


# In[17]:


data_clean = pd.DataFrame(data_clean.transcript.apply(round2))
data_clean


# In[18]:


data_df


# In[19]:


full_names = ['quotes']

data_df['full_name'] = full_names
data_df


# In[20]:


data_df.to_pickle("corpus.pkl")


# In[21]:


data = pd.read_pickle('corpus.pkl')
data


# In[22]:


ali_text = data.transcript.loc['motivation']
ali_text[:200]


# In[23]:


from collections import defaultdict

def markov_chain(text):
    '''The input is a string of text and the output will be a dictionary with each word as
       a key and each value as the list of words that come after the key in the text.'''
    
    # Tokenize the text by word, though including punctuation
    words = text.split(' ')
    
    # Initialize a default dictionary to hold all of the words and next words
    m_dict = defaultdict(list)
    
    # Create a zipped list of all of the word pairs and put them in word: list of next words format
    for current_word, next_word in zip(words[0:-1], words[1:]):
        m_dict[current_word].append(next_word)

    # Convert the default dict back into a dictionary
    m_dict = dict(m_dict)
    return m_dict


# In[24]:


# Create the dictionary for Ali's routine, take a look at it
ali_dict = markov_chain(ali_text)
ali_dict


# In[25]:


import random

def generate_sentence(chain, count=15):
    '''Input a dictionary in the format of key = current word, value = list of next words
       along with the number of words you would like to see in your generated sentence.'''

    # Capitalize the first word
    word1 = random.choice(list(chain.keys()))
    sentence = word1.capitalize()

    # Generate the second word from the value list. Set the new word as the first word. Repeat.
    for i in range(count-1):
        word2 = random.choice(chain[word1])
        word1 = word2
        sentence += ' ' + word2

    # End it with a period
    sentence += '.'
    return(sentence)


# In[29]:


generate_sentence(ali_dict)


# In[ ]:




