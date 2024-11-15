import re
import pandas as pd


def preprocess(data):
    pattern = '\d{2}/\d{2}/\d{4}, \d{1,2}:\d{2}\s?[ap]m'

    messages = re.split(pattern, data)[1:]
    messages = [messages.replace('-', '').strip() for messages in messages]

    date_time = re.findall(pattern, data)
    date_time = [date_time.replace('\u202f', '').strip() for date_time in date_time]

    df = pd.DataFrame({'user_messages': messages, 'dates': date_time})
    df['dates'] = pd.to_datetime(df['dates'], format='%d/%m/%Y, %I:%M%p')

    users = []
    messages = []

    for message in df['user_messages']:
        entry = re.split('([^:]+):\s*(.*)', message)
        if entry[1:]:
            users.append(entry[1].strip())
            messages.append(entry[2].strip())
        else:
            users.append('group_notification')
            messages.append(message.strip())

    df['user'] = users
    df['message'] = messages
    df.drop(columns='user_messages', inplace=True)

    df['year'] = df['dates'].dt.year
    df['day'] = df['dates'].dt.day
    df['only_date'] = df['dates'].dt.date
    df['month'] = df['dates'].dt.month
    df['day_name'] = df['dates'].dt.day_name()
    df['month_name'] = df['dates'].dt.month_name()
    df['hour'] = df['dates'].dt.hour
    df['minute'] = df['dates'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df
