import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

st.set_page_config(
    page_title="ChatDecoder",
    layout="wide",
    page_icon="💬"
)

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300&display=swap" rel="stylesheet">
<div style='font-family: "Roboto", sans-serif; text-align: center; font-size: 46px; font-weight: 600; color: white;'>
💬ChatDecoder
""",
            unsafe_allow_html=True
            )

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300&display=swap" rel="stylesheet">
<div style='font-family: "Roboto", sans-serif; text-align: center; font-size: 25px; font-weight: 100; color: white;'>
 Insights from WhatsApp Conversations
""",
            unsafe_allow_html=True
            )

st.write("")

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300&display=swap" rel="stylesheet">
<div style='font-family: "Roboto", sans-serif; text-align: center; font-size: 20px; color: gray;'>

The ChatDecoder is a powerful tool designed to provide in-depth insights into personal and group WhatsApp conversations. It tracks key metrics such as message volume, word count, media shared, and the number of links exchanged. By identifying the most active participants, the tool reveals who is most engaged in the conversation and who might be less involved. Additionally, it generates visualizations like word clouds, monthly activity timelines, and daily activity timeline engagement maps, making it easy to identify trends and peak times of interaction.

You're analyzing the dynamics of a group chat or exploring individual conversations, the ChatDecoder helps uncover hidden patterns and behaviors, enhancing your understanding of messaging habits and interactions over time.
</div>
""", unsafe_allow_html=True)

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300&display=swap" rel="stylesheet">
<div style='font-family: "Roboto", sans-serif; text-align: center; font-size: 15px; font-weight: 400; color: red;'>
Note: ChatDecoder does not store your chat data. All interactions are processed in real-time and not saved.</div>
""", unsafe_allow_html=True)

st.title("")

uploaded_file = st.sidebar.file_uploader("Choose a WhatsApp chat file:")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    df['user'] = df['user'].replace('+91 87996 56797', 'Bhavya Patel')
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "All Users")

    st.markdown("""
            <style>
            .stat-container {
                width: 200px;
                height: 150px;
                border-radius: 30px;
                background-color: #333;
                color: white;
                text-align: center;
                font-size: 38px;
                font-weight: bold;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
                margin: auto;
            }
            .stat-title {
                font-size: 26px;
                color: #bbb;
                margin-top: 5px;
            }
            </style>
            """, unsafe_allow_html=True)

    selected_user = st.sidebar.selectbox("Do you to analyze a specific user?", user_list)

    if st.sidebar.button("Show Analysis"):
        num_messages, words, num_media, links = helper.fetch_stats(selected_user, df)

        col1, col2, col3, col4 = st.columns(4)
        # total messages
        with col1:
            st.markdown(f"""
                            <div class="stat-container">
                                <div class="stat-title">Total Messages</div>
                                <div>{num_messages}</div>
                            </div>
                            """, unsafe_allow_html=True)

        # total words
        with col2:
            st.markdown(f"""
                            <div class="stat-container">
                                <div class="stat-title">Total Words</div>
                                <div>{words}</div>
                            </div>
                            """, unsafe_allow_html=True)

        # media shared
        with col3:
            st.markdown(f"""
                            <div class="stat-container">
                                <div class="stat-title">Media Shared</div>
                                <div>{num_media}</div>
                            </div>
                            """, unsafe_allow_html=True)

        # link shared
        with col4:
            st.markdown(f"""
                            <div class="stat-container">
                                <div class="stat-title">Link Shared</div>
                                <div>{links}</div>
                            </div>
                            """, unsafe_allow_html=True)

        st.title("")

        # busy user in the group(for group only)
        if selected_user == 'All Users':
            st.markdown(
                """
                <h1 style='text-align: center; 
                    font-size: 40px; 
                    font-weight: bold; 
                    color: white;'>
                    Most Busy Users
                </h1>
                """,
                unsafe_allow_html=True
            )
            x = helper.most_busy_user(df)
            new_df = helper.busy_user_percent(df)

            col1, col2 = st.columns(2)
            # bar graph
            with col1:
                fig = px.bar(df, x=x.index, y=x.values, labels={'x': 'Users', 'y': 'Message Count'})
                fig.update_layout(
                    xaxis=dict(showgrid=True),
                    yaxis=dict(showgrid=True)
                )
                st.plotly_chart(fig)

            # pie graph
            with col2:
                pie = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
                    columns={'user': 'User', 'count': 'Percent'}).head()
                fig = px.pie(pie, names=pie['User'], values=pie['Percent'])
                st.plotly_chart(fig)

        # timeline
        st.markdown(
            """
            <h1 style='text-align: center; 
                font-size: 40px; 
                font-weight: semi-bold; 
                color: white;'>
                Timeline
            </h1>
            """,
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2)
        # daily timeline
        with col1:
            st.markdown(
                """
                <h1 style='text-align: center; 
                    font-size: 30px; 
                    font-weight: bold; 
                    color: white;'>
                    Daily Timeline
                </h1>
                """,
                unsafe_allow_html=True
            )
            daily_timeline = helper.daily_timeline(selected_user, df)
            fig = px.line(df, x=daily_timeline['only_date'], y=daily_timeline['message'], labels={'x': 'Days',
                                                                                                'y': 'Message Count'})
            fig.update_layout(
                xaxis=dict(showgrid=True),
                yaxis=dict(showgrid=True)
            )
            st.plotly_chart(fig)

        # monthly timeline
        with col2:
            st.markdown(
                """
                <h1 style='text-align: center; 
                    font-size: 30px; 
                    font-weight: bold; 
                    color: white;'>
                    Monthly Timeline
                </h1>
                """,
                unsafe_allow_html=True
            )
            timeline = helper.monthly_timeline(selected_user, df)
            fig = px.line(df, x=timeline['time'], y=timeline['message'], markers=True, labels={'x': 'Months',
                                                                                               'y': 'Message Count'})
            fig.update_layout(
                xaxis=dict(showgrid=True),
                yaxis=dict(showgrid=True)
            )
            st.plotly_chart(fig)

        # activity map
        st.markdown(
            """
            <h1 style='text-align: center; 
                font-size: 40px; 
                font-weight: semi-bold; 
                color: white;'>
                Activity Map
            </h1>
            """,
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2)
        # busy days
        with col1:
            st.markdown(
                """
                <h1 style='text-align: center;
                    font-size: 30px; 
                    font-weight: semi-bold; 
                    color: white;'>
                    Most Active Day
                </h1>
                """,
                unsafe_allow_html=True
            )
            busy_day = helper.weekly_activity(selected_user, df)
            fig = px.bar(df, x=busy_day.index, y=busy_day.values, labels={'x': 'Days', 'y': 'Message Count'})
            fig.update_layout(
                xaxis=dict(showgrid=True),
                yaxis=dict(showgrid=True)
            )
            st.plotly_chart(fig)

        # busy months
        with col2:
            st.markdown(
                """
                <h1 style='text-align: center; 
                    font-size: 30px; 
                    font-weight: semi-bold; 
                    color: white;'>
                    Most Active Month
                </h1>
                """,
                unsafe_allow_html=True
            )
            busy_month = helper.monthly_activity(selected_user, df)
            fig = px.bar(df, x=busy_month.index, y=busy_month.values, labels={'x': 'Months', 'y': 'Message Count'})
            fig.update_layout(
                xaxis=dict(showgrid=True),
                yaxis=dict(showgrid=True)
            )
            st.plotly_chart(fig)

        col1, col2 = st.columns(2)

        # create wordcloud
        with col1:
            st.markdown(
                """
                <h1 style='text-align: center; 
                    font-size: 40px; 
                    font-weight: bold; 
                    color: white;'>
                    WordCloud
                </h1>
                """,
                unsafe_allow_html=True
            )
            df_wc = helper.create_wordcloud(selected_user, df)
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.imshow(df_wc)
            ax.axis("off")
            st.pyplot(fig)

        # subrust graph
        with col2:
            st.markdown(
                """
                <h1 style='text-align: center; 
                    font-size: 40px; 
                    font-weight: bold; 
                    color: white;'>
                    Overall Usage
                </h1>
                """,
                unsafe_allow_html=True
            )
            user_sunbrust = helper.sunbrust_graph(selected_user, df)
            fig = px.sunburst(
                user_sunbrust,
                path=["year", "month_name", "day_name"],
                values="count",
            )
            st.plotly_chart(fig)

        # activity heatmap
        st.markdown(
            """
            <h1 style='text-align: center; 
                font-size: 40px; 
                font-weight: semi-bold; 
                color: white;'>
                Activity Heatmap
            </h1>
            """,
            unsafe_allow_html=True
        )

        heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots(figsize=(12, 5))
        ax = sns.heatmap(heatmap, linewidths=0.1, square=True)
        plt.xlabel('Time Period(Hours)')
        plt.ylabel('Days')
        plt.xticks(rotation=50)
        st.pyplot(fig)
