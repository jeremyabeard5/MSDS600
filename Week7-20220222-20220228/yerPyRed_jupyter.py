import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
import praw
import pandas as pd
import credentials
import sqlite3
import matplotlib.pyplot as plt


def ReadCredentials():
    print('Credentials')
    print(f'Client ID: {credentials.client_id}')
    print(f'Client Secret: {credentials.client_secret}')
    print(f'User Agent: {credentials.user_agent}')



if __name__ == "__main__":
    print('Begin program.')
    #fig, axes = plt.subplots(nrows=2, ncols=2)
    
    
    
    reddit = praw.Reddit(client_id=credentials.client_id,
                         client_secret=credentials.client_secret,
                         user_agent=credentials.user_agent)
    
    print('Reading credentials...')
    ReadCredentials();
    
    print('Building subreddit object')
    reddit_data = {'title': [],
                   'link': [],
                   'author': [],
                   'n_comments': [],
                   'score': [],
                   'text': []}
    
    subreddit_name = input('Enter the subreddit to query: ') #'olympics'
    subreddit = reddit.subreddit(subreddit_name).hot(limit=None)
    
    for post in list(subreddit):
        reddit_data['title'].append(post.title)
        reddit_data['link'].append(post.permalink)
        if post.author is None:
            reddit_data['author'].append('')
        else:
            reddit_data['author'].append(post.author.name)
        
        reddit_data['n_comments'].append(post.num_comments)
        reddit_data['score'].append(post.score)
        reddit_data['text'].append(post.selftext)
        
    df = pd.DataFrame(reddit_data)
    print(df)
    
    print(f'Saving sql_{subreddit_name}.sqlite')
    con = sqlite3.connect(f'sql_{subreddit_name}.sqlite')
    df.to_sql('posts', con, if_exists='replace', index=False)
    df_check = pd.read_sql_query('SELECT * FROM posts;', con)
    con.close()
    df_check
    
    print('Plotting charts...')
    plt.figure(1)
    print('Plotting chart 1')
    #plt.ion()
    #plt.subplot(2,2,1)
    df['score'].plot.hist(bins=10, title='Scores', xlabel='Score')
    print('Plotting chart 2')
    plt.figure(2)
    #plt.subplot(2,2,2)
    df['author'].value_counts()[:10].plot.bar(title='Top Authors', ylabel='# Posts')
    #df[df['author'] == 'Compy385']
    
    print('Plotting chart 3')
    plt.figure(3)
    fd = nltk.FreqDist(' '.join(df['title']).split())
    print(fd.most_common(30))
    
    #plt.subplot(2,2,3)
    fd.plot(30, title='Raw Word Frequency')
    print('Plotting chart 4')
    plt.figure(4)
    stops = stopwords.words('english')
    stops
    
    words = ' '.join(df['title']).lower().split()
    cleaned_words = [w for w in words if w not in set(stops)]
    cleaned_fd = nltk.FreqDist(cleaned_words)
    cleaned_fd.most_common(30)
    
    #plt.subplot(2,2,4)
    cleaned_fd.plot(30, title='Cleaned Word Frequency')
    #plt.ioff()
    plt.tight_layout()
    plt.show()
    
    
    
    
    