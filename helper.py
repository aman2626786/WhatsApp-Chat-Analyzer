from urlextract import URLExtract
extractor = URLExtract()
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji
from emoji import emoji_list



def fatch_stats(selected_user,df):
    
    if selected_user != 'OverAll':
        df = df[df['users'] == selected_user]

    num_messages = df.shape[0]
    words =[]
    for massage in df['text']:
        words.extend(massage.split())
    
    # Fatch number of media messages
    media_massage = df[df['text'] == '<Media omitted>'].shape[0]

    # Fatch number of links shared
    links = []
    for text in df['text']:
        links.extend(extractor.find_urls(text))
        
    return num_messages, len(words), media_massage,len(links)

def most_busy_users(df):
    x = df['users'].value_counts().head()
    df = round((df['users'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'users':'name','count':'percent'})

    return x,df


def create_wordcloud(selected_user, df):
    if selected_user != 'OverAll':
        df = df[df['users'] == selected_user]

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(df['text'].str.cat(sep=' '))
    return df_wc


def most_common_words(selected_user, df):
    f = open("stop_hinglish.txt",'r')
    stop_words = f.read()
    if selected_user != 'OverAll':
        df = df[df['users'] == selected_user]

    temp = df[df['text'] != '<Media omitted>']
    words = []

    for text in temp['text']:
        for word in text.lower().split():
            if word not in stop_words:
                words.append(word)

    return_df = pd.DataFrame(Counter(words).most_common(20))
    return return_df


def emoji_helper(selected_user, df):
    if selected_user != 'OverAll':
        df = df[df['users'] == selected_user]

    emojis = []
    for text in df['text']:
        emojis.extend([match['emoji'] for match in emoji_list(text)])


    emoji_df = pd.DataFrame(Counter(emojis).most_common())

    return emoji_df

def monthly_timeline(selected_user, df):
    if selected_user != 'OverAll':
        df = df[df['users'] == selected_user]
    timeline = df.groupby(['year','month_num','month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "." + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline

def daily_timeline(selected_user, df):
    if selected_user != 'OverAll':
        df = df[df['users'] == selected_user]
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline 

def week_activity_map(selected_user, df):
    if selected_user != 'OverAll':
        df = df[df['users'] == selected_user]
    return df['day_name'].value_counts()

def month_activity_map(selected_user, df):
    if selected_user != 'OverAll':
        df = df[df['users'] == selected_user]
    return df['month'].value_counts()

def activity_heatmap(selected_user, df):
    if selected_user != 'OverAll':
        df = df[df['users'] == selected_user]
    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return user_heatmap



