import re
import pandas as pd
import numpy as np
from dateutil import parser

def preprocess(data):
    # Improved regex: works for both 12-hour and 24-hour formats
    pattern = r'(\d{1,2}/\d{1,2}/\d{2,4}), (\d{1,2}:\d{2}(?:\s?[APMapm]{2})?) - (.*?)(?=(?:\n\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2}(?:\s?[APMapm]{2})? -)|\Z)'

    matches = re.findall(pattern, data, re.DOTALL)

    message_list = []

    for date, time, message in matches:
        datetime_str = f"{date}, {time}"
        try:
            dt = parser.parse(datetime_str)  # Smart datetime parser
        except:
            dt = None  # Fail-safe if parsing fails

        message_list.append({
            "datetime": dt,
            "message": message.strip()
        })

    df = pd.DataFrame(message_list)

    # Drop messages with bad datetime
    df.dropna(subset=["datetime"], inplace=True)

    # Split sender and text
    def split_sender_message(msg):
        if ": " in msg:
            name, text = msg.split(": ", 1)
            return name.strip(), text.strip()
        else:
            return np.nan, msg.strip()

    df[["name", "text"]] = df["message"].apply(lambda x: pd.Series(split_sender_message(x)))
    df = df.rename(columns={'name': 'users'})
    df = df.fillna('unknown')

    # Add additional time-based features
    df['year'] = df['datetime'].dt.year
    df['month_num'] = df['datetime'].dt.month
    df['month'] = df['datetime'].dt.month_name()
    df['day'] = df['datetime'].dt.day
    df['hour'] = df['datetime'].dt.hour
    df['minute'] = df['datetime'].dt.minute
    df['only_date'] = df['datetime'].dt.date
    df['day_name'] = df['datetime'].dt.day_name()

    # Period mapping (for heatmap)
    period = []
    for hour in df['hour']:
        if hour == 23:
            period.append(f"{hour}-00")
        elif hour == 0:
            period.append("00-1")
        else:
            period.append(f"{hour}-{hour+1}")
    df['period'] = period

    return df
