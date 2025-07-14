import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("WhatsApp Char Analyzer")

# choose a file
uploaded_file = st.sidebar.file_uploader("Upload a WhatsApp chat file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    
    df = preprocessor.preprocess(data)

    st.title("WhatsApp Chat Data Structure")
    st.dataframe(df)

    # fatch unique users
    user_list = df['users'].unique().tolist()
    user_list.remove('unknown')
    user_list.sort()
    user_list.insert(0, 'OverAll')

    selected_user = st.sidebar.selectbox("Show analysis WRT", user_list)

    if st.sidebar.button("Show Analysis"):

        st.title("Top Statistics")

        num_massages,words,media_massage,num_links = helper.fatch_stats(selected_user, df)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_massages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Total Media Shared")
            st.title(media_massage)
        with col4:
            st.header("Links Shared")
            st.title(num_links)

        # Monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'],timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        
        # Daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'],daily_timeline['message'],color='red')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # activity map
        st.title("Activity Map")
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            plt.xticks(rotation='vertical')
            ax.bar(busy_day.index, busy_day.values, color='orange')
            st.pyplot(fig)
        with col2:
            st.header("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            plt.xticks(rotation='vertical')
            ax.bar(busy_month.index, busy_month.values, color='blue')
            st.pyplot(fig)
            
        # activity heatmap
        plt.title("User Activity Heatmap")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)
                                               



    # find the busiest users in the group
    if selected_user == 'OverAll':
        st.title("Most Busy Users")
        x,new_df = helper.most_busy_users(df)
        fig, ax = plt.subplots()

        col1, col2 = st.columns(2)

        with col1:
            ax.bar(x.index, x.values,color='blue')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.dataframe(new_df)


    # create a word cloud
    st.title("Word Cloud")
    df_wc = helper.create_wordcloud(selected_user,df)
    fig, ax = plt.subplots()
    plt.imshow(df_wc)
    st.pyplot(fig)

 
    # Most common words
    most_common_df = helper.most_common_words(selected_user,df)
    fig,ax = plt.subplots()
    ax.bar(most_common_df[0], most_common_df[1], color='yellow')
    plt.xticks(rotation='vertical')
    st.title("Most Common Words")
    st.pyplot(fig)
    st.dataframe(most_common_df)



    # emoji analysis
    emoji_df = helper.emoji_helper(selected_user, df)
    st.title("Emoji Analysis")
    
    col1, col2 = st.columns(2)

    with col1:
        st.dataframe(emoji_df)
    with col2:
        if not emoji_df.empty and emoji_df.shape[1] >= 2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df.iloc[:5, 1], labels=emoji_df.iloc[:5, 1])
            st.pyplot(fig)
        else:
            st.warning("No emojis found to display in pie chart.")
