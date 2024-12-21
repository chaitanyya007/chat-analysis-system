import pandas as pd
from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import emoji
import seaborn as sns
import squarify
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download wordsstop words list
nltk.download('stopwords')
nltk.download('punkt_tab')

extract = URLExtract()


def fetch_stats(selected_user, df):

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    num_messages = df.shape[0]
    words = []
    for message in df['message']:
        words.extend(message.split())

    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links)


def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={
        'count':'percent', 'user':'name'
    })
    return x, df


def create_wordcloud(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    wc = WordCloud(width=500, height = 500, min_font_size=10, background_color='white')
    df_wc = wc.generate(df['message'].str.cat(sep=" "))
    return df_wc


def most_common_words(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    words = []

    for message in temp['message']:
        text = message
        stop_words = set(stopwords.words('english'))

        # Tokenize words
        message = word_tokenize(text)
        words.extend(message)
    filtered_words = [
        word for word in words
        if word.lower() not in stop_words and word not in string.punctuation
    ]
    return_df = pd.DataFrame(Counter(filtered_words).most_common(20))
    return return_df


def most_common_emojis(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    return_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return return_df


def monthly_timeline(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+"-"+str(timeline['year'][i]))

    timeline['time'] = time

    return timeline


def daily_timeline(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    d_timeline = df.groupby('only_date').count()['message'].reset_index()

    return d_timeline


def week_activity_map(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()


def month_activity_map(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()


def hourly_activity_map(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    heatmap = df.pivot_table(index = 'day_name', columns = 'period', values = 'message', aggfunc = 'count').fillna(0)
    return heatmap

def emoji_representation(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    return_df = pd.DataFrame(Counter(emojis).most_common(15))
    # Prepare data for Treemap
    labels = [f'{emoji} ({count})' for emoji, count in zip(return_df[0], return_df[1])]
    sizes = return_df[1]
    return labels, sizes

    # Plot Treemap


    


