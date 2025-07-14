import re
import pandas as pd
import numpy as np

def preprocess(data):
    # Step 2: Regular expression pattern to extract datetime and message
    pattern = r'(\d{1,2}/\d{1,2}/\d{2}), (\d{1,2}:\d{2}\s?[AP]M) - (.*?)(?=(?:\n\d{1,2}/\d{1,2}/\d{2}, \d{1,2}:\d{2}\s?[AP]M -)|\Z)'

    # Step 3: Find all messages
    matches = re.findall(pattern, data, re.DOTALL)

    # Step 4: Store extracted messages
    message_list = []

    for date, time, message in matches:
        datetime_str = f"{date}, {time}"
        message_cleaned = message.strip()
        
        # Print output
        # print(f" DateTime: {datetime_str}")
        # print(f" Message: {message_cleaned}")
        # print("-" * 60)
        
        # Add to list for DataFrame
        message_list.append({
            "datetime": datetime_str,
            "message": message_cleaned
        })

    # Step 5: Convert to DataFrame
    df = pd.DataFrame(message_list)

    # Step 6: Optional – convert to datetime object
    df["datetime"] = pd.to_datetime(df["datetime"], format="%m/%d/%y, %I:%M %p")

    # Function to split name and message if ":" exists
    def split_sender_message(msg):
        if ": " in msg:
            name, text = msg.split(": ", 1)
            return name.strip(), text.strip()
        else:
            # System message or deleted message
            return np.nan, msg.strip()

    # Apply function to each row
    df[["name", "text"]] = df["message"].apply(lambda x: pd.Series(split_sender_message(x)))

    df = df.rename(columns={'name':'users'})
    df = df.fillna('unknown')

    df['year'] = df['datetime'].dt.year
    df['month_num'] = df['datetime'].dt.month
    df['month'] = df['datetime'].dt.month_name()
    df['day'] = df['datetime'].dt.day
    df['hour'] = df['datetime'].dt.hour
    df['minute'] = df['datetime'].dt.minute
    df['only_date'] = df['datetime'].dt.date
    df['day_name'] = df['datetime'].dt.day_name()

    period = []
    for hour in df[['day_name','hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour+1))
        else:
            period.append(str(hour) + "-" + str(hour+1))
    df['period'] = period
    return df





    
