from wordcloud import WordCloud
from urlextract import URLExtract

extract = URLExtract()


def fetch_stats(selected_user, df):
    # fetch total messages
    if selected_user != 'All Users':
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]

    # fetch total words
    words = []
    for message in df['message']:
        words.extend(message.split(' '))

    # fetch total media shared
    num_media = df[df['message'] == '<Media omitted>'].shape[0]

    # fetch total links shared
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), num_media, len(links)


def most_busy_user(df):
    # bar graph
    x = df['user'].value_counts().head()
    return x


def busy_user_percent(df):
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'user': 'User', 'count': 'Percent'})
    return df


def create_wordcloud(selected_user, df):
    df = df[df['message'] != '<Media omitted>']
    if selected_user != 'All Users':
        df = df[df['user'] == selected_user]

    wc = WordCloud(height=500, width=500, min_font_size=10, background_color='black')
    df_wc = wc.generate(df['message'].str.cat(sep=" "))

    return df_wc


def monthly_timeline(selected_user, df):
    if selected_user != 'All Users':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month', 'month_name']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month_name'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline


def daily_timeline(selected_user, df):
    if selected_user != 'All Users':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline


def weekly_activity(selected_user, df):
    if selected_user != 'All Users':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()


def monthly_activity(selected_user, df):
    if selected_user != 'All Users':
        df = df[df['user'] == selected_user]

    return df['month_name'].value_counts()


def activity_heatmap(selected_user, df):
    if selected_user != 'All Users':
        df = df[df['user'] == selected_user]

    heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return heatmap


def sunbrust_graph(selected_user, df):
    if selected_user != 'All Users':
        df = df[df['user'] == selected_user]

    user_sunbrust = df[['year', 'month_name', 'day_name']].value_counts().reset_index()

    return user_sunbrust
